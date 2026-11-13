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


    def test_import_is_fail_closed_and_never_promotes_evidence(self):
        required = (
            'function readCandidate(packet)',
            'function applyCandidate(parsed)',
            'id="obs-import-file"',
            'id="obs-import-status"',
            'file.size>131072||file.size===0',
            'packet.native_verification_status!=="NOT VERIFIED"',
            'packet.publication_status!=="HOLD"',
            'packet.release_authorised!==false',
            'packet.independent_review_approved!==false',
            'row.dev_verified!==false||row.production_verified!==false',
            'row.case_id!==id',
            'row.workstream!==node.dataset.nativeGroup',
            'row.persona!==node.dataset.nativePersona',
            'row.planned_control!==node.querySelector("h3").textContent',
            'row.evidence_missing!==missing',
            'Object.keys(context).length!==4',
            'Object.keys(row).length!==allowed.length',
            'field.value=""',
            'Current entries unchanged.',
            'Restored 29 candidate notes locally.'
        )
        for rule in required:
            self.assertIn(rule, self.content, rule)
        self.assertNotIn("localStorage", self.content)
        self.assertNotIn("sessionStorage", self.content)

    def test_import_does_not_expose_upload_or_network_surface(self):
        start = self.content.index('<section id="native-observation-log"')
        end = self.content.index('</section>', start)
        section = self.content[start:end]
        self.assertIn('type="file"', section)
        self.assertNotRegex(section, r'<(?:form|iframe|script|img)\b')
        self.assertNotRegex(section, r'(?:https?://|mailto:|enctype=|method=)')
        self.assertIn('JSON.parse(await file.text())', self.content)
        self.assertIn('output.textContent=', self.content)


if __name__ == "__main__":
    unittest.main()
