#!/usr/bin/env python3
"""Public-safe invariant checks for the native observation scratchpad."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "incident-pack-native-pilot.html"


class ObservationWorkbookContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = HTML.read_text(encoding="utf-8")

    def test_planned_cases_are_preserved(self):
        cases = re.findall(r'data-native-case="(NV-\d{3})"', self.content)
        self.assertEqual(cases, [f"NV-{i:03d}" for i in range(1, 30)])
        self.assertIn('id="native-observation-log"', self.content)
        self.assertIn('id="obs-cases"', self.content)
        self.assertIn('id="obs-export"', self.content)
        self.assertIn('id="obs-reset"', self.content)

    def test_export_is_review_candidate_not_runtime_acceptance(self):
        for invariant in (
            'classification:"source-only"',
            'observation_classification:"SELF-REPORTED / UNREVIEWED"',
            'native_verification_status:"NOT VERIFIED"',
            'independent_review_approved:false',
            'release_authorised:false',
            'publication_status:"HOLD"',
            'dev_verified:false',
            'production_verified:false',
            'native-observation-candidate-UNREVIEWED-HOLD.json'
        ):
            self.assertIn(invariant, self.content, invariant)
        self.assertNotIn('native_verification_status:"DEV-VERIFIED"', self.content)
        self.assertNotIn('release_authorised:true', self.content)

    def test_safe_local_only_input_policy(self):
        for required in (
            'function validAlias(value)',
            'function sanitizeContext()',
            'evidence_missing:',
            'missing_evidence_aliases:',
            'Object.keys(data).forEach(k=>result[k]=accepted[k]?data[k]:null)',
            'const blob=new Blob(',
            'URL.createObjectURL(blob)',
            'No observations have been recorded.'
        ):
            self.assertIn(required, self.content, required)
        start = self.content.index('<section id="native-observation-log"')
        end = self.content.index('</section>', start)
        section = self.content[start:end]
        self.assertNotRegex(section, r'<(?:form|iframe|script|img)\b')
        self.assertNotRegex(section, r'(?:https?://|mailto:)')


if __name__ == "__main__":
    unittest.main()
