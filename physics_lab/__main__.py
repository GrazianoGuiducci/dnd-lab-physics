"""Run with python -m physics_lab. No provider or operational Lab controller."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request
from urllib.parse import urlsplit

from .corpus import CorpusError, MAX_BYTES, PUBLIC_URL, compare, load, read_bytes, render_html


class PublicRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urlsplit(newurl)
        if target.scheme != "https" or target.netloc != "d-nd.com":
            raise CorpusError("public download redirected outside its HTTPS origin")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_bytes() -> bytes:
    request = urllib.request.Request(PUBLIC_URL, headers={
        "Accept": "application/json", "User-Agent": "dnd-lab-physics-public-reader/0.2"})
    with urllib.request.build_opener(PublicRedirects).open(request, timeout=45) as response:
        return response.read(MAX_BYTES + 1)


def write_new(path: Path, content: bytes) -> None:
    # Exclusive creation prevents overwriting snapshots, sources or foreign work.
    with path.open("xb") as stream:
        stream.write(content)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Inspect the MM-DND Physics Lab public corpus offline.")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("verify", "summary", "event", "trace", "report"):
        command = commands.add_parser(name)
        command.add_argument("corpus", type=Path)
        command.add_argument("--expected-sha256")
        if name in ("event", "trace"):
            command.add_argument("--index", type=int, required=True)
        if name == "report":
            command.add_argument("--output", type=Path, required=True)
    command = commands.add_parser("compare")
    command.add_argument("before", type=Path)
    command.add_argument("after", type=Path)
    command = commands.add_parser("fetch", help="Download only the fixed public HTTPS projection")
    command.add_argument("--output", type=Path, required=True)
    command.add_argument("--expected-sha256")
    return root


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parser().parse_args(argv)
    try:
        if args.command == "compare":
            result = compare(load(args.before), load(args.after))
        elif args.command == "fetch":
            receipt = args.output.with_name(args.output.name + ".receipt.json")
            if args.output.exists() or receipt.exists():
                raise CorpusError("snapshot or receipt already exists; choose a new output name")
            corpus = read_bytes(fetch_bytes(), args.expected_sha256)
            result = {"source_url": PUBLIC_URL, "retrieved_at": datetime.now(timezone.utc).isoformat(),
                      "sha256": corpus.sha256, "bytes": len(corpus.raw),
                      "latest_event_index": corpus.data["current"]["latest_event_index"],
                      "license": "Source rights retained; repository MIT license does not relicense this download."}
            write_new(args.output, corpus.raw)
            # If interrupted here, the untouched raw snapshot remains independently
            # verifiable; an absent receipt must not be reported as a full download.
            write_new(receipt, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode())
        else:
            corpus = load(args.corpus, args.expected_sha256)
            if args.command == "verify":
                result = {"valid_public_projection": True, "sha256": corpus.sha256,
                          "occurrences": len(corpus.events),
                          "private_deposit_bytes_verified": False,
                          "scientific_claims_validated": False}
            elif args.command == "summary":
                result = corpus.summary()
            elif args.command == "event":
                result = corpus.event(args.index)
            elif args.command == "trace":
                corpus.event(args.index)
                result = corpus.trace(args.index)
            else:
                write_new(args.output, render_html(corpus).encode("utf-8"))
                result = {"report": str(args.output), "source_sha256": corpus.sha256,
                          "occurrences": len(corpus.events)}
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (CorpusError, OSError, ValueError, urllib.error.URLError, RecursionError):
        # Do not echo malformed records, exception URLs or possible secret input.
        print("Cannot complete: invalid/unsupported public input, integrity mismatch, unavailable network, "
              "or output already exists. Use --help and a fresh output path.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
