/* Offline CMDB Health assurance lab. Synthetic fixtures; no ServiceNow connection.
   Rendered percentages are fixture labels, NOT native CMDB Health calculations. */
(function(root,make){
  "use strict";
  const api=make();
  if(typeof module==="object" && module.exports) module.exports=api;
  root.CMDBHealthAssurance=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  const scenarios=Object.freeze([
    Object.freeze({id:"jobs",tag:"01 / Completeness",label:"Silent score: scheduled job inactive",
      className:"cmdb_ci_server",score:"—",population:"1,240 synthetic CIs",job:"Inactive",
      problem:"A populated health tile looks trustworthy, but the completeness collection job is inactive. An older result cannot describe today's CI population.",
      recommendation:"HOLD the score. Identify class scope, capture the job's configuration and last successful run, and compare freshness after an authorised non-production execution.",
      risk:["Completeness job not evidenced as active","Last successful run and denominator unknown","Required and recommended-field definitions not confirmed"],
      theme:"Completeness",evidence:"Scheduled job configuration, class scope, rule snapshot, run timestamp and before/after result"}),
    Object.freeze({id:"duplicate",tag:"02 / Correctness",label:"Duplicates: identity conflict",
      className:"cmdb_ci_computer",score:"71%",population:"920 synthetic CIs",job:"Reported / unverified",
      problem:"Two synthetic discovery feeds appear to create the same server. A good-looking overall health number can obscure duplicate, stale and orphan-rule failures.",
      recommendation:"HOLD remediation. Review identifiers, IRE source authority and class rules; run preview and negative-persona checks before any merge or deletion.",
      risk:["Identification-rule behaviour not proven","Competing source precedence unresolved","Duplicate resolution and negative ACL test not executed"],
      theme:"Correctness",evidence:"IRE preview results, duplicate rule findings, CI lineage, ACL denial and independent disposition review"}),
    Object.freeze({id:"audit",tag:"03 / Compliance",label:"Compliance: audit scope drift",
      className:"cmdb_ci_service",score:"86%",population:"360 synthetic CIs",job:"Reported / unverified",
      problem:"A service CI health headline improves after a class filter change, even though the audit policy and affected CI population have not been reconciled.",
      recommendation:"HOLD the trend. Version the audit/certification definitions and class filters, compare tested populations and re-run accepted control samples.",
      risk:["Audit definition and scope versions missing","Historical and current denominators differ","Failed-control ownership and exceptions not reconciled"],
      theme:"Compliance",evidence:"Audit/certification rule revision, evaluated CI list, exception owner, rerun receipt and reviewer sign-off"}),
    Object.freeze({id:"relationship",tag:"04 / Relationships",label:"Relationships: incomplete coverage",
      className:"cmdb_rel_ci",score:"64%",population:"2,100 synthetic links",job:"Reported / unverified",
      problem:"A relationship score looks precise, yet suggested relationships and hosting/containment compliance were not checked against the service model or processor schedule.",
      recommendation:"HOLD the release decision. Confirm relationship rules, scheduled calculations, service impact and whether a metric failure cap stopped the cycle.",
      risk:["Relationship processor execution not evidenced","Rule and suggested-relationship context missing","Calculation completion and failure-cap status unknown"],
      theme:"Relationship health",evidence:"Relationship/processor job receipts, rule version, class/service coverage, capped metrics and owner review"})
  ]);
  const definitions=[
    ["jobs","CH-JOB",[
      ["Inspect baseline jobs and role","sn_cmdb_admin or admin reads scheduled jobs without editing scripts"],
      ["Verify metric schedule and execution","Relevant completeness calculation job is active and has an appropriate successful run"],
      ["Confirm class and field criteria","Required/recommended fields and evaluated class population independently recorded"],
      ["Reconcile score freshness","Dashboard drill-down and calculation timestamp match the accepted run"],
      ["Negative-persona schedule access","Unentitled user cannot enable, alter or execute the CMDB Health job"],
      ["Owner signs off the run","Evidence and next-run ownership accepted without treating this offline lab as execution"]]],
    ["duplicate","CH-COR",[
      ["Inspect correctness metric definitions","Duplicate, stale and orphan rules and effective class scope recorded"],
      ["Run bounded duplicate preview","Identification-rule preview demonstrates the conflict without writing production CIs"],
      ["Validate reconciliation ownership","Authoritative source and allowed attributes checked by an authorised role"],
      ["Compare health drill-down","Duplicate findings trace to affected CIs with timestamps and a controlled denominator"],
      ["Deny unauthorised resolution","Negative-persona test denies CI consolidation, deletion and rule modification"],
      ["Reconcile post-fix signals","After authorised DEV remediation, rerun and independently review affected CIs"]]],
    ["audit","CH-COM",[
      ["Snapshot compliance definitions","Effective audit/certification criteria and revision are preserved"],
      ["Pin class and service population","Included/excluded CI counts and service boundary independently reconciled"],
      ["Reproduce the baseline result","Job run receipt and compliance metric drill-down use the same scope"],
      ["Trace exception disposition","Noncompliant CI owners, follow-up tasks and permitted waivers evidenced"],
      ["Exercise ACL negative case","Unentitled persona cannot edit audit rules or evidence dispositions"],
      ["Compare before and after","Scope-normalised results and an independent reviewer determine actual improvement"]]],
    ["relationship","CH-REL",[
      ["Read relationship health configuration","Suggested, hosting and containment criteria plus eligible CI classes recorded"],
      ["Check relationship calculation jobs","Relationship calculation and compliance processor state and timing confirmed"],
      ["Inspect orphan/duplicate links","Representative failed relationships traced to parent/child CIs and owners"],
      ["Check calculation completion","Any cap, aborted collection or incomplete run is explicitly reported"],
      ["Reject unentitled edits","Negative persona cannot alter relationship rules or protected CI links"],
      ["Approve service impact reconciliation","Service owner and reviewer accept corrected link scope and rerun evidence"]]]
  ];
  const gates=Object.freeze(definitions.flatMap(function(d){return d[2].map(function(item,i){
    return Object.freeze({id:d[1]+"-"+String(i+1).padStart(2,"0"),scenario:d[0],action:item[0],expected:item[1]});
  });}));
  const headers=Object.freeze(["Gate ID","Health domain","Native DEV action","Expected private evidence","Execution status","Release decision","Evidence class","Instance","Build version","Executor persona","Executed at","Evidence receipt","Independent reviewer"]);
  function scenario(id){return scenarios.find(x=>x.id===id)||null;}
  function assess(id){const s=scenario(id);if(!s)throw Error("Unknown health scenario");
    return Object.freeze({scenario:s,status:"NOT RUN",decision:"HOLD",evidence:"MOCK-ONLY",risk:s.risk});
  }
  function rows(selector){
    if(selector!=="all"&&!scenario(selector))throw Error("Unknown export selector");
    return gates.filter(g=>selector==="all"||g.scenario===selector).map(g=>[
      g.id,scenario(g.scenario).theme,g.action,g.expected,"NOT RUN","HOLD","MOCK-ONLY","","","","","",""
    ]);
  }
  function quote(v){
    let x=String(v===null||v===undefined?"":v);
    if(/^\s*[=+\-@]/.test(x))x="'"+x;
    return '"'+x.replace(/"/g,'""')+'"';
  }
  function csv(selector){return [headers,...rows(selector)].map(r=>r.map(quote).join(",")).join("\r\n")+"\r\n";}

  // All before/after samples are deliberately synthetic passing fractions,
  // NOT native ServiceNow CMDB Health scores or job outputs.
  const cohortScenarios=Object.freeze([
    Object.freeze({id:"remediated",label:"Controlled remediation",brief:"The same fictional CI cohort and rule definition are used on two completed runs.",
      before:Object.freeze({passing:700,total:1000,cohort:"sample-cohort-a",rules:"sample-rules-v1",completed:true,run:"2026-11-01T09:00:00Z"}),
      after:Object.freeze({passing:820,total:1000,cohort:"sample-cohort-a",rules:"sample-rules-v1",completed:true,run:"2026-11-02T09:00:00Z"}),
      finding:"The illustrative fraction improves with matching scope and rule labels. Real DEV receipts and reviewer approval are still missing."}),
    Object.freeze({id:"denominator",label:"Denominator shrinkage",brief:"The fictional passing count is unchanged, but excluded CIs make the percentage appear stronger.",
      before:Object.freeze({passing:700,total:1000,cohort:"sample-cohort-a",rules:"sample-rules-v1",completed:true,run:"2026-11-01T09:00:00Z"}),
      after:Object.freeze({passing:700,total:800,cohort:"sample-cohort-b",rules:"sample-rules-v1",completed:true,run:"2026-11-02T09:00:00Z"}),
      finding:"A higher fraction caused by excluding 200 sample CIs is not evidence of corrected configuration data."}),
    Object.freeze({id:"rule-change",label:"Metric definition changed",brief:"The fictional CI set is the same but the acceptance rule changed between runs.",
      before:Object.freeze({passing:700,total:1000,cohort:"sample-cohort-a",rules:"sample-rules-v1",completed:true,run:"2026-11-01T09:00:00Z"}),
      after:Object.freeze({passing:850,total:1000,cohort:"sample-cohort-a",rules:"sample-rules-v2",completed:true,run:"2026-11-02T09:00:00Z"}),
      finding:"A rule revision breaks simple trend comparison even when the denominator happens to match."}),
    Object.freeze({id:"incomplete",label:"Incomplete calculation",brief:"The second fictional calculation has no completed-run receipt.",
      before:Object.freeze({passing:700,total:1000,cohort:"sample-cohort-a",rules:"sample-rules-v1",completed:true,run:"2026-11-01T09:00:00Z"}),
      after:Object.freeze({passing:820,total:1000,cohort:"sample-cohort-a",rules:"sample-rules-v1",completed:false,run:""}),
      finding:"A percentage without a completed job cannot be used as a fresh, accepted health trend."})
  ]);
  function sampleFraction(sample){
    if(!sample||!Number.isSafeInteger(sample.passing)||!Number.isSafeInteger(sample.total)||
      sample.total<=0||sample.passing<0||sample.passing>sample.total)throw Error("Invalid synthetic cohort counts");
    return Math.round(1000*sample.passing/sample.total)/10;
  }
  function compareCohort(id){
    const fixture=cohortScenarios.find(s=>s.id===id);
    if(!fixture)throw Error("Unknown comparison fixture");
    const a=fixture.before,b=fixture.after,problems=[];
    const prior=sampleFraction(a),next=sampleFraction(b);
    if(a.total!==b.total)problems.push("Denominator changed: "+a.total+" to "+b.total+" sample CIs");
    if(a.cohort!==b.cohort)problems.push("CI cohort membership token changed");
    if(a.rules!==b.rules)problems.push("Metric rule version changed");
    if(!a.completed||!b.completed||!a.run||!b.run)problems.push("A completed calculation receipt is missing");
    if(a.run&&b.run&&(!Number.isFinite(Date.parse(a.run))||!Number.isFinite(Date.parse(b.run))||Date.parse(b.run)<=Date.parse(a.run)))
      problems.push("Calculation timestamps do not establish chronological completion");
    return Object.freeze({fixture,before:prior,after:next,delta:Math.round((next-prior)*10)/10,
      comparable:problems.length===0,
      reasons:Object.freeze(problems.length?problems:["Synthetic scope, rule and completed-run markers match; real CI membership and job receipts still require DEV proof"]),
      evidence:"MOCK-ONLY",nativeStatus:"NOT RUN",releaseDecision:"HOLD"});
  }
  const cohortCsvHeaders=Object.freeze(["Synthetic scenario","Before passing","Before population","After passing","After population",
    "Illustrative before %","Illustrative after %","Illustrative change (pp)","Like-for-like inputs","Reason","Native execution","Release decision","Evidence classification"]);
  function cohortCsv(){
    const data=cohortScenarios.map(function(s){
      const result=compareCohort(s.id);return [s.label,s.before.passing,s.before.total,s.after.passing,s.after.total,
        result.before,result.after,result.delta,result.comparable?"SYNTHETIC MATCH":"NO",
        result.reasons.join("; "),result.nativeStatus,result.releaseDecision,result.evidence];
    });
    return [cohortCsvHeaders,...data].map(r=>r.map(quote).join(",")).join("\r\n")+"\r\n";
  }
  return Object.freeze({scenarios,gates,headers,scenario,assess,rows,csv,cohortScenarios,compareCohort,cohortCsv,cohortCsvHeaders});
});