import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from physics_lab.corpus import CorpusError, canonical, compare, load, read_bytes, render_html
from physics_lab.__main__ import main, PublicRedirects

FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "synthetic-corpus.json"


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.raw = FIXTURE.read_bytes()
        self.corpus = read_bytes(self.raw)
        self.data = copy.deepcopy(self.corpus.data)

    def rejected(self):
        with self.assertRaises(CorpusError):
            read_bytes(canonical(self.data))

    def test_exact_input_bytes_and_digest(self):
        self.assertEqual(self.corpus.raw, self.raw)
        self.assertEqual(self.corpus.sha256, hashlib.sha256(self.raw).hexdigest())

    def test_summary_describes_recorded_memory(self):
        self.assertEqual(self.corpus.summary()["recorded_memory_decisions"], {"RETAIN": 1, "NO_RESIDUE": 1})

    def test_raw_event_preserved(self):
        self.assertEqual(self.corpus.event(2), self.data["events"][1])

    def test_explicit_contact_reaches_source(self):
        trace = self.corpus.trace(2)
        self.assertEqual(trace["visited_indices"], [1, 2])
        self.assertEqual(trace["unresolved"], [])

    def test_no_causality_inferred_from_sequence(self):
        self.data["events"][1].pop("field_transition")
        trace = read_bytes(canonical(self.data)).trace(2)
        self.assertEqual(trace["visited_indices"], [2])
        self.assertEqual(trace["unresolved"][0]["reason"], "contact_not_recorded")

    def test_wrong_source_identity_remains_unresolved(self):
        self.data["events"][1]["field_transition"]["source_events"][0]["event_id"] = "foreign"
        self.assertFalse(read_bytes(canonical(self.data)).trace(2)["contacts"][0]["resolved"])

    def test_self_contact_is_not_traversed(self):
        source = self.data["events"][1]["field_transition"]["source_events"][0]
        source.update(event_index=2, event_id="synthetic-second-observation")
        self.assertEqual(read_bytes(canonical(self.data)).trace(2)["visited_indices"], [2])

    def test_open_carrier_shapes_preserved(self):
        for value, shape in [(False, "boolean"), (0, "number"), (None, "null"),
                             ([{"alternative": "φ"}], "array"), ("unclassified", "string")]:
            with self.subTest(shape=shape):
                carrier = self.data["events"][0]["resultant_carrier"]
                carrier.update(value=value, shape=shape)
                self.assertEqual(read_bytes(canonical(self.data)).events[0]["resultant_carrier"]["value"], value)

    def test_legacy_statement_supported(self):
        self.data["schema"] = "mm_dnd.regenerative_lab_public_projection.v0.1"
        self.data["events"][0].pop("resultant_carrier")
        self.data["events"][0]["statement"] = "Recorded legacy statement"
        self.assertEqual(read_bytes(canonical(self.data)).events[0]["statement"], "Recorded legacy statement")

    def test_unknown_schema_not_downgraded(self):
        self.data["schema"] = "future.v9"
        self.rejected()

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(CorpusError):
            read_bytes(b'{"schema": 1, "schema": 2}')

    def test_nonfinite_numbers_rejected(self):
        for value in (b'NaN', b'Infinity', b'1e999'):
            with self.subTest(value=value), self.assertRaises(CorpusError):
                read_bytes(b'{"number":' + value + b'}')

    def test_privacy_flags_are_required(self):
        del self.data["privacy"]["contains_secrets"]
        self.rejected()

    def test_privacy_true_is_rejected(self):
        self.data["privacy"]["contains_prompts"] = True
        self.rejected()

    def test_known_private_marker_rejected(self):
        self.data["events"][0]["source_relations"] = [{"source_path": "/root/private"}]
        self.rejected()

    def test_authority_not_granted(self):
        self.data["authority"] = {"measurement_authorized": True}
        self.rejected()

    def test_boolean_indices_rejected(self):
        self.data["events"][0]["event_index"] = True
        self.rejected()

    def test_sequence_gap_rejected(self):
        self.data["events"][1]["event_index"] = 3
        self.rejected()

    def test_duplicate_event_identity_rejected(self):
        self.data["events"][1]["event_id"] = self.data["events"][0]["event_id"]
        self.rejected()

    def test_current_identity_must_match(self):
        self.data["current"]["latest_event_id"] = "other"
        self.rejected()

    def test_count_must_match(self):
        self.data["machine"]["processed_events"] = 3
        self.rejected()

    def test_recorded_deposit_digest_required(self):
        self.data["events"][0]["provenance"]["deposit_sha256"] = "wrong"
        self.rejected()

    def test_carrier_shape_must_match(self):
        self.data["events"][0]["resultant_carrier"]["shape"] = "string"
        self.rejected()

    def test_unknown_optional_fields_are_preserved(self):
        self.data["events"][0]["future_relation"] = {"something": [1, 2]}
        self.assertEqual(read_bytes(canonical(self.data)).events[0]["future_relation"], {"something": [1, 2]})

    def test_malformed_memory_decision_rejected(self):
        self.data["events"][0]["memory_decision"] = {"unexpected": "shape"}
        self.rejected()

    def test_malformed_contact_rejected(self):
        self.data["events"][1]["field_transition"]["source_events"] = ["not a contact record"]
        self.rejected()

    def test_sha256_binding(self):
        read_bytes(self.raw, self.corpus.sha256)
        for bad in ("0" * 64, "not-a-digest"):
            with self.subTest(bad=bad), self.assertRaises(CorpusError):
                read_bytes(self.raw, bad)

    def test_projection_changes_are_not_hidden(self):
        self.data["events"][0]["memory_decision"] = "COOL"
        result = compare(self.corpus, read_bytes(canonical(self.data)))
        self.assertEqual(result["changed_ids"], ["synthetic-first-observation"])
        self.assertFalse(result["existing_prefix_preserved"])

    def test_append_only_projection(self):
        before = copy.deepcopy(self.data)
        before["events"] = before["events"][:1]
        before["current"].update(latest_event_id="synthetic-first-observation", latest_event_index=1)
        before["machine"]["processed_events"] = 1
        result = compare(read_bytes(canonical(before)), self.corpus)
        self.assertTrue(result["existing_prefix_preserved"])
        self.assertEqual(result["added_ids"], ["synthetic-second-observation"])

    def test_report_escapes_record_content(self):
        self.data["events"][0]["resultant_carrier"]["value"] = {"text": "<script>alert(1)</script>"}
        output = render_html(read_bytes(canonical(self.data)))
        self.assertNotIn("<script>", output)
        self.assertIn("&lt;script&gt;", output)
        self.assertIn("default-src 'none'", output)

    def test_public_fetch_preserves_raw_bytes_and_receipt(self):
        with tempfile.TemporaryDirectory() as folder, patch("physics_lab.__main__.fetch_bytes", return_value=self.raw), patch("sys.stdout", new_callable=io.StringIO):
            output = Path(folder) / "corpus.json"
            self.assertEqual(main(["fetch", "--output", str(output)]), 0)
            self.assertEqual(output.read_bytes(), self.raw)
            receipt = json.loads(output.with_name("corpus.json.receipt.json").read_text())
            self.assertEqual(receipt["sha256"], self.corpus.sha256)

    def test_fetch_never_overwrites(self):
        with tempfile.TemporaryDirectory() as folder, patch("physics_lab.__main__.fetch_bytes") as network, patch("sys.stderr", new_callable=io.StringIO):
            output = Path(folder) / "corpus.json"
            output.write_bytes(b"foreign data")
            self.assertEqual(main(["fetch", "--output", str(output)]), 2)
            self.assertEqual(output.read_bytes(), b"foreign data")
            network.assert_not_called()

    def test_bad_download_creates_no_file(self):
        with tempfile.TemporaryDirectory() as folder, patch("physics_lab.__main__.fetch_bytes", return_value=b'{}'), patch("sys.stderr", new_callable=io.StringIO):
            output = Path(folder) / "corpus.json"
            self.assertEqual(main(["fetch", "--output", str(output)]), 2)
            self.assertFalse(output.exists())

    def test_report_never_overwrites(self):
        with tempfile.TemporaryDirectory() as folder, patch("sys.stderr", new_callable=io.StringIO):
            output = Path(folder) / "report.html"
            output.write_text("foreign data")
            self.assertEqual(main(["report", str(FIXTURE), "--output", str(output)]), 2)
            self.assertEqual(output.read_text(), "foreign data")

    def test_cross_origin_redirect_rejected(self):
        with self.assertRaises(CorpusError):
            PublicRedirects().redirect_request(None, None, 302, "", {}, "http://localhost/private")

    def test_oversized_input_rejected(self):
        with patch("physics_lab.corpus.MAX_BYTES", 4), self.assertRaises(CorpusError):
            read_bytes(self.raw)

    def test_cli_commands_offline(self):
        for command in ("verify", "summary", "event", "trace"):
            with self.subTest(command=command), patch("sys.stdout", new_callable=io.StringIO) as output:
                argv = [command, str(FIXTURE)]
                if command in {"event", "trace"}:
                    argv += ["--index", "2"]
                self.assertEqual(main(argv), 0)
                self.assertIsInstance(json.loads(output.getvalue()), dict)

    def test_absent_occurrence_is_explicit(self):
        with self.assertRaises(CorpusError):
            self.corpus.event(999)

    def test_cli_unicode_survives_non_utf8_console(self):
        self.data["events"][0]["resultant_carrier"]["value"] = {"math": "φ − ∞"}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "unicode.json"
            path.write_bytes(canonical(self.data))
            buffer = io.BytesIO()
            console = io.TextIOWrapper(buffer, encoding="ascii")
            with patch("sys.stdout", console):
                self.assertEqual(main(["event", str(path), "--index", "1"]), 0)
                console.flush()
            self.assertEqual(json.loads(buffer.getvalue().decode("utf-8"))["resultant_carrier"]["value"], {"math": "φ − ∞"})


if __name__ == "__main__":
    unittest.main()
