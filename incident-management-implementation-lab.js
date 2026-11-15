/* ServiceNow Incident Management portfolio lab — synthetic client-neutral rehearsal only. */
"use strict";
const SCENARIOS=Object.freeze({
 intake:{title:"Intake & priority",description:"A service desk qualifies an outage, captures safe incident context and applies its configured impact/urgency prioritisation.",screen:"Incident intake",fields:[["Channel","Phone / self-service"],["Business impact","Assess with user"],["Urgency","Instance policy"],["Assignment","Resolver group"]],flow:["Qualify","Log incident","Prioritise","Assign"],risk:"Confirm request versus incident, installed priority lookup, and confidence in CI/service ownership. Never derive a universal P1 threshold from this demonstration.",gates:[
 ["IN-I01","Record identity","Create a synthetic incident and read back its unique number/sys_id and required field values","itil fulfiller"],
 ["IN-I02","Request boundary","Verify that a service request is redirected to an appropriate Catalog item, not falsely classified as an outage","service desk"],
 ["IN-I03","Caller & channel","Check authorised caller, contact channel and required categorisation with anonymised values","incident agent"],
 ["IN-I04","Impact/urgency lookup","Read the target instance data lookup and confirm calculated priority for approved policy cases","incident admin"],
 ["IN-I05","Assignment","Test group assignment rules, manual transfer audit and ownership accountability","resolver group"],
 ["IN-I06","CI/service trust","Check valid CI/business service relationships without accepting unresolved duplicates","cmdb owner"],
 ["IN-I07","Negative access","Excluded persona cannot create or modify privileged incident attributes through UI or direct record route","excluded requester"],
 ["IN-I08","Independent intake receipt","Record target scope, installed version, record alias, persona, execution time and independent reviewer privately","independent reviewer"]
 ]},
 restore:{title:"Restore & communicate",description:"The resolver group investigates and restores the service while keeping internal work notes separate from public communications.",screen:"Incident resolution",fields:[["State","In progress / on hold"],["SLA","Configured schedule"],["Work notes","Internal only"],["Communication","Approved update"]],flow:["Investigate","Escalate","Restore","Update"],risk:"SLA pause, reassign and notification behaviour depend on the actual definitions, schedules and transitions. Do not treat a simulated countdown as measured SLA compliance.",gates:[
 ["IN-R01","State transitions","Read and execute the installed incident In Progress / On Hold transition and mandatory hold reason","incident agent"],
 ["IN-R02","SLA conditions","Read active SLA definitions, schedules, start/stop/pause conditions and task linkage","sla admin"],
 ["IN-R03","SLA pause/resume","Exercise synthetic pause and resume while preserving auditable task SLA results","sla tester"],
 ["IN-R04","Resolver ownership","Assign to a permitted resolver group, test escalation and review reassignment history","resolver group"],
 ["IN-R05","Notes segregation","Confirm work notes stay internal and additional comments reach only authorised audiences","itil fulfiller"],
 ["IN-R06","Notification safety","Check configured customer updates for approved content and correct recipients; block unauthorised data","communications reviewer"],
 ["IN-R07","Negative access","Excluded portal user cannot view internal work notes or restricted linked tasks through direct URLs","excluded requester"],
 ["IN-R08","Independent restoration receipt","Store masked record references, SLA evidence, allowed/denied persona outcomes and reviewer privately","independent reviewer"]
 ]},
 close:{title:"Close & improve",description:"The service desk confirms restoration, records correct resolution codes and separates permanent cause investigation from immediate incident recovery.",screen:"Resolution assurance",fields:[["Restoration","User confirmed"],["Resolution code","Instance mapping"],["Closure","Policy governed"],["Problem link","If recurring"]],flow:["Restore","Validate","Resolve / reopen","Close"],risk:"Do not confuse incident restoration with elimination of root cause. Check installed closure automation, user communication and reconciliation with Problem/Change governance.",gates:[
 ["IN-C01","Resolution policy","Read configured resolution codes, mandatory resolution notes and close-code mapping","incident admin"],
 ["IN-C02","Recovery evidence","Record synthetic user/service restoration confirmation and actual resolution timestamp","incident agent"],
 ["IN-C03","Closure lifecycle","Verify target state flow, notification and auto-closure rules without assuming a fixed default duration","incident manager"],
 ["IN-C04","Reopen path","Exercise permitted reopen/reassign behaviour and SLA impact, including negative tests","incident agent"],
 ["IN-C05","Related problem","For repeated incidents, verify a separate linked Problem with accountable investigation","problem coordinator"],
 ["IN-C06","Authorised change","Confirm risky permanent remediation follows Change control rather than unapproved incident shortcuts","change manager"],
 ["IN-C07","Negative access","Unauthorised persona cannot force close, modify resolution or read restricted linked records","excluded requester"],
 ["IN-C08","Independent closure receipt","Store version, instance alias, record references, role results, timestamp and reviewer privately","independent reviewer"]
 ]}
});
const KEYS=Object.keys(SCENARIOS);
const HEADERS=["Scenario","Test ID","Control","Expected native DEV acceptance","Persona","Design reviewed","Native execution","Release decision","Classification","Instance alias (private)","Installed version (private)","Executor role (private)","Executed UTC (private)","Evidence receipt (private)","Independent reviewer (private)"];
function getScenario(key){return Object.hasOwn(SCENARIOS,key)?SCENARIOS[key]:null}
function rowsFor(key,marks){const s=getScenario(key);if(!s)return [];const reviewed=new Set(marks instanceof Set?[...marks]:Array.isArray(marks)?marks:[]);return s.gates.map(([id,control,expected,persona])=>({scenario:s.title,id,control,expected,persona,read:reviewed.has(id)?"REVIEWED":"UNREVIEWED",native:"NOT RUN",release:"HOLD",classification:"MOCK-ONLY"}))}
function allRows(marks){return KEYS.flatMap(key=>rowsFor(key,marks&&Object.hasOwn(marks,key)?marks[key]:[]))}
function csvValue(value){const s=String(value);return '"'+(/^[=+\-@\t\r]/.test(s)?"'"+s:s).replace(/"/g,'""')+'"'}
function csvRows(rows){return [HEADERS,...rows.map(r=>[r.scenario,r.id,r.control,r.expected,r.persona,r.read,r.native,r.release,r.classification,"","","","","",""])].map(row=>row.map(csvValue).join(",")).join("\r\n")+"\r\n"}
function scenarioCsv(key,marks){return getScenario(key)?csvRows(rowsFor(key,marks)):""}
function allCsv(marks){return csvRows(allRows(marks))}
if(typeof module!=="undefined"&&module.exports)module.exports={SCENARIOS,KEYS,HEADERS,getScenario,rowsFor,allRows,scenarioCsv,allCsv};
if(typeof document!=="undefined"){
 const marks=Object.fromEntries(KEYS.map(k=>[k,new Set()]));let current="intake";
 const tabs=document.getElementById("scenarios"),gates=document.getElementById("gates"),fields=document.getElementById("mock-fields"),flow=document.getElementById("scenario-flow");
 function clear(node){while(node.firstChild)node.removeChild(node.firstChild)}
 function el(tag,text,className){const node=document.createElement(tag);if(className)node.className=className;if(text!==undefined)node.textContent=text;return node}
 function progress(){document.getElementById("progress").textContent=marks[current].size+" of 8 design controls reviewed · native NOT RUN · release HOLD"}
 function render(){
   const s=getScenario(current);
   for(const button of tabs.querySelectorAll("button[data-scenario]"))button.setAttribute("aria-pressed",String(button.dataset.scenario===current));
   document.getElementById("journey-title").textContent=s.title;document.getElementById("journey-description").textContent=s.description;document.getElementById("mock-title").textContent=s.screen;document.getElementById("scenario-risk").textContent=s.risk;
   clear(fields);for(const [name,value] of s.fields){const cell=el("div",undefined,"mock-cell");cell.appendChild(el("span",name));cell.appendChild(document.createTextNode(value));fields.appendChild(cell)}
   clear(flow);s.flow.forEach((stage,i)=>{if(i)flow.appendChild(el("b","→"));flow.appendChild(el("span",stage))});
   clear(gates);for(const [id,control,expected,persona] of s.gates){const label=el("label",undefined,"gate");const input=document.createElement("input");input.type="checkbox";input.checked=marks[current].has(id);input.setAttribute("aria-label","Design reviewed: "+id+" "+control);input.addEventListener("change",()=>{input.checked?marks[current].add(id):marks[current].delete(id);progress()});const copy=el("span");copy.appendChild(el("span",id+" · "+persona,"code"));copy.appendChild(el("strong",control));copy.appendChild(el("small",expected));label.appendChild(input);label.appendChild(copy);gates.appendChild(label)}
   progress();
 }
 function download(csv,name){if(!csv)return;const url=URL.createObjectURL(new Blob(["\uFEFF",csv],{type:"text/csv;charset=utf-8"}));const anchor=document.createElement("a");anchor.href=url;anchor.download=name;anchor.click();URL.revokeObjectURL(url);document.getElementById("export-status").textContent="Downloaded an offline NOT RUN / HOLD worksheet; native acceptance is still pending."}
 tabs.addEventListener("click",event=>{const button=event.target.closest("button[data-scenario]");if(!button||!tabs.contains(button)||!getScenario(button.dataset.scenario))return;current=button.dataset.scenario;render();document.getElementById("export-status").textContent=""});
 document.getElementById("export-one").addEventListener("click",()=>download(scenarioCsv(current,marks[current]),"incident-"+current+"-8-gate-native-hold.csv"));
 document.getElementById("export-all").addEventListener("click",()=>download(allCsv(marks),"incident-management-24-gate-native-hold.csv"));
 render();
}
