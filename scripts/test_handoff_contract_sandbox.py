"""Offline contract simulator checks. JS logic is demonstrative, never native verification."""
from html.parser import HTMLParser
from pathlib import Path
import json
import shutil
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"governed-handoff-contract.html"
JS=ROOT/"handoff-contract-engine.js"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.scripts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag=="script": self.scripts.append(a.get("src"))

class HandoffSandboxTests(unittest.TestCase):
    def test_page_has_accessible_controls_and_explicit_boundary(self):
        html=PAGE.read_text(encoding="utf-8")
        p=Parser(); p.feed(html)
        self.assertIn("handoff-contract-engine.js",p.scripts)
        for key in ("hc-form","hc-scenario","hc-version","hc-reviewed","hc-authorised",
                    "hc-evidence","hc-supported","hc-conflict","hc-replay",
                    "hc-download","hc-output","hc-status","hc-checks"):
            self.assertIn(key,p.ids)
        for text in ("MOCK-ONLY","NOT DEPLOYED","NOT RUN","not server assertions",
                     "no free-text customer entry","workbench-acceptance-playbook.html"):
            self.assertIn(text,html)
        self.assertNotIn("drive.google.com/file/d/",html)
        self.assertNotIn("dev438211.service-now.com",html)
        self.assertNotIn("<img",html.lower())

    def test_script_is_offline_and_never_promotes_status(self):
        js=JS.read_text(encoding="utf-8")
        for text in ("MOCK-ONLY","NOT RUN","NOT VERIFIED","HOLD","wrote_records:false",
                     "checked_native_permissions:false","textContent","replaceChildren"):
            self.assertIn(text,js)
        for prohibited in ("fetch(","XMLHttpRequest","WebSocket","sendBeacon",
                           "localStorage","sessionStorage","document.cookie","eval("):
            self.assertNotIn(prohibited,js)

    @unittest.skipUnless(shutil.which("node"), "Node not installed; HTML/JS static checks remain")
    def test_synthetic_scenarios_fail_closed_and_export_hold(self):
        code=r"""
const assert=require('node:assert/strict');
const {states,evaluate}=require('./handoff-contract-engine.js');
assert.equal(Object.keys(states).length,8);
const outcome=key=>evaluate(states[key]);
assert.match(outcome('ready').outcome,/DRAFT ELIGIBLE/);
assert.match(outcome('review').outcome,/HOLD/);
assert.match(outcome('version').outcome,/REJECT/);
assert.match(outcome('evidence').outcome,/HOLD/);
assert.match(outcome('role').outcome,/REJECT/);
assert.match(outcome('scope').outcome,/MANUAL/);
assert.match(outcome('conflict').outcome,/HOLD/);
assert.match(outcome('replay').outcome,/REUSE/);
for(const fixture of Object.values(states)){
 const result=evaluate(fixture);
 assert.equal(result.classification,'MOCK-ONLY');
 assert.equal(result.publication_decision,'HOLD');
 assert.equal(result.native_execution,'NOT RUN');
 assert.equal(result.production_verification,'NOT VERIFIED');
 assert.equal(result.wrote_records,false);
 assert.equal(result.checked_native_permissions,false);
}
const compound=evaluate({...states.ready,reviewed:false,replay:true});
assert.match(compound.outcome,/HOLD/); // replay never bypasses unapproved review
const denial=evaluate({...states.ready,authorised:false,replay:true});
assert.match(denial.outcome,/REJECT/); // replay never bypasses role denial
"""
        result=subprocess.run(["node","-e",code],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)

if __name__=="__main__":
    unittest.main()
