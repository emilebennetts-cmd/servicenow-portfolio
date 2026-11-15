/* CMDB Data Manager governance lab — synthetic planning data only.
 * No instance connection, credentials, native writes, or certification logic.
 */
(function(root, make) {
  "use strict";
  var api = make();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CMDBPolicyLab = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function() {
  "use strict";
  var scenarios = Object.freeze([
    Object.freeze({
      id:"retire", label:"Retire an inactive server",
      story:"A discovery-managed server has been marked for retirement, but a still-active source could repopulate operational fields.",
      policy:"Retire", className:"cmdb_ci_server", ownerKnown:true,
      retirementDefinitionActive:true, retired:false, legalHold:false,
      dependentReview:true, exclusionChecked:true, retentionDays:0,
      sourceRefreshRisk:true, approvalPath:true
    }),
    Object.freeze({
      id:"archive", label:"Archive a retired CI",
      story:"A retired infrastructure CI is a candidate for temporary archiving after dependency and record-retention checks.",
      policy:"Archive", className:"cmdb_ci_server", ownerKnown:true,
      retirementDefinitionActive:true, retired:true, legalHold:false,
      dependentReview:true, exclusionChecked:true, retentionDays:120,
      sourceRefreshRisk:false, approvalPath:true
    }),
    Object.freeze({
      id:"delete", label:"Delete a legally held CI",
      story:"A retired CI falls within a cleanup filter but is subject to a records-preservation hold.",
      policy:"Delete", className:"cmdb_ci_server", ownerKnown:true,
      retirementDefinitionActive:true, retired:true, legalHold:true,
      dependentReview:true, exclusionChecked:true, retentionDays:0,
      sourceRefreshRisk:false, approvalPath:true
    }),
    Object.freeze({
      id:"attest", label:"Attest an unowned CI",
      story:"A CI may still be in service but has no accountable managed-by assignment.",
      policy:"Attestation", className:"cmdb_ci_computer", ownerKnown:false,
      retirementDefinitionActive:false, retired:false, legalHold:false,
      dependentReview:false, exclusionChecked:false, retentionDays:0,
      sourceRefreshRisk:false, approvalPath:false
    })
  ]);
  var checks = Object.freeze([
    ["DM-RET-01","retire","Confirm active class retirement definition","Class-specific active retirement definition and inheritance inspected"],
    ["DM-RET-02","retire","Preview CI conditions and exclusions","Target candidate set, class and exclusions reviewed without publishing"],
    ["DM-RET-03","retire","Trace discovery and source reactivation risk","Source reconciliation, last-seen signal and re-ingestion risk assessed"],
    ["DM-RET-04","retire","Validate task owner and approval separation","Assignment group, fulfiller permissions and approver roles evidenced"],
    ["DM-RET-05","retire","Check dependent CIs and rollback plan","Dependency ownership, cascades, monitoring and reversal path reviewed"],
    ["DM-ARC-01","archive","Verify retired state and definition","All selected CIs already retired under active class definition"],
    ["DM-ARC-02","archive","Confirm retention authority and recovery window","Approved retention duration and restore responsibility recorded"],
    ["DM-ARC-03","archive","Review CI relationships and exclusions","Dependent CIs, relationship impact and excluded records assessed"],
    ["DM-ARC-04","archive","Exercise negative-persona approval access","Unauthorised persona cannot approve or execute the policy task"],
    ["DM-ARC-05","archive","Reconcile archived records and task batches","Task counts, batches and retrieval test independently read back"],
    ["DM-DEL-01","delete","Check legal hold and signed disposition","Preservation holds and records-management authorisation validated"],
    ["DM-DEL-02","delete","Validate retired state and exclusions","Target remains retired and excluded CIs are not selected"],
    ["DM-DEL-03","delete","Review irreversible deletion and dependencies","Impact on mapped services, downstream references and fallback evidenced"],
    ["DM-DEL-04","delete","Confirm approvals and administrative boundaries","Different maker, checker and executor personas verified"],
    ["DM-DEL-05","delete","Reconcile task and post-delete state","Native task audit, CI absence and exceptions independently recorded"],
    ["DM-ATT-01","attest","Identify accountable owner or escalation","Managed-by assignment and missing-owner exception resolved"],
    ["DM-ATT-02","attest","Validate source authority and observation age","Reconciliation source, data timestamp and owner challenge checked"],
    ["DM-ATT-03","attest","Inspect attestation field configuration","Certified fields, display fields and permitted updates confirmed"],
    ["DM-ATT-04","attest","Test negative-persona CI update denial","Unentitled user cannot change certified attributes"],
    ["DM-ATT-05","attest","Review rejected and stale task routing","Rejection, task ageing, reassignment and evidence tracked"]
  ].map(function(item){return Object.freeze({id:item[0],scenario:item[1],step:item[2],evidence:item[3]});}));
  var headers=Object.freeze(["Control ID","Policy type","Native DEV action","Expected private evidence","Execution status","Release decision","Evidence class","Instance","Installed version","Executor role","Executed at","Evidence receipt","Independent reviewer"]);
  function getScenario(id) {return scenarios.find(function(s){return s.id===id;}) || null;}
  function assess(id) {
    var s=getScenario(id);
    if (!s) throw new Error("Unknown scenario");
    var blockers=[], review=[];
    if (!s.ownerKnown) blockers.push("Accountable task owner is missing");
    if ((s.policy==="Retire" || s.policy==="Archive" || s.policy==="Delete") && !s.retirementDefinitionActive) blockers.push("Active class retirement definition not confirmed");
    if ((s.policy==="Archive" || s.policy==="Delete") && !s.retired) blockers.push("CI is not in the retired state");
    if (s.legalHold && (s.policy==="Archive" || s.policy==="Delete")) blockers.push("Records preservation hold prevents disposition");
    if ((s.policy==="Archive" || s.policy==="Delete") && !s.exclusionChecked) blockers.push("Exclusion list not reviewed");
    if ((s.policy==="Archive" || s.policy==="Delete") && !s.dependentReview) blockers.push("Dependent CI impact not assessed");
    if (s.policy==="Archive" && !(s.retentionDays>0)) blockers.push("Positive retention window not recorded");
    if (s.sourceRefreshRisk) blockers.push("Re-ingestion could reverse the state change");
    if (!s.approvalPath) blockers.push("Approval/assignment route not evidenced");
    review.push("Execute native preview and negative-persona tests in authorised DEV");
    review.push("Independently review signed approval, scope version and instance evidence");
    if (s.policy==="Delete") review.push("Deletion is irreversible in the active CMDB; require records-management sign-off");
    return Object.freeze({scenario:s,readiness:blockers.length?"HOLD":"REVIEW REQUIRED",blockers:blockers,review:review,evidenceClass:"MOCK-ONLY",nativeStatus:"NOT RUN"});
  }
  function rows(selector) {
    if (selector!=="all" && !getScenario(selector)) throw new Error("Unknown export scenario");
    return checks.filter(function(c){return selector==="all"||c.scenario===selector;}).map(function(c) {
      return [c.id, getScenario(c.scenario).policy, c.step, c.evidence,"NOT RUN","HOLD","MOCK-ONLY","","","","","",""];
    });
  }
  function cell(value) {
    var x=String(value===null||value===undefined?"":value);
    // Prevent office-spreadsheet formula execution if future labels are ever externally supplied.
    if (/^[\s]*[=+\-@]/.test(x)) x="'"+x;
    return '"'+x.replace(/"/g,'""')+'"';
  }
  function toCsv(selector) {
    return [headers].concat(rows(selector)).map(function(row){return row.map(cell).join(",");}).join("\r\n")+"\r\n";
  }
  return Object.freeze({scenarios:scenarios,checks:checks,headers:headers,getScenario:getScenario,assess:assess,rows:rows,toCsv:toCsv});
});
