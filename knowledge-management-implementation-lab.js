/* Synthetic browser-only Knowledge Management lab. No ServiceNow API, storage or auto-certification. */
"use strict";
const SCENARIOS=Object.freeze({
  author:{title:"Author & publish",description:"A contributor creates a reusable resolution article; the assigned manager reviews it before the permitted audience can read it.",flow:["Draft article","Quality review","Approval","Published"],risk:"Risk to control: the approval-publish setting, contributor permissions and article-version prerequisites vary by knowledge base and installed release.",gates:[
    ["KN-A01","Base configuration","Confirm the intended active knowledge base, manager and contribution policy","knowledge_admin"],
    ["KN-A02","Contributor persona","A permitted contributor can create a synthetic draft in the correct knowledge base","knowledge contributor"],
    ["KN-A03","Article structure","Check title, summary, category, template and validity settings on kb_knowledge","knowledge contributor"],
    ["KN-A04","Approval routing","Publish requests are directed to the intended approver only where approval workflow is configured","knowledge approver"],
    ["KN-A05","Rejection path","A rejected article remains unpublished and can be corrected safely","knowledge approver"],
    ["KN-A06","Publication","Approved synthetic article becomes visible to an authorised reader","approved reader"],
    ["KN-A07","Unauthorised contribution","Excluded user cannot create or edit knowledge in the restricted base","excluded contributor"],
    ["KN-A08","Private audit receipt","Capture version, scope, test executor, approvals and masked evidence references","independent reviewer"]
  ]},
  access:{title:"Reader & access",description:"An employee searches for a fix while a restricted procedure remains hidden from an excluded audience.",flow:["Search query","Criteria evaluated","Authorised article","Feedback"],risk:"Risk to control: user criteria must protect both search results and direct URLs; do not rely on the navigation hiding a page.",gates:[
    ["KN-R01","Read criteria","Confirm Can Read and Cannot Read configuration for the knowledge base","knowledge_admin"],
    ["KN-R02","Positive reader","Authorised reader can discover the published synthetic article using search","approved reader"],
    ["KN-R03","Direct link","Authorised reader opens the published article from its direct link","approved reader"],
    ["KN-R04","Denied search","Excluded reader cannot discover restricted article text or title via search","excluded reader"],
    ["KN-R05","Denied direct link","Excluded reader cannot retrieve a restricted article via a direct URL","excluded reader"],
    ["KN-R06","Contribute criteria","Reader-only persona cannot modify article or contribution settings","read-only persona"],
    ["KN-R07","Feedback","Supported feedback on the permitted article reaches configured owners without leaking restricted text","approved reader"],
    ["KN-R08","Private audit receipt","Record fresh-session personas, release, exact test outcome and reviewer receipt","independent reviewer"]
  ]},
  retire:{title:"Review & retire",description:"An owner detects an outdated procedure, routes it through the applicable governance process and verifies its final visibility.",flow:["Validity review","Revision or retire","Approval decision","Search checked"],risk:"Risk to control: versioned Review, Outdated and Pending retirement states depend on the Knowledge Management Advanced feature and instance settings.",gates:[
    ["KN-T01","Ownership","Confirm assigned article owner or ownership group and review cadence","knowledge manager"],
    ["KN-T02","Validity","Identify an expiring synthetic article and the configured expiration behaviour","knowledge manager"],
    ["KN-T03","Review route","Confirm whether revision and Review state are supported by activated versioning","knowledge contributor"],
    ["KN-T04","Revision approval","Approved revision publishes without silently overriding an unrelated article","knowledge approver"],
    ["KN-T05","Retirement request","Submit a retirement request through the configured base process","knowledge manager"],
    ["KN-T06","Retirement rejection","Rejected retirement leaves the article visible to authorised readers","knowledge approver"],
    ["KN-T07","Retired visibility","After approved retirement, verify reader search and direct-link behaviour","approved reader"],
    ["KN-T08","Private audit receipt","Record state transition, installed plugin prerequisite, role and reviewer outcome","independent reviewer"]
  ]}
});
const HEADERS=["Scenario","Test ID","Control","Expected native DEV test","Persona","Design reviewed","Native outcome","Release decision","Classification","Instance alias (private)","App/version (private)","Execution date (private)","Evidence receipt alias (private)","Executor role (private)","Independent reviewer (private)"];
const KEYS=Object.keys(SCENARIOS);
function getScenario(key){return Object.hasOwn(SCENARIOS,key)?SCENARIOS[key]:null}
function rowsFor(key,marks){const scenario=getScenario(key);if(!scenario)return [];const read=new Set(Array.isArray(marks)?marks:marks instanceof Set?[...marks]:[]);return scenario.gates.map(([id,control,expected,persona])=>({scenario:scenario.title,id,control,expected,persona,read:read.has(id)?"REVIEWED":"UNREVIEWED",native:"NOT RUN",release:"HOLD",classification:"MOCK-ONLY"}))}
function allRows(marks){return KEYS.flatMap(key=>rowsFor(key,marks&&marks[key]))}
function quoteCsv(value){return '"'+String(value).replace(/"/g,'""')+'"'}
function csvForRows(rows){return [HEADERS,...rows.map(row=>[row.scenario,row.id,row.control,row.expected,row.persona,row.read,row.native,row.release,row.classification,"","","","","",""])].map(fields=>fields.map(quoteCsv).join(",")).join("\r\n")+"\r\n"}
function csvFor(key,marks){return getScenario(key)?csvForRows(rowsFor(key,marks)):""}
function allCsv(marks){return csvForRows(allRows(marks))}
if(typeof module!=="undefined"&&module.exports){module.exports={getScenario,rowsFor,allRows,csvFor,allCsv,SCENARIOS,HEADERS}}
if(typeof document!=="undefined"){
const marks={author:new Set(),access:new Set(),retire:new Set()};
let selected="author";
const group=document.getElementById("scenarios"),gates=document.getElementById("gates"),status=document.getElementById("export-status");
function render(){
  const scenario=getScenario(selected);
  for(const b of group.querySelectorAll("button[data-scenario]"))b.setAttribute("aria-pressed",String(b.dataset.scenario===selected));
  document.getElementById("journey-title").textContent=scenario.title;
  document.getElementById("journey-description").textContent=scenario.description;
  document.getElementById("journey-risk").textContent=scenario.risk;
  const flow=document.getElementById("journey-flow");flow.replaceChildren();
  scenario.flow.forEach((stage,index)=>{if(index){const arrow=document.createElement("b");arrow.textContent="→";arrow.setAttribute("aria-hidden","true");flow.append(arrow)}const el=document.createElement("span");el.textContent=stage;flow.append(el)});
  gates.replaceChildren();scenario.gates.forEach(([id,control,expected,persona])=>{
    const label=document.createElement("label");label.className="gate";
    const checkbox=document.createElement("input");checkbox.type="checkbox";checkbox.checked=marks[selected].has(id);checkbox.setAttribute("aria-label",id+" reviewed");checkbox.addEventListener("change",()=>{if(checkbox.checked)marks[selected].add(id);else marks[selected].delete(id);progress()});
    const details=document.createElement("span"),code=document.createElement("span"),strong=document.createElement("strong"),small=document.createElement("small");code.className="code";code.textContent=id+" · "+persona;strong.textContent=control;small.textContent=expected;details.append(code,strong,small);label.append(checkbox,details);gates.append(label)});
  progress()
}
function progress(){document.getElementById("progress").textContent=marks[selected].size+" of 8 design controls reviewed · native NOT RUN · release HOLD"}
function download(filename,csv){const blob=new Blob([csv],{type:"text/csv;charset=utf-8"});const url=URL.createObjectURL(blob);try{const a=document.createElement("a");a.href=url;a.download=filename;a.click()}finally{URL.revokeObjectURL(url)}status.textContent="CSV prepared locally. All native results remain NOT RUN / HOLD / MOCK-ONLY."}
group.addEventListener("click",e=>{const btn=e.target.closest("button[data-scenario]");if(btn&&getScenario(btn.dataset.scenario)){selected=btn.dataset.scenario;status.textContent="No ServiceNow requests have been made.";render()}});
document.getElementById("export-scenario").addEventListener("click",()=>download("knowledge-"+selected+"-8-dev-gates.csv",csvFor(selected,marks[selected])));
document.getElementById("export-all").addEventListener("click",()=>download("knowledge-management-24-dev-gates.csv",allCsv(marks)));
document.getElementById("reset").addEventListener("click",()=>{marks[selected].clear();status.textContent="Reading marks cleared for this journey; native NOT RUN.";render()});
render();
}