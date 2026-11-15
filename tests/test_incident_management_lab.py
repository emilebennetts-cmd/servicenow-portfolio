"""Incident Management static portfolio acceptance: accessible and fail-closed."""
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
class IncidentManagementLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page=(ROOT/"incident-management-implementation-lab.html").read_text(encoding="utf-8")
        cls.script=(ROOT/"incident-management-implementation-lab.js").read_text(encoding="utf-8")
    def test_accessibility_and_offline_boundaries(self):
        for marker in ('lang="en"','id="main"','aria-live="polite"','aria-pressed="true"',
                       "prefers-reduced-motion","@media(max-width:560px)","script-src 'self'",
                       "connect-src 'none'","img-src 'none'","form-action 'none'",
                       'id="export-all"','src="incident-management-implementation-lab.js"'):
            with self.subTest(marker=marker):self.assertIn(marker,self.page)
        self.assertNotRegex(self.page,r"<(?:img|iframe|canvas|picture)\b")
        self.assertNotRegex(self.page,r'<script[^>]*>\s*[^<\s]')
        for banned in ("localStorage","sessionStorage","fetch(","XMLHttpRequest","innerHTML"):
            self.assertNotIn(banned,self.script)
    def test_architecture_and_claim_boundaries(self):
        for marker in ("Incident Management","impact","urgency","SLA","service request",
                       "Problem","Change","CMDB","Service Operations Workspace","ITSM",
                       "MOCK-ONLY","SOURCE-ONLY","DEV-REPORTED","DEV-VERIFIED","PRODUCTION-VERIFIED",
                       "NOT RUN","HOLD","no ServiceNow licence","No genuine ServiceNow screenshots"):
            with self.subTest(marker=marker):self.assertIn(marker.lower(),self.page.lower())
    def test_unique_controls_and_export(self):
        ids=re.findall(r'\["(IN-[IRC]\d\d)"',self.script)
        self.assertEqual(len(ids),24);self.assertEqual(len(set(ids)),24)
        for marker in ('native:"NOT RUN"','release:"HOLD"','classification:"MOCK-ONLY"',
                       'allCsv(marks)','URL.revokeObjectURL(url)'):
            self.assertIn(marker,self.script)
        self.assertNotIn('native:"PASSED"',self.script)
if __name__=="__main__":unittest.main()
