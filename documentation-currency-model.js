/* Public, source-document edition crosswalk. Distinct PDF/DOCX editions are NOT interchangeable; no runtime attestation. */
(function(root,factory){const api=factory();if(typeof module==="object"&&module.exports)module.exports=api;else root.DocCurrencyGate=api;})(typeof globalThis!=="undefined"?globalThis:this,function(){
"use strict";
const docs=Object.freeze([
  Object.freeze({id:"ASBUILT-SEP30",name:"Delivery Solution As-Built",edition:"September PDF",format:"PDF",version:"4.6.1",cutoff:"2026-09-30",kind:"CONTROLLED DRAFT",scope:"September lifecycle and handover procedures; historical 4.5.1 DEV boundary",next:"Check target package and reconcile September procedures before use."}),
  Object.freeze({id:"TRAINING-SEP30",name:"Delivery User Guides & Training",edition:"September PDF",format:"PDF",version:"4.6.1",cutoff:"2026-09-30",kind:"CONTROLLED DRAFT",scope:"September persona guides and unfilled live screenshot placeholders",next:"Rehearse procedures against authorised target and collect persona sign-off."}),
  Object.freeze({id:"ASBUILT-OCT19",name:"Delivery Solution As-Built",edition:"October DOCX",format:"DOCX",version:"4.22.2",cutoff:"2026-10-19",kind:"CONTROLLED DRAFT",scope:"October source-defined delivery controls; dated DEV observations are not current target acceptance",next:"Confirm exact target commit, installed package, generated records and authorisation."}),
  Object.freeze({id:"TRAINING-OCT19",name:"Delivery User Guides & Training",edition:"October DOCX",format:"DOCX",version:"4.22.2",cutoff:"2026-10-19",kind:"CONTROLLED DRAFT",scope:"October role-based guidance, exercises and competency sign-off; visual sign-off not supplied",next:"Revalidate persona permissions and routes; obtain approved screens and trainer sign-off."}),
  Object.freeze({id:"ARCH-OCT19",name:"Delivery Architecture",edition:"October DOCX",format:"DOCX",version:"4.22.2",cutoff:"2026-10-19",kind:"SOURCE/HISTORICAL DEV DOCUMENT",scope:"Source architecture, generated metadata, ACL, integration and transport boundaries",next:"Reconfirm scope, package, roles, dependencies and current authorised DEV read-back."}),
  Object.freeze({id:"DIAG-DEMO",name:"Diagnostic Completion Runbook",edition:"Fictional showcase",format:"DOCX",version:null,cutoff:"historical showcase",kind:"FICTIONAL SHOWCASE RUNBOOK",scope:"Simulated finding-to-delivery reconciliation and non-production release demonstration",next:"Exclude demo approvals from native acceptance; obtain separately authorised real evidence."})
]);
const versions=Object.freeze(["4.6.1","4.22.2"]);
const personas=Object.freeze([
 Object.freeze({id:"presales",label:"Presales & account lead",focus:"Engagement qualification, estimate and proposal baseline",proof:"Authorised target membership, scope and baseline review"}),
 Object.freeze({id:"delivery",label:"Delivery lead",focus:"Guided journey, workshops, decisions and operational ownership",proof:"Linked records, independent approvals and open-exception review"}),
 Object.freeze({id:"architect",label:"Solution architect",focus:"Design decision, build specification and segregation of duties",proof:"Approved decision lineage, no self-approval and tested ACLs"}),
 Object.freeze({id:"test",label:"Test & release lead",focus:"Negative-path tests, defects, release and rollback evidence",proof:"Target-specific test results, approved change and rollback rehearsal"}),
 Object.freeze({id:"platform",label:"Platform owner",focus:"Application identity, source manifest, roles and access",proof:"Current installed version/scope read-back and target entitlements"})
]);

// Role-based native acceptance protocols derived from controlled October As-Built,
// Architecture and User Guides/Training. These are *test designs*, NOT test results.
const protocols=Object.freeze([
  ["PRE-01","presales","Engagement initiation","Create an authorised non-customer engagement and verify named accountable roles and the saved lifecycle reference.","Unauthorised member must not gain access to the engagement.","Training §3–4; As-Built §10","Scoped-app access and membership ACLs"],
  ["PRE-02","presales","Estimate and proposal","Trace a reviewed scope decision through estimate, controlled proposal and recorded client-approval boundary.","A draft or rejected proposal must not masquerade as accepted scope.","Training §4; As-Built §17","Scoped application; document generation entitlement if needed"],
  ["PRE-03","presales","AI consent boundary","Verify explicit AI processing decision and no outbound request before consent or connection authorisation.","Unset consent must not trigger provider processing.","Training §4; Architecture §7–8","AI/Now Assist and external-provider rights if used"],
  ["DEL-01","delivery","Requirements traceability","Trace workshop question through requirement, design decision and owned acceptance criterion.","Unanswered or deferred work cannot satisfy a completed gate.","Training §4; As-Built §5, §17","Custom scoped application hosting"],
  ["DEL-02","delivery","Guided stage gates","Confirm saved gate outcomes, owner, evidence references, exception expiry and independent approvals.","Self-approval and expired waivers must not advance the release.","As-Built §10–11; Architecture §8","Roles, ACLs and approval routing"],
  ["DEL-03","delivery","Operational handover","Review as-built, runbook, training and business/technical/operations acceptance before closure.","Missing handover owner or unresolved high-severity defect blocks closure.","Training §4; As-Built §13, §18","Scoped app roles; optional ITSM if linked"],
  ["ARC-01","architect","Scope and package identity","Read installed app scope, version, selected source/package identity and generated metadata on authorised DEV.","Different app scopes or stale package versions must not be conflated.","Architecture §4–5; As-Built §7","App repository/Now SDK access; deployer permissions"],
  ["ARC-02","architect","Role and ACL segregation","Test scoped-table read/write rights and approval roles using separate least-privilege identities.","Cross-engagement access and self-approval must be rejected.","Architecture §8; As-Built §8","Elevated test identities, roles and ACLs"],
  ["ARC-03","architect","External authority","Trace system-of-record ownership and connection alias use before enabling an integration.","Missing provider permission or contract must leave outbound sync disabled.","Architecture §7, §12–13","IntegrationHub/spokes or provider access only if selected"],
  ["TST-01","test","Acceptance evidence","Run positive and negative persona workflows with dated test IDs, observed outcomes and defect linkage.","Synthetic walkthrough alone must never count as a passed native test.","Training §8–10; As-Built §15","ATF where licensed/available; test-user roles"],
  ["TST-02","test","Transport and rollback","Verify update-set/app package identity, collision checks and a rehearsed rollback under approved change.","Mismatched scope or missing rollback approval blocks promotion.","Architecture §5, §11; As-Built §12, §15","Release/deployer access; Change entitlement if used"],
  ["TST-03","test","Document and privacy output","Exercise controlled Word/HTML generation and inspect redaction, access and approval states.","Unapproved customer data, arbitrary external URLs or disabled exports must not leak.","Training §4, §8; Architecture §8","Scoped document rights; optional third-party renderer"],
  ["PLT-01","platform","Target installation read-back","Capture current installed scope, version, application ID, component state and date; compare with selected document edition.","Historical DEV evidence must not certify a newer or different target.","Architecture §5; As-Built §7, §15","Scoped application administrative/deployer roles"],
  ["PLT-02","platform","Role provisioning and monitoring","Verify role grants, membership filters, event audit, scheduled jobs and support escalation.","An unprivileged account must not see admin operations or other-engagement data.","Architecture §8, §11; As-Built §13","Platform admin/security roles; optional analytics entitlement"],
  ["PLT-03","platform","Entitlement and plugin register","Compare installed capabilities, plugins, integration usage and actual contracted entitlements with signed ownership.","Unlicensed spokes, AI or ITOM collectors cannot be marked available based on source code.","Architecture §12–13; As-Built §9","ITSM/ITOM/AI/IntegrationHub as applicable; contract check"]
].map(([id,persona,capability,expected,negative,source,entitlement])=>
 Object.freeze({id,persona,capability,expected,negative,source,entitlement})));
function protocolRows(target,persona="all"){
 valid(target);
 if(persona!=="all"&&!personas.some(p=>p.id===persona))throw Error("Unsupported protocol persona");
 return protocols.filter(p=>persona==="all"||p.persona===persona).map(p=>Object.freeze({
  ...p,referenceRelease:target,classification:"SOURCE-ONLY",execution:"NOT RUN",
  approval:"HOLD",production:"NOT VERIFIED",screenshot:"NOT AUTHORISED"
 }));
}
function protocolCsv(target,persona="all"){
 const headers=["Control ID","Persona","Capability","Reference snapshot","Source section","Expected positive observation","Required negative control","Entitlement review","Evidence class","Native execution","Approval","Production","Screenshot"];
 const rows=protocolRows(target,persona).map(p=>[p.id,p.persona,p.capability,p.referenceRelease,p.source,p.expected,p.negative,p.entitlement,p.classification,p.execution,p.approval,p.production,p.screenshot]);
 const escape=value=>'"'+String(value).replace(/"/g,'""').replace(/^([=+\-@\t\r])/,"'$1")+'"';
 return [headers,...rows].map(row=>row.map(escape).join(",")).join("\r\n")+"\r\n";
}

function valid(target){if(!versions.includes(target))throw Error("Unsupported evidence target: choose a controlled snapshot.");}
function rows(target){valid(target);return docs.map(d=>Object.freeze({...d,alignment:d.version===null?"UNVERSIONED / SHOWCASE":d.version===target?"SNAPSHOT MATCH":"DOCUMENT DRIFT",decision:"HOLD",nativeVerification:"NOT RUN",publication:"NOT AUTHORISED"}));}
function training(target,id){valid(target);const persona=personas.find(p=>p.id===id);if(!persona)throw Error("Unsupported training persona");const edition=target==="4.22.2"?"October DOCX":"September PDF";return Object.freeze({...persona,edition,release:target,action:"Rehearse on authorised target, capture observed result and obtain independent reviewer approval.",nativeVerification:"NOT RUN",decision:"HOLD"});}
function csv(target){const fields=["Doc ID","Controlled document","Edition","Format","Snapshot","Evidence cutoff","Target","Comparison","Native acceptance","Decision","Next evidence action"];const records=rows(target).map(d=>[d.id,d.name,d.edition,d.format,d.version||"none",d.cutoff,target,d.alignment,d.nativeVerification,d.decision,d.next]);const esc=v=>'"'+String(v).replace(/"/g,'""').replace(/^([=+\-@\t\r])/,"'$1")+'"';return [fields,...records].map(row=>row.map(esc).join(",")).join("\r\n")+"\r\n";}
return Object.freeze({docs,versions,personas,protocols,protocolRows,protocolCsv,rows,training,csv});
});