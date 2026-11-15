/* Offline native acceptance handoff for the CMDB Source Onboarding Lab.
 * All data is synthetic; acceptance outcomes are immutable NOT RUN / HOLD.
 * No ServiceNow connection, writes, persistence or real identifier values.
 */
(function(root) {
  'use strict';
  const scenarios = Object.freeze({
    stable: [
      ['ST-01','Known CI update','Run no-commit IRE query for approved class and stable native identity','Expected CI match, class and rule trace inspected against target configuration'],
      ['ST-02','Replay and idempotency','Repeat the same synthetic payload via authorised non-production integration','No unexpected additional CI and source provenance maintained'],
      ['ST-03','Class guard','Submit a controlled cross-class identifier collision','Class identification outcome and reject/exception routing inspected'],
      ['ST-04','Dependent identification','Test a fixture requiring a parent/dependent relationship','Dependency rule and resolved target references observed'],
      ['ST-05','Attribute precedence','Attempt lower-priority source update to governed field','Configured reconciliation precedence prevents unintended overwrite'],
      ['ST-06','Denied identity','Repeat a controlled operation using an unauthorised test persona','Native ACL/connector denial and audit evidence observed']
    ],
    collision: [
      ['CO-01','Missing native identity','Preview payload with hostname but no strong native identifier','IRE outcome recorded, no fabricated match on hostname'],
      ['CO-02','Reused hostname','Preview two distinct synthetic CIs sharing a short hostname','Duplicate/match decision evaluated against installed identification rules'],
      ['CO-03','Class mismatch','Compare class mapping under competing discovery sources','Class rule and hierarchy precedence explicitly inspected'],
      ['CO-04','Insert restriction','Exercise source-specific insertion restriction with controlled fixture','Observed create/deny/skip behaviour matches approved policy'],
      ['CO-05','Exception ownership','Route ambiguous identity to steward without automatically merging','Owner, triage path and evidence retention observed'],
      ['CO-06','Correction retest','Repair source-native identity mapping and rerun non-commit query','Before/after rule traces reviewed by independent verifier']
    ],
    attributes: [
      ['AT-01','High-authority update','Submit synthetic field delta from designated authoritative source','Field change and source precedence verified on target'],
      ['AT-02','Lower-authority denial','Submit conflicting delta from lower-priority source','Protected attribute remains unchanged per configured rule'],
      ['AT-03','Null overwrite guard','Preview null/empty payload for governed attribute','Null handling matches configured reconciliation/refresh policy'],
      ['AT-04','Stale data refresh','Exercise controlled last-updated/refresh window boundaries','Refresh authority and source staleness evaluated using target rules'],
      ['AT-05','Partial payload','Preview payload omitting unrelated protected fields','Absent fields are preserved or updated only as documented'],
      ['AT-06','Denied user','Attempt attribute update as unauthorised test persona','ACL/connector boundary denies access; audit event inspected']
    ]
  });
  const scenarioLabels = Object.freeze({stable:'Stable server identifier',collision:'Hostname collision / missing identity',attributes:'Endpoint attribute authority'});
  const columns = Object.freeze(['test_id','scenario','control','native_action','expected_evidence','execution_status','release_decision','classification','instance','installed_scope_version','executor_role','execution_utc','private_evidence_receipt','independent_reviewer']);
  function buildRows(scenario) {
    if (scenario !== 'all' && !Object.prototype.hasOwnProperty.call(scenarios,scenario)) throw new Error('Unknown synthetic scenario');
    const keys=scenario==='all'?Object.keys(scenarios):[scenario];
    return keys.flatMap(key=>scenarios[key].map(test=>({
      test_id:test[0],scenario:scenarioLabels[key],control:test[1],native_action:test[2],expected_evidence:test[3],
      execution_status:'NOT RUN',release_decision:'HOLD',classification:'MOCK-ONLY',
      instance:'',installed_scope_version:'',executor_role:'',execution_utc:'',private_evidence_receipt:'',independent_reviewer:''
    })));
  }
  function csvCell(v) {return '"'+String(v).replace(/"/g,'""')+'"';}
  function toCsv(scenario) {
    return [columns.join(','),...buildRows(scenario).map(row=>columns.map(col=>csvCell(row[col])).join(','))].join('\r\n')+'\r\n';
  }
  const api=Object.freeze({columns,scenarioLabels,buildRows,toCsv});
  if (typeof module!=='undefined' && module.exports) module.exports=api;
  if (typeof document==='undefined') return;
  const all=document.getElementById('native-matrix-all');
  const selected=document.getElementById('native-matrix-selected');
  const selector=document.getElementById('scenario-select');
  const status=document.getElementById('native-matrix-status');
  if (!all || !selected || !selector || !status) return;
  function download(which){
    const rows=buildRows(which);
    const blob=new Blob([toCsv(which)],{type:'text/csv;charset=utf-8'});
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');
    a.href=url;a.download='cmdb-ire-native-handoff-'+which+'-HOLD.csv';
    document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    status.textContent=rows.length+' synthetic test cases exported. All native results remain NOT RUN / HOLD. Fill receipt fields privately after authorised execution.';
  }
  all.addEventListener('click',()=>download('all'));
  selected.addEventListener('click',()=>download(selector.value));
})(typeof globalThis!=='undefined'?globalThis:this);
