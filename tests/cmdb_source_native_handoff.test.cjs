'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {columns,scenarioLabels,buildRows,toCsv}=require('../cmdb-source-acceptance.js');
const page=fs.readFileSync(path.join(__dirname,'../cmdb-source-onboarding-lab.html'),'utf8');
test('18 stable synthetic acceptance IDs and six cases per path',()=>{
 const rows=buildRows('all');
 assert.equal(rows.length,18);
 assert.equal(new Set(rows.map(r=>r.test_id)).size,18);
 for(const key of Object.keys(scenarioLabels)) assert.equal(buildRows(key).length,6);
 assert.throws(()=>buildRows('production'),/Unknown synthetic scenario/);
});
test('native and approval claims are always HOLD, even after exporting any path',()=>{
 for(const key of ['all',...Object.keys(scenarioLabels)]){
  for(const r of buildRows(key)){
    assert.equal(r.execution_status,'NOT RUN');
    assert.equal(r.release_decision,'HOLD');
    assert.equal(r.classification,'MOCK-ONLY');
    for(const col of ['instance','installed_scope_version','executor_role','execution_utc','private_evidence_receipt','independent_reviewer']) assert.equal(r[col],'');
    assert.equal(Object.keys(r).length,columns.length);
  }
 }
});
test('RFC4180-compatible CSV quotes and does not spill real values',()=>{
 const csv=toCsv('all');
 assert.equal(csv.trim().split('\r\n').length,19);
 assert.equal(csv.split('\r\n')[0],columns.join(','));
 assert.match(csv,/"NOT RUN","HOLD","MOCK-ONLY","",/);
 assert.doesNotMatch(csv,/dev438211|x_1577958|password|credential|Bearer /i);
});
test('new public controls are labeled as a non-certifying offline handoff',()=>{
 assert.match(page,/id="native-matrix-all"/);
 assert.match(page,/id="native-matrix-selected"/);
 assert.match(page,/cmdb-source-acceptance\.js/);
 assert.match(page,/18 native checks/i);
 assert.match(page,/NOT RUN \/ HOLD/);
 assert.match(page,/no ServiceNow write/i);
});
