/* Browser-local ServiceNow Request Management design rehearsal; no instance calls. */
(function(root) {
"use strict";
const controls = {
access: {
title:"Application access",
description:"Conditional manager and application-owner approval before a least-privilege access task.",
gates:[
["ACC-01","Define a supported catalogue item","Read back the item identity, owner, category and active state."],
["ACC-02","Enforce requester eligibility","Verify user criteria for permitted and denied personas, then assess record ACLs."],
["ACC-03","Require an accountable approver","Confirm conditional manager/application-owner approval route and separation of duties."],
["ACC-04","Reject and stop cleanly","Reject approval as a negative persona; no unintended fulfilment task may proceed."],
["ACC-05","Preserve REQ and RITM linkage","Inspect native request and requested-item identity, variables and record audit."],
["ACC-06","Assign fulfilment accurately","Confirm a single intended catalog task, group assignment and authorised work notes."],
["ACC-07","Close access safely","Validate completed/rejected/cancelled state propagation and requester notification."],
["ACC-08","Retain independent evidence","Store attributable DEV test IDs, source revision, timestamps and reviewer sign-off privately."]]},
hardware:{
title:"Hardware order",
description:"Eligibility, approval, authorised stock/asset fulfilment and reconciled task closure.",
gates:[
["HW-01","Define item and variables","Confirm device variants, quantities, delivery attributes and mandatory validations."],
["HW-02","Restrict catalogue visibility","Verify user criteria and REQ/RITM/task ACLs across positive and denied roles."],
["HW-03","Route purchase authority","Confirm cost and manager approval rules including reject/cancel outcomes."],
["HW-04","Inspect native record hierarchy","Trace submitted REQ, RITM variables and any associated catalog tasks."],
["HW-05","Verify asset entitlement boundary","Check HAM/SAM, stockroom and asset workflows only where deployed and entitled."],
["HW-06","Prevent duplicate fulfilment","Test retry, reassignment and failure/recovery without duplicated catalog tasks."],
["HW-07","Confirm handover and closure","Check receipt evidence, fulfilment ownership, state propagation and notifications."],
["HW-08","Run source-to-instance acceptance","Record approved baseline, synthetic persona outcomes and independent reviewer."]]},
service:{
title:"Standard service",
description:"A repeatable low-risk service with validated eligibility and traceable fulfilment.",
gates:[
["SRV-01","Set service ownership","Identify item owner, fulfilment group, category and service offering where applicable."],
["SRV-02","Minimise and validate inputs","Check mandatory request variables, help text, defaults and privacy boundaries."],
["SRV-03","Protect access by user criteria","Test catalogue eligibility separately from task and request ACL permissions."],
["SRV-04","Select approved fulfilment design","Inspect the associated Service Catalog flow or supported fulfilment process."],
["SRV-05","Verify approval decision","Prove approval is intentional, including a negative path or documented no-approval policy."],
["SRV-06","Trace REQ, RITM and tasks","Confirm stable links, assignments, due dates and auditable work completion."],
["SRV-07","Test exception and closure routes","Exercise cancellation, task failure, rejection, notification and recovery."],
["SRV-08","Collect gated native evidence","Capture synthetic execution receipts and a release-specific independent review."]]}
};
function getScenario(key){return Object.prototype.hasOwnProperty.call(controls,key)?controls[key]:null}
function acceptanceRows(key,readIds){const s=getScenario(key);if(!s)return [];const seen=new Set(readIds||[]);return s.gates.map(g=>({id:g[0],control:g[1],evidence:g[2],read:seen.has(g[0]),native:"NOT RUN",release:"HOLD",classification:"MOCK-ONLY"}))}
function quote(value){return '"'+String(value).replace(/"/g,'""')+'"'}
function acceptanceCsv(key,readIds){const s=getScenario(key);if(!s)return "";const header=["Scenario","Test ID","Acceptance control","Evidence required","Read in rehearsal","Native execution","Release decision","Evidence class"];const rows=acceptanceRows(key,readIds).map(r=>[s.title,r.id,r.control,r.evidence,r.read?"READ":"UNREAD",r.native,r.release,r.classification]);return [header,...rows].map(row=>row.map(quote).join(",")).join("\r\n")+"\r\n"}

/* Unified, private-review-ready handoff: fixed statuses cannot claim native execution. */
function allAcceptanceRows(readByScenario){
 const marks=readByScenario||{};
 return Object.keys(controls).flatMap(key=>acceptanceRows(key,marks[key]||[]).map(row=>({scenario:controls[key].title,...row})));
}
function allAcceptanceCsv(readByScenario){
 const header=["Scenario","Test ID","Acceptance control","Evidence required","Read in rehearsal","Native execution","Release decision","Evidence class","Instance alias (private)","Build version (private)","Executor role (private)","Execution date (private)","Evidence receipt alias (private)","Independent reviewer (private)"];
 const rows=allAcceptanceRows(readByScenario).map(r=>[r.scenario,r.id,r.control,r.evidence,r.read?"READ":"UNREAD",r.native,r.release,r.classification,"","","","","",""]);
 return [header,...rows].map(row=>row.map(quote).join(",")).join("\r\n")+"\r\n";
}
if(typeof module!=="undefined" && module.exports){module.exports={getScenario,acceptanceRows,acceptanceCsv,allAcceptanceRows,allAcceptanceCsv}}
if(typeof document==="undefined")return;
const title=document.getElementById("scenario-title"),desc=document.getElementById("scenario-description"),list=document.getElementById("gates"),progress=document.getElementById("progress");
if(!title||!desc||!list||!progress)return;
let current="access";const read=new Map(Object.keys(controls).map(k=>[k,new Set()]));
const buttons=Array.from(document.querySelectorAll("[data-scenario]"));
function render(){const s=getScenario(current);title.textContent=s.title;desc.textContent=s.description;buttons.forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.scenario===current)));
list.replaceChildren();s.gates.forEach(g=>{const item=document.createElement("li");item.className="gate";
const label=document.createElement("label");const checkbox=document.createElement("input");checkbox.type="checkbox";checkbox.checked=read.get(current).has(g[0]);checkbox.dataset.testId=g[0];
const txt=document.createElement("span");txt.textContent=g[0]+" · "+g[1];label.append(checkbox,txt);
const evidence=document.createElement("p");evidence.textContent=g[2];item.append(label,evidence);list.append(item)});
progress.textContent=read.get(current).size+" of "+s.gates.length+" design gates read · Native acceptance NOT RUN · HOLD";
}
buttons.forEach(button=>button.addEventListener("click",()=>{if(getScenario(button.dataset.scenario)){current=button.dataset.scenario;render()}}));
list.addEventListener("change",event=>{const node=event.target;if(!node||node.type!=="checkbox")return;const code=node.dataset.testId;
if(!getScenario(current).gates.some(g=>g[0]===code))return;if(node.checked)read.get(current).add(code);else read.get(current).delete(code);
progress.textContent=read.get(current).size+" of 8 design gates read · Native acceptance NOT RUN · HOLD"});
document.getElementById("reset").addEventListener("click",()=>{for(const s of read.values())s.clear();render()});
function download(csv,filename){
 const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));
 const a=document.createElement("a");a.href=url;a.download=filename;document.body.append(a);a.click();a.remove();URL.revokeObjectURL(url);
}
document.getElementById("export-all").addEventListener("click",()=>{
 const marks=Object.fromEntries(Array.from(read.entries()).map(([key,values])=>[key,values]));
 download(allAcceptanceCsv(marks),"request-management-24-gates-NOT-RUN-HOLD.csv");
});
document.getElementById("export").addEventListener("click",()=>{
const data=acceptanceCsv(current,read.get(current));if(!data)return;
download(data,"request-management-"+current+"-NOT-RUN-HOLD.csv");
});
render();
})(this);
