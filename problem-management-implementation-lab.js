/* Problem Management portfolio rehearsal: synthetic UI, no ServiceNow access or storage. */
"use strict";
const SCENARIOS=Object.freeze({
  detect:{title:"Recurring incidents",description:"A triage team groups repeated synthetic incidents around one accountable Problem record and assigns investigation ownership.",flow:["Incident trend","Problem assessment","RCA task","Root cause"],risk:"Never infer a common root cause merely from similar incident symptoms. Confirm CI/service context, duplicate handling and accountable investigation.",gates:[
    ["PR-D01","Problem identification","Verify native Problem record identity, assignment group and accountable coordinator","problem_coordinator"],
    ["PR-D02","Incident association","Link synthetic related incidents and verify they are not incorrectly merged or closed","itil fulfiller"],
    ["PR-D03","CI/service context","Read back impacted configuration item, service and ownership only when CMDB data is trusted","problem_coordinator"],
    ["PR-D04","State-model prerequisite","Identify installed Problem state model and supported transitions for this instance","problem_admin"],
    ["PR-D05","Root-cause assignment","Create a Root Cause Analysis problem task for an appropriate subject-matter group","problem_task_analyst"],
    ["PR-D06","Investigation evidence","Attach synthetic cause notes and observations without customer identifiers or credentials","problem_coordinator"],
    ["PR-D07","Denied persona","A requester without Problem write access cannot edit investigation or assigned tasks","excluded requester"],
    ["PR-D08","Independent receipt","Capture target version, record IDs, positive/negative persona outcomes and reviewer privately","independent reviewer"]
  ]},
  known:{title:"Workaround & known error",description:"Teams communicate a safe workaround while investigation continues, without presenting a workaround as a permanent resolution.",flow:["RCA evidence","Workaround","Known error review","Incident guidance"],risk:"Known error article integration and the Primary Known Error reference depend on the installed Problem/Knowledge integration capability. Do not assume it is enabled.",gates:[
    ["PR-K01","Known error prerequisite","Confirm the installed Problem/Knowledge integration and enabled article workflow","problem_admin"],
    ["PR-K02","Workaround governance","Record approved workaround text on synthetic Problem and audit changes","problem_coordinator"],
    ["PR-K03","Incident communication","Check that related incident owners see approved workaround guidance as configured","itil fulfiller"],
    ["PR-K04","Article lifecycle","If entitled and installed, create a known error article using the configured approval path","knowledge contributor"],
    ["PR-K05","Audience restriction","Verify authorised knowledge readers and negative user criteria/direct-link access","excluded reader"],
    ["PR-K06","Traceable reference","Read back primary known error reference only when the relevant integration is active","problem_coordinator"],
    ["PR-K07","No premature closure","Confirm publishing a workaround does not falsely resolve the underlying Problem","problem_manager"],
    ["PR-K08","Independent receipt","Preserve masked artifact IDs, version, security outcomes and reviewer sign-off privately","independent reviewer"]
  ]},
  fix:{title:"Permanent fix & closure",description:"An approved change addresses a demonstrated root cause, then owners validate recurrence and decide whether to resolve, reanalyse or accept risk.",flow:["Proposed fix","Change approval","Fix validation","Resolve or reanalyse"],risk:"Problem and Change are separate governance records. Do not bypass Change approvals or assume an accepted risk is an implemented technical fix.",gates:[
    ["PR-F01","Validated root cause","Check recorded cause, fix proposal and the evidence supporting that proposal","problem_coordinator"],
    ["PR-F02","Change relationship","Create/link an authorised Change Request and confirm related record references","change_manager"],
    ["PR-F03","Approval separation","Exercise approved/rejected change paths without allowing the proposer to bypass authority","change approver"],
    ["PR-F04","Implementation evidence","Capture synthetic implementation and rollback/readiness evidence through Change","change implementer"],
    ["PR-F05","Fix effectiveness","Verify service recovery and recurrence observations before Problem resolution","problem_manager"],
    ["PR-F06","Reanalysis path","Confirm supported reanalyse/reopen behaviour when the underlying issue persists","problem_coordinator"],
    ["PR-F07","Risk acceptance","Check authorised risk acceptance as an explicit outcome, not falsely labelled a technical fix","risk approver"],
    ["PR-F08","Independent receipt","Record CI/service context, state model, change outcome, roles and reviewer privately","independent reviewer"]
  ]}
});
const KEYS=Object.keys(SCENARIOS);
const HEADERS=["Scenario","Test ID","Control","Expected native DEV acceptance","Persona","Design reviewed","Native execution","Release decision","Classification","Instance alias (private)","Installed version (private)","Executor role (private)","Executed UTC (private)","Evidence receipt (private)","Independent reviewer (private)"];
function getScenario(key){return Object.hasOwn(SCENARIOS,key)?SCENARIOS[key]:null}
function rowsFor(key,marks){const s=getScenario(key);if(!s)return [];const selected=new Set(marks instanceof Set?[...marks]:Array.isArray(marks)?marks:[]);return s.gates.map(([id,control,expected,persona])=>({scenario:s.title,id,control,expected,persona,read:selected.has(id)?"REVIEWED":"UNREVIEWED",native:"NOT RUN",release:"HOLD",classification:"MOCK-ONLY"}))}
function allRows(marks){return KEYS.flatMap(key=>rowsFor(key,marks&&Object.hasOwn(marks,key)?marks[key]:[]))}
function csvField(value){return '"'+String(value).replace(/"/g,'""')+'"'}
function csvRows(rows){return [HEADERS,...rows.map(r=>[r.scenario,r.id,r.control,r.expected,r.persona,r.read,r.native,r.release,r.classification,"","","","","",""])].map(row=>row.map(csvField).join(",")).join("\r\n")+"\r\n"}
function scenarioCsv(key,marks){return getScenario(key)?csvRows(rowsFor(key,marks)):""}
function allCsv(marks){return csvRows(allRows(marks))}
if(typeof module!=="undefined"&&module.exports)module.exports={SCENARIOS,KEYS,HEADERS,getScenario,rowsFor,allRows,scenarioCsv,allCsv};
if(typeof document!=="undefined"){
 const marks=Object.fromEntries(KEYS.map(key=>[key,new Set()]));let current=KEYS[0];
 const tabs=document.getElementById("scenarios"),gates=document.getElementById("gates"),status=document.getElementById("export-status");
 function progress(){document.getElementById("progress").textContent=marks[current].size+" of 8 design gates reviewed · native NOT RUN · release HOLD"}
 function render(){
   const s=getScenario(current);for(const button of tabs.querySelectorAll("button[data-scenario]"))button.setAttribute("aria-pressed",String(button.dataset.scenario===current));
   document.getElementById("journey-title").textContent=s.title;
   document.getElementById("journey-description").textContent=s.description;
   document.getElementById("journey-risk").textContent=s.risk;
   const flow=document.getElementById("journey-flow");flow.replaceChildren();
   for(let i=0;i<s.flow.length;i++){if(i){const arrow=document.createElement("b");arrow.textContent="→";arrow.setAttribute("aria-hidden","true");flow.append(arrow)}const step=document.createElement("span");step.textContent=s.flow[i];flow.append(step)}
   gates.replaceChildren();for(const [id,control,expected,persona] of s.gates){
     const label=document.createElement("label");label.className="gate";
     const input=document.createElement("input");input.type="checkbox";input.checked=marks[current].has(id);input.setAttribute("aria-label",id+" design reviewed");
     input.addEventListener("change",()=>{if(input.checked)marks[current].add(id);else marks[current].delete(id);progress()});
     const detail=document.createElement("span"),code=document.createElement("span"),strong=document.createElement("strong"),small=document.createElement("small");
     code.className="gate-code";code.textContent=id+" · "+persona;strong.textContent=control;small.textContent=expected;detail.append(code,strong,small);label.append(input,detail);gates.append(label)
   }
   progress();
 }
 function download(csv,name){
   const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));
   try{const a=document.createElement("a");a.href=url;a.download=name;document.body.append(a);a.click();a.remove()}
   finally{URL.revokeObjectURL(url)}
   status.textContent="Local CSV prepared. All native evidence remains NOT RUN / HOLD / MOCK-ONLY.";
 }
 tabs.addEventListener("click",event=>{const button=event.target.closest("button[data-scenario]");if(button&&getScenario(button.dataset.scenario)){current=button.dataset.scenario;render()}});
 document.getElementById("export-scenario").addEventListener("click",()=>download(scenarioCsv(current,marks[current]),"problem-management-"+current+"-8-gates-HOLD.csv"));
 document.getElementById("export-all").addEventListener("click",()=>download(allCsv(marks),"problem-management-24-dev-gates-HOLD.csv"));
 document.getElementById("reset").addEventListener("click",()=>{marks[current].clear();status.textContent="Reading marks cleared; native acceptance remains NOT RUN.";render()});
 render();
}
