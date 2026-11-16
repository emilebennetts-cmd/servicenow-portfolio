"use strict";
const test=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const lab=require("../cmdb-relationship-assurance-model.js");
test("five bounded synthetic topology cases preserve HOLD",()=>{
 assert.equal(lab.scenarios.length,5);
 assert.equal(new Set(lab.scenarios.map(s=>s.id)).size,5);
 for(const s of lab.scenarios){const r=lab.assess(s.id);assert.equal(r.evidence,"MOCK-ONLY");assert.equal(r.native,"NOT RUN");assert.equal(r.release,"HOLD");assert.ok(r.edgeCount>0);}
});
test("duplicate, orphan, stale and invalid direction are distinguishable",()=>{
 for(const [id,kind] of [["duplicate","duplicate"],["orphan","orphan"],["stale","stale"],["direction","governance"]])assert.ok(lab.assess(id).findings.some(x=>x.kind===kind),id);
 assert.equal(lab.assess("baseline").findings.length,0);
 assert.equal(lab.assess("baseline").decision,"REVIEW — NOT APPROVED");
 assert.throws(()=>lab.assess("arbitrary"),/Unknown synthetic/);
});
test("30 native gate IDs are unique and immutable outcomes remain unrun",()=>{
 assert.equal(lab.gates.length,30);assert.equal(new Set(lab.gates.map(g=>g.id)).size,30);
 for(const g of lab.gates){assert.equal(g.status,"NOT RUN");assert.equal(g.decision,"HOLD");assert.equal(g.evidence,"MOCK-ONLY");}
 const all=lab.csv(),selected=lab.csv("orphan");
 assert.equal(all.split("\r\n").filter(Boolean).length,31);
 assert.equal(selected.split("\r\n").filter(Boolean).length,7);
 assert.equal((all.match(/"NOT RUN","HOLD","MOCK-ONLY"/g)||[]).length,30);
 assert.throws(()=>lab.csv("invalid"),/Unknown export/);
 assert.doesNotMatch(all,/https?:|password|token|bearer |dev[0-9]+|@/i);
});
test("public page is responsive, local-only, explicit about evidence and license",()=>{
 const s=fs.readFileSync(path.join(__dirname,"..","cmdb-relationship-assurance-lab.html"),"utf8");
 for(const term of ['data-case="duplicate"','data-case="direction"','data-export="all"','role="status"',"MOCK-ONLY","NOT RUN","PRODUCTION-VERIFIED","cmdb_rel_ci","CI Class Manager","Service Mapping","No licence"])assert.ok(s.includes(term),term);
 assert.match(s,/connect-src 'none'/);assert.match(s,/script-src 'self'/);
 assert.doesNotMatch(s,/<img\b|localStorage|sessionStorage|XMLHttpRequest|<iframe\b/i);
});
