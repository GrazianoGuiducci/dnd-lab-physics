"""Inspect public records without reconstructing private Lab memory.

This is a consumer of the MM-DND public projection, not its producer or an
implementation of the regenerative researcher. All analyses are descriptive.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import html
import json
from pathlib import Path
import re
from typing import Any

PUBLIC_URL = "https://d-nd.com/data/lab/regenerative/latest.json"
SCHEMAS = {
    "mm_dnd.regenerative_lab_public_projection.v0.1",
    "mm_dnd.regenerative_lab_public_projection.v0.2",
}
MAX_BYTES = 32 * 1024 * 1024
PRIVACY_KEYS = (
    "contains_private_paths", "contains_prompts", "contains_provider_logs",
    "contains_raw_provider_output", "contains_secrets",
)
# Match the owner's known private-value markers; this is an additional bounded
# check, not a general detector or permission to publish arbitrary input.
PRIVATE_MARKERS = ("/opt/", "/root/", "c:\\", "api_key", "authorization:",
                   "bearer ", "oauth_snapshot")


class CorpusError(ValueError):
    """Invalid, unsupported or non-public projection."""


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CorpusError("duplicate JSON key")
        result[key] = value
    return result


def _constant(_value):
    raise CorpusError("non-finite JSON number")


def _integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _public_values(value: Any) -> bool:
    if isinstance(value, dict):
        return all(_public_values(k) and _public_values(v) for k, v in value.items())
    if isinstance(value, list):
        return all(_public_values(v) for v in value)
    return not isinstance(value, str) or not any(
        marker in value.casefold() for marker in PRIVATE_MARKERS)


def _next_relation(value: Any) -> bool:
    return value is None or isinstance(value, str) or (isinstance(value, dict) and bool(value))


def _shape(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    return "number"


@dataclass(frozen=True)
class Corpus:
    data: dict[str, Any]
    raw: bytes

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.raw).hexdigest()

    @property
    def events(self) -> list[dict[str, Any]]:
        return self.data["events"]

    def event(self, index: int) -> dict[str, Any]:
        for row in self.events:
            if row["event_index"] == index:
                return row
        raise CorpusError("occurrence index is absent from this projection")

    def summary(self) -> dict[str, Any]:
        return {
            "schema": self.data["schema"], "sha256": self.sha256,
            "bytes": len(self.raw), "occurrences": len(self.events),
            "current": self.data["current"], "machine": self.data["machine"],
            "recorded_memory_decisions": dict(Counter(
                e.get("memory_decision", "not_expressed") for e in self.events)),
            "reading": "Public records; integrity checks do not validate physical claims.",
        }

    def trace(self, index: int) -> dict[str, Any]:
        """Follow only explicit recorded contacts, never chronological adjacency."""
        by_index = {e["event_index"]: e for e in self.events}
        pending, seen, contacts, unresolved = [index], set(), [], []
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            event = by_index[current]
            transition = event.get("field_transition")
            if not isinstance(transition, dict):
                unresolved.append({"event_index": current, "reason": "contact_not_recorded"})
                continue
            for source in transition.get("source_events", []):
                previous = by_index.get(source.get("event_index"))
                match = (previous is not None
                         and previous["event_id"] == source.get("event_id")
                         and previous["event_index"] < current)
                contacts.append({"to_event_index": current, "recorded_source": source,
                                 "resolved": match})
                if match:
                    pending.append(previous["event_index"])
                else:
                    unresolved.append({"event_index": current,
                                       "reason": "source_contact_not_resolved"})
        return {"event_index": index, "visited_indices": sorted(seen),
                "contacts": contacts, "unresolved": unresolved,
                "reading": "Recorded contact is not independent proof of causation."}


def read_bytes(raw: bytes, expected_sha256: str | None = None) -> Corpus:
    if len(raw) > MAX_BYTES:
        raise CorpusError("projection exceeds the 32 MiB reader limit")
    if expected_sha256 is not None:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
            raise CorpusError("expected SHA-256 must contain 64 hexadecimal characters")
        if hashlib.sha256(raw).hexdigest() != expected_sha256.lower():
            raise CorpusError("projection SHA-256 mismatch")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                          parse_constant=_constant)
        # Also reject a finite-looking literal such as 1e999 that overflows.
        canonical(data)
    except (UnicodeError, ValueError, TypeError, RecursionError) as exc:
        raise CorpusError("invalid strict UTF-8 JSON projection") from exc
    if not isinstance(data, dict) or data.get("schema") not in SCHEMAS:
        raise CorpusError("unsupported public projection schema; no conversion attempted")
    privacy = data.get("privacy")
    if not isinstance(privacy, dict) or any(privacy.get(k) is not False for k in PRIVACY_KEYS):
        raise CorpusError("all five public privacy declarations must be explicitly false")
    if not _public_values(data):
        raise CorpusError("projection contains a known private-value marker")
    authority = data.get("authority", {})
    if not isinstance(authority, dict) or any(
        authority.get(k, False) is not False for k in (
            "projection_is_scientific_authority", "measurement_authorized",
            "promotion_allowed", "projection_authorizes_publication")):
        raise CorpusError("public projection cannot grant scientific or operational authority")
    events, current, machine = data.get("events"), data.get("current"), data.get("machine")
    if not isinstance(events, list) or not events or not isinstance(current, dict) or not isinstance(machine, dict):
        raise CorpusError("expected a complete non-empty projection with current and machine")
    ids = set()
    for index, event in enumerate(events, 1):
        if not isinstance(event, dict) or type(event.get("event_index")) is not int or event["event_index"] != index:
            raise CorpusError("complete projection must have ordered contiguous occurrence indices")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id or event_id in ids:
            raise CorpusError("occurrence identities must be non-empty and unique")
        ids.add(event_id)
        if "memory_decision" in event and not isinstance(event["memory_decision"], str):
            raise CorpusError("recorded memory decision must be a string")
        if event.get("state") not in {"OCCURRENCE", "REGENERATIVE_EVENT", "NO_EVENT"}:
            raise CorpusError("unsupported occurrence state; no classification inferred")
        if "next_relation" not in event or not _next_relation(event["next_relation"]):
            raise CorpusError("next relation must be null, text or a non-empty source record")
        if any(not isinstance(event.get(key), str) for key in ("finite_state", "observed_at")):
            raise CorpusError("occurrence state and observation time must be strings")
        provenance = event.get("provenance", {})
        if not isinstance(provenance, dict) or not re.fullmatch(r"[0-9a-f]{64}", str(provenance.get("deposit_sha256", ""))):
            raise CorpusError("each occurrence needs its recorded deposit SHA-256")
        carrier = event.get("resultant_carrier")
        if carrier is not None:
            if (not isinstance(carrier, dict)
                or carrier.get("schema") != "mm_dnd.lab_regenerative_resultant_carrier.v0.1"
                or "value" not in carrier or carrier.get("shape") != _shape(carrier["value"])):
                raise CorpusError("unsupported or inconsistent open resultant carrier")
        elif not isinstance(event.get("statement"), str):
            raise CorpusError("legacy occurrence needs its statement compatibility view")
        transition = event.get("field_transition")
        if transition is not None and (
            not isinstance(transition, dict)
            or not isinstance(transition.get("source_events", []), list)
            or any(not isinstance(row, dict) or type(row.get("event_index")) is not int
                   or not isinstance(row.get("event_id"), str)
                   for row in transition.get("source_events", []))):
            raise CorpusError("malformed recorded contact")
    latest = events[-1]
    if (type(current.get("latest_event_index")) is not int
        or current["latest_event_index"] != latest["event_index"]
        or current.get("latest_event_id") != latest["event_id"]
        or current.get("latest_event_state") != latest["state"]):
        raise CorpusError("current occurrence does not match the complete projection")
    for key in ("finite_state", "observed_at", "next_relation"):
        if key not in current or canonical(current[key]) != canonical(latest[key]):
            raise CorpusError("current occurrence view differs from its latest public record")
    for key in ("lab_continues", "mandatory_followup"):
        if key in current or key in latest:
            if type(current.get(key)) is not bool or current[key] is not latest.get(key):
                raise CorpusError("current occurrence continuity flag differs from its record")
    if type(machine.get("processed_events")) is not int or machine["processed_events"] != len(events):
        raise CorpusError("processed event count does not match the projection")
    if any(not _integer(machine.get(k)) for k in ("provider_calls", "retries")):
        raise CorpusError("machine counters must be non-negative integers")
    return Corpus(data, raw)


def load(path: str | Path, expected_sha256: str | None = None) -> Corpus:
    with Path(path).open("rb") as stream:
        return read_bytes(stream.read(MAX_BYTES + 1), expected_sha256)


def compare(before: Corpus, after: Corpus) -> dict[str, Any]:
    old = {e["event_id"]: e for e in before.events}
    new = {e["event_id"]: e for e in after.events}
    changed = [k for k in old.keys() & new.keys() if digest(old[k]) != digest(new[k])]
    removed = list(old.keys() - new.keys())
    prefix_preserved = after.events[:len(before.events)] == before.events
    return {"before_sha256": before.sha256, "after_sha256": after.sha256,
            "added_ids": sorted(new.keys() - old.keys()), "removed_ids": sorted(removed),
            "changed_ids": sorted(changed), "existing_prefix_preserved": prefix_preserved,
            "reading": "Projection differences; a changed rendering is not proof that a private deposit changed."}


def render_html(corpus: Corpus) -> str:
    def block(value):
        return "<pre>" + html.escape(json.dumps(value, ensure_ascii=False, indent=2)) + "</pre>"
    rows = []
    for event in corpus.events:
        value = event.get("resultant_carrier", {}).get("value", event.get("statement"))
        rows.append(f'<details id="e{event["event_index"]}"><summary>E{event["event_index"]} · '
                    + html.escape(event["event_id"]) + "</summary><h3>Recorded resultant</h3>"
                    + block(value) + "<h3>Complete public record</h3>" + block(event) + "</details>")
    return """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>MM-DND Physics Lab — public corpus</title><style>
body{max-width:1000px;margin:3rem auto;padding:0 1rem;background:#101820;color:#e6eef2;font:17px/1.6 system-ui}
h1,h2,h3{line-height:1.3}a{color:#8ce1cf}details{margin:1rem 0;border:1px solid #52646c;padding:1rem;border-radius:8px}
summary{cursor:pointer;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}
</style><main><h1>MM-DND Physics Lab</h1><p>Offline reading of one public corpus.
Records preserve their source language and open resultant values. Recorded outcomes do not certify physical laws.</p>
<h2>Snapshot identity</h2>""" + block(corpus.summary()) + "<h2>Occurrences</h2>" + "".join(rows) + "</main></html>\n"
