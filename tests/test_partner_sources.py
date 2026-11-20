import csv
import json
from pathlib import Path
import unittest


RECORDS = Path(__file__).resolve().parents[1] / 'records'
SCHEMAS = {'clearing_terms.json': 'dict', 'clearing_events.csv': ['at', 'actual_at', 'batch', 'line', 'business_ref', 'source', 'currency', 'minor', 'action', 'state', 'bank_ref'], 'clearing_lines.csv': ['ref', 'original', 'master', 'start', 'end', 'audio', 'region', 'grant', 'payee']}


class PartnerSourceTests(unittest.TestCase):
    def test_format(self):
        for name, shape in SCHEMAS.items():
            with self.subTest(name=name), (RECORDS / name).open(encoding='utf-8', newline='') as source:
                if isinstance(shape, list):
                    rows = csv.DictReader(source)
                    self.assertEqual(rows.fieldnames, shape)
                    records = list(rows)
                    self.assertTrue(records)
                    self.assertTrue(all(None not in row and None not in row.values() for row in records))
                else:
                    records = json.load(source)
                    self.assertIsInstance(records, list if shape == 'list' else dict)
                    self.assertTrue(records)
