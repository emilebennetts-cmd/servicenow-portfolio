"use strict";
const test=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const tower=require("../cmdb-assurance-control-tower.js");
const deps={ire:require("../cmdb-source-acceptance.js"),tags:require("../cmdb-tag-governance-model.js"),health:require("../cmdb-health-assurance-model.js"),relationships:require("../cmdb-relationship-assurance-model.js"),lifecycle:require("../cmdb-data-manager-policy-model.js")};
test("117 source-defined native prompts retain independent IDs and immutable HOLD results",()=>{
 const rows=tower.createRows(deps);
 assert.equal(rows.length,117);
 assert.equal(new Set(rows.map(r=>r.key+":"+r.id)).size,117);
 for(const [key,n] of Object.entries(tower.EXPECTED))assert.equal(rows.filter(r=>r.key===key).length,n);
 for(const row of rows){assert.equal(row.native,"NOT RUN");assert.equal(row.decision,"HOLD");assert.equal(row.evidence,"MOCK-ONLY");}
});
test("filtering does not promote native evidence",()=>{
 const rows=tower.createRows(deps);
 assert.equal(tower.filterRows(rows,"identity","").length,18);
 assert.equal(tower.filterRows(rows,"tags","").length,25);
 assert.equal(tower.filterRows(rows,"all","").length,117);
 assert.equal(tower.filterRows(rows,"all","zznotmatched").length,0);
 assert.throws(()=>tower.filterRows(rows,"unknown",""),/Unknown workstream/);
});
test("all 117 CSV rows remain NOT RUN/HOLD and receipts blank",()=>{
 const data=tower.csv(tower.createRows(deps));
 assert.equal(data.split("\r\n").filter(Boolean).length,118);
 assert.equal((data.match(/"NOT RUN","HOLD","MOCK-ONLY"/g)||[]).length,117);
 assert.doesNotMatch(data,/bearer\s|password|dev[0-9]+\.service-now|@gmail/i);
 const formula=tower.csv([{key:"identity",id:"=1+2",scenario:"",action:"test",expected:"expected"}]);
 assert.match(formula,/"'=1\+2"/);
});
test("source drift or missing models fails closed",()=>{
 assert.throws(()=>tower.createRows({...deps,ire:null}),/Missing source model/);
 assert.throws(()=>tower.createRows({...deps,tags:{gates:[]}}),/count drift/);
 assert.throws(()=>tower.createRows({...deps,health:{gates:[...deps.health.gates,deps.health.gates[0]]}}),/count drift/);
});
test("responsive page uses local assets and discloses licence and evidence",()=>{
 const html=fs.readFileSync(path.join(__dirname,"..","cmdb-assurance-control-tower.html"),"utf8");
 for(const token of ["117 native","NOT RUN / HOLD","DEV-VERIFIED 0","PRODUCTION-VERIFIED 0","no ServiceNow licence","Service Mapping","Data Manager","MOCK-ONLY","data-tower-export=\"all\""])assert.ok(html.toLowerCase().includes(token.toLowerCase()),token);
 assert.match(html,/connect-src 'none'/);
 assert.match(html,/@media\(max-width:600px\)/);
 assert.doesNotMatch(html,/<img\b|<iframe\b|localStorage|sessionStorage|XMLHttpRequest/i);
});

test("native execution sequence binds all five source models without inventing approvals",()=>{
 const rows=tower.createRows(deps),planned=tower.planRows(rows);
 assert.equal(planned.length,117);
 assert.deepEqual(tower.STAGES.map(s=>s.key),["identity","tags","health","relationships","lifecycle"]);
 assert.deepEqual(tower.STAGES.map(s=>planned.filter(r=>r.key===s.key).length),[18,25,24,30,20]);
 assert.deepEqual([...new Set(planned.map(r=>r.step))],[1,2,3,4,5]);
 for(const r of planned){
   assert.ok(r.entry&&r.dependency&&r.owner&&r.exit&&r.action&&r.expected);
   assert.equal(r.native,"NOT RUN");assert.equal(r.decision,"HOLD");assert.equal(r.evidence,"MOCK-ONLY");
 }
 assert.throws(()=>tower.planRows(rows.slice(1)),/requires all 117/);
 assert.throws(()=>tower.planRows(rows.map((r,i)=>i? r : {...r,native:"PASSED"})),/HOLD/);
 assert.throws(()=>tower.planRows(rows.map((r,i)=>i? r : {...r,id:rows[1].id})),/HOLD/);
});
test("sequenced CSV preserves receipt blanks, formula protection and native HOLD claims",()=>{
 const rows=tower.createRows(deps);
 const output=tower.planCsv(rows);
 assert.equal(output.split("\r\n").filter(Boolean).length,118);
 assert.equal((output.match(/"NOT RUN","HOLD","MOCK-ONLY"/g)||[]).length,117);
 assert.match(output,/"1 \/ CI identity and source precedence"/);
 assert.match(output,/"5 \/ Data Manager lifecycle and attestation"/);
 assert.doesNotMatch(output,/bearer\s|password|@gmail|dev[0-9]+\.service-now/i);
 const html=fs.readFileSync(path.join(__dirname,"..","cmdb-assurance-control-tower.html"),"utf8");
 for(const token of ["id=\"native-execution-plan\"","id=\"tower-plan-export\"","id=\"tower-plan-status\"","STAGE 5","approval","NOT RUN"]){assert.ok(html.includes(token),token);}
});
