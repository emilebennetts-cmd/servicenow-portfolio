/* SOURCE-ONLY consultative model. Synthetic data only; NOT a ServiceNow runtime control. */
(function(root,factory){
  const api=factory();
  if(typeof module==="object" && module.exports) module.exports=api;
  if(root) root.CMDBOwnerGate=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  const REVIEW_DAYS=90; // Illustrative local policy, NOT a ServiceNow default.
  const GATES=Object.freeze([
    {id:"business_owner",title:"Accountable business owner",action:"Assign and attest an accountable business owner with an approved role mapping."},
    {id:"support_owner",title:"Operational support ownership",action:"Resolve support group accountability and on-call ownership."},
    {id:"criticality",title:"Business criticality rationale",action:"Obtain documented criticality and impact approval from the service owner."},
    {id:"source_authority",title:"Authoritative source reconciliation",action:"Resolve source precedence and conflicting owners before any update."},
    {id:"recency",title:"Attestation currency",action:"Re-attest within the organisation's approved policy window."},
    {id:"independent_review",title:"Independent review boundary",action:"Secure an independent evidence reviewer and record the decision separately."}
  ]);
  const CASES=Object.freeze([
    {id:"missing-owner",title:"Orphaned application",caption:"Asset has a service mapping but no named accountability.",flags:[false,false,true,true,true,false],days:24},
    {id:"source-conflict",title:"Competing discovery sources",caption:"Two reconciled feeds report different owners.",flags:[true,true,true,false,true,true],days:12},
    {id:"stale-attestation",title:"Unrevisited ownership",caption:"Historical approval exists but exceeds the sample review interval.",flags:[true,true,true,true,false,true],days:196},
    {id:"criticality-gap",title:"Impact not agreed",caption:"Operational support is known; business impact tier is unapproved.",flags:[true,true,false,true,true,true],days:19},
    {id:"self-approval",title:"Separation-of-duties failure",caption:"The same accountable party is marked as the evidence reviewer.",flags:[true,true,true,true,true,false],days:13},
    {id:"ready-candidate",title:"Reviewed candidate",caption:"All six example prerequisites are satisfied; native verification is still outstanding.",flags:[true,true,true,true,true,true],days:28}
  ]);
  function evaluate(id){
    const item=CASES.find(c=>c.id===id);
    if(!item) throw new TypeError("Unknown synthetic scenario");
    if(item.flags.length!==GATES.length || item.flags.some(f=>typeof f!=="boolean") ||
      !Number.isSafeInteger(item.days) || item.days<0) throw new TypeError("Invalid scenario");
    const controls=GATES.map((g,i)=>({
      id:g.id,title:g.title,action:g.action,
      passed:g.id==="recency" ? (item.flags[i] && item.days<=REVIEW_DAYS) : item.flags[i],
      disposition:(g.id==="recency" ? item.flags[i] && item.days<=REVIEW_DAYS : item.flags[i])?"SIMULATED READY":"REQUIRES REVIEW"
    }));
    const open=controls.filter(g=>!g.passed);
    return Object.freeze({
      id:item.id,title:item.title,caption:item.caption,days:item.days,
      controls,ready:open.length===0,
      result:open.length===0?"CANDIDATE FOR NATIVE REVIEW":"HOLD — REMEDIATE",
      reason:open.length===0?"This synthetic record may enter a separately authorised native test. No approval is granted.":open.map(x=>x.title).join("; "),
      evidenceClass:"MOCK-ONLY",nativeStatus:"NOT RUN",releaseStatus:"HOLD"
    });
  }
  function escapeCell(value){
    let s=String(value);
    if(/^[\s]*[=+\-@]/.test(s)) s="'"+s;
    return '"'+s.replace(/"/g,'""')+'"';
  }
  function toCSV(id){
    const v=evaluate(id);
    const head=["scenario","gate_id","gate","simulated_disposition","required_action","evidence_class","native_status","release_status"];
    const rows=v.controls.map(x=>[v.id,x.id,x.title,x.disposition,x.action,"MOCK-ONLY","NOT RUN","HOLD"]);
    return [head,...rows].map(r=>r.map(escapeCell).join(",")).join("\r\n")+"\r\n";
  }
  return Object.freeze({REVIEW_DAYS,GATES,CASES,evaluate,toCSV});
});
