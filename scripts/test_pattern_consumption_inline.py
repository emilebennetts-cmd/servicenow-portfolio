"""The source model and inline, offline public demonstrator must never drift."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PatternConsumptionInlineTests(unittest.TestCase):
    def test_offline_no_external_script_and_exact_source_sync(self):
        html=(ROOT/"pattern-library.html").read_text(encoding="utf-8")
        model=(ROOT/"pattern-consumption-contract.js").read_text(encoding="utf-8").strip()
        self.assertIn("<script>\n"+model+"\n</script>",html)
        self.assertNotRegex(html,r"<script\s+src=")
        self.assertIn("script-src 'unsafe-inline'",html)
        self.assertNotIn("script-src 'self'",html)
    def test_source_has_no_remote_endpoint(self):
        model=(ROOT/"pattern-consumption-contract.js").read_text(encoding="utf-8")
        self.assertNotIn("fetch(",model)
        self.assertNotIn("XMLHttpRequest",model)
        self.assertNotIn("navigator.sendBeacon",model)
if __name__=="__main__":unittest.main()
