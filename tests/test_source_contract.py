import csv
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "records"


class SourceContract(unittest.TestCase):
    def test_export_shape(self):
        self.assertLessEqual(set(EXPECTED), {path.name for path in ROOT.iterdir()})
        for name, contract in EXPECTED.items():
            with self.subTest(source=name):
                path = ROOT / name
                if path.suffix == ".csv":
                    with path.open(encoding="utf-8", newline="") as source:
                        reader = csv.DictReader(source)
                        self.assertEqual(reader.fieldnames, contract)
                        rows = list(reader)
                    self.assertTrue(rows)
                    self.assertTrue(all(None not in row and None not in row.values() for row in rows))
                else:
                    body = json.loads(path.read_text(encoding="utf-8"))
                    self.assertIsInstance(body, list if contract == "list" else dict)
                    self.assertTrue(body)

    def test_related_export_records(self):
        for name, value in SEQUENCE.items():
            with self.subTest(source=name):
                path = ROOT / name
                if path.suffix == ".csv":
                    with path.open(encoding="utf-8", newline="") as source:
                        cells = {cell for row in csv.reader(source) for cell in row}
                else:
                    rows = json.loads(path.read_text(encoding="utf-8"))
                    cells = {item for row in rows for item in row.values() if isinstance(item, str)}
                self.assertIn(value, cells)


EXPECTED = {'layer_share.json': 'dict', 'assets.csv': ['platform', 'package', 'tag', 'master', 'start', 'end', 'audio', 'region', 'basis_unit', 'weight'], 'meters.csv': ['package', 'source_tag', 'meter', 'master', 'start', 'end', 'audio', 'region', 'unit', 'amount'], 'statements.csv': ['id', 'at', 'platform', 'package', 'currency', 'minor', 'kind', 'specific', 'reference'], 'grants.csv': ['id', 'payee', 'master', 'start', 'end', 'audio', 'region', 'layer', 'share', 'exclusive', 'priority', 'from', 'through'], 'revisions.csv': ['seq', 'kind', 'grant', 'from', 'through', 'start', 'end', 'region', 'audio'], 'wire.csv': ['seq', 'transfer', 'kind', 'source', 'original', 'payee', 'currency', 'minor', 'grant', 'start', 'end']}
SEQUENCE = {'grants.csv': 'g3', 'statements.csv': 'refund', 'wire.csv': 'recover'}
