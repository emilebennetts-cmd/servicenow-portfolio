"""Problem Management static case study must remain accessible, offline and fail-closed."""
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ProblemManagementLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page=(ROOT/"problem-management-implementation-lab.html").read_text(encoding="utf-8")
        cls.script=(ROOT/"problem-management-implementation-lab.js").read_text(encoding="utf-8")
    def test_mobile_access_and_offline_policy(self):
        for marker in ('lang="en"','id="main"','aria-live="polite"','aria-pressed="true"',
                       "@media(max-width:570px)","prefers-reduced-motion","script-src 'self'",
                       "connect-src 'none'","img-src 'none'","form-action 'none'",
                       'id="export-all"','src="problem-management-implementation-lab.js"'):
            with self.subTest(marker=marker):self.assertIn(marker,self.page)
        self.assertNotRegex(self.page,r'<(?:img|iframe|canvas|picture)\b')
        self.assertNotRegex(self.page,r'<script[^>]*>\s*[^<\s]')
        for banned in ("localStorage","sessionStorage","fetch(","innerHTML","XMLHttpRequest"):
            self.assertNotIn(banned,self.script)
    def test_native_boundary_and_entitlements(self):
        for marker in ("Problem Tasks","CMDB","Known error","Change","ITSM","Service Operations Workspace",
                       "MOCK-ONLY","SOURCE-ONLY","DEV-REPORTED","DEV-VERIFIED","PRODUCTION-VERIFIED",
                       "NOT RUN","HOLD","no ServiceNow licence","No genuine ServiceNow screenshots"):
            with self.subTest(marker=marker):self.assertIn(marker.lower(),self.page.lower())
    def test_unique_gates_and_fixed_export(self):
        ids=re.findall(r'\["(PR-[DKF]\d\d)"',self.script)
        self.assertEqual(len(ids),24);self.assertEqual(len(set(ids)),24)
        for marker in ('native:"NOT RUN"','release:"HOLD"','classification:"MOCK-ONLY"',
                       'allCsv(marks)','URL.revokeObjectURL(url)'):
            self.assertIn(marker,self.script)
        self.assertNotIn('native:"PASSED"',self.script)
if __name__=="__main__":unittest.main()
