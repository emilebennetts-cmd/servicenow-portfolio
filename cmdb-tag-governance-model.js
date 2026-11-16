"use strict";
/* Public, synthetic CMDB Tag Governance demonstrations. No instance I/O. */
(function(root,factory){const api=factory();if(typeof module==="object"&&module.exports)module.exports=api;else root.CMDBTagGovernance=api;})(typeof globalThis!=="undefined"?globalThis:this,function(){
const scenarios=[
{id:"key-drift",label:"Inconsistent environment keys",category:"Normalisation review",summary:"Two sources describe the same environment with different tag keys.",records:[
{ci:"SYN-APP-01",source:"Cloud inventory",tags:[["Environment","Production"],["owner","platform-team"],["cost_center","CC-100"]]},
{ci:"SYN-APP-02",source:"Cloud inventory",tags:[["env","prod"],["owner","platform-team"],["cost_center","CC-100"]]}],
note:"Review aliases with data owners, preserving raw tags and discovery provenance. Do not bulk rewrite keys before checking source-of-truth and downstream Service Mapping criteria."},
{id:"missing-cost",label:"Missing accountability tag",category:"Policy non-compliance",summary:"Required chargeback information is absent from a synthetic CI.",records:[
{ci:"SYN-CLOUD-03",source:"Cloud inventory",tags:[["env","production"],["owner","app-team"]]},
{ci:"SYN-CLOUD-04",source:"Cloud inventory",tags:[["env","production"],["owner","app-team"],["cost_center","CC-200"]]}],
note:"Assign a remediation task to the accountable owner; request source correction. Avoid inventing a chargeback cost centre."},
{id:"collision",label:"Conflicting duplicate values",category:"Identity conflict",summary:"A single synthetic CI carries contradictory environment values under equivalent keys.",records:[
{ci:"SYN-VM-05",source:"Cloud inventory",tags:[["environment","production"],["Env","development"],["owner","ops-team"],["cost_center","CC-300"]]}],
note:"HOLD all automated changes. Identify which provider and timestamp produced each value before interpreting environment or service-mapping scope."},
{id:"reingestion",label:"Manual fix versus re-ingestion",category:"Source authority",summary:"A manual value change would be overwritten by the authoritative cloud source on rediscovery.",records:[
{ci:"SYN-VM-06",source:"Cloud discovery",tags:[["env","dev"],["owner","ops-team"],["cost_center","CC-400"]]}],
sourceConflict:true,note:"Keep the change request on HOLD and remediate the tag upstream. Validate on a fresh discovery cycle and check whether tag-based Service Mapping membership changes."},
{id:"baseline",label:"Policy-compliant example",category:"Review before release",summary:"Synthetic keys are consistent and complete, but no native audit or independent sign-off exists.",records:[
{ci:"SYN-APP-07",source:"Cloud inventory",tags:[["env","production"],["owner","service-team"],["cost_center","CC-500"]]},
{ci:"SYN-APP-08",source:"Cloud inventory",tags:[["env","production"],["owner","service-team"],["cost_center","CC-500"]]}],
note:"A green illustration still requires policy execution, owner confirmation, Service Mapping impact review and independent DEV acceptance."}
];
const alias=Object.freeze({env:"environment",environment:"environment",costcentre:"cost_center",costcenter:"cost_center",cost_center:"cost_center",owner:"owner"});
function canon(key){const compact=String(key).trim().toLowerCase().replace(/[\s-]+/g,"_");return alias[compact]||compact;}
function value(v){const text=String(v).trim().toLowerCase();return text==="prod"?"production":text==="dev"?"development":text;}
function evaluate(id){
 const s=scenarios.find(s=>s.id===id);if(!s)throw Error("Unknown synthetic scenario");
 const findings=[];const canonicalKeys=new Set();let rawKeys=new Set();
 for(const record of s.records){
  const byKey=new Map();
  for(const [key,val] of record.tags){const k=canon(key),v=value(val);rawKeys.add(key);canonicalKeys.add(k);if(!byKey.has(k))byKey.set(k,new Set());byKey.get(k).add(v);}
  for(const mandatory of ["environment","owner","cost_center"])if(!byKey.has(mandatory)||!Array.from(byKey.get(mandatory)).some(Boolean))findings.push({ci:record.ci,kind:"missing",message:"Required "+mandatory+" tag absent"});
  for(const [key,values] of byKey)if(values.size>1)findings.push({ci:record.ci,kind:"conflict",message:"Conflicting values for "+key});
 }
 const rawAliases=Array.from(rawKeys).filter(k=>canon(k)==="environment");
 if(rawAliases.length>1)findings.push({ci:"CROSS-CI",kind:"variant",message:"Environment key variants require owner-approved normalisation"});
 if(s.sourceConflict)findings.push({ci:"SOURCE",kind:"authority",message:"Manual remediation would be overwritten by discovery"});
 const hold=findings.some(f=>["missing","conflict","authority"].includes(f.kind));
 return {scenario:s,findings,ciCount:s.records.length,tagCount:s.records.reduce((n,r)=>n+r.tags.length,0),canonicalKeyCount:canonicalKeys.size,decision:hold?"HOLD — REMEDIATION BLOCKED":"REVIEW — NOT APPROVED",nativeStatus:"NOT RUN",releaseDecision:"HOLD",evidence:"MOCK-ONLY",explanation:s.note};
}
const gateTypes=[
["READBACK","Read cmdb_key_value for an authorised synthetic/non-customer sample, prove CI association and scope"],
["POLICY","Confirm installed Tag Governance application and effective Tag Count, Tag Presence and Tag Key & Value policy definitions"],
["LINEAGE","Compare provider tag keys, source timestamps, discovery update and downstream service-mapping scope"],
["ACL","Test an authorised analyst and a denied persona; record actual roles and ACL outcomes"],
["APPROVAL","Re-run in DEV, capture before/after exception counts, owner decision and independent release sign-off"]
];
const gates=scenarios.flatMap((scenario,i)=>gateTypes.map(([suffix,action],j)=>({id:"TG-"+String(i+1).padStart(2,"0")+"-"+String(j+1).padStart(2,"0"),scenario:scenario.id,action,expected:"Private dated native read-back, reviewer and evidence receipt; no simulated test is sufficient",nativeStatus:"NOT RUN",releaseDecision:"HOLD",classification:"MOCK-ONLY"})));
const headers=["Test ID","Scenario","Native action","Expected evidence","Native result","Release decision","Evidence classification","Instance alias","Installed plugin / version","Executor","Execution UTC","Private evidence receipt","Independent reviewer"];
function csvEscape(v){return '"'+String(v??"").replace(/"/g,'""')+'"';}
function csv(id="all"){if(id!=="all"&&!scenarios.some(s=>s.id===id))throw Error("Unknown export scenario");const subset=gates.filter(g=>id==="all"||g.scenario===id);return [headers,...subset.map(g=>[g.id,g.scenario,g.action,g.expected,g.nativeStatus,g.releaseDecision,g.classification,"","","","","",""])].map(r=>r.map(csvEscape).join(",")).join("\r\n")+"\r\n";}
function safeText(node,text){if(node)node.textContent=String(text);}
function attach(doc){
 if(!doc||!doc.getElementById)return;
 const panel=doc.getElementById("tg-investigation"),controls=Array.from(doc.querySelectorAll("[data-tg-case]"));
 const make=(tag,klass,value)=>{const x=doc.createElement(tag);if(klass)x.className=klass;x.textContent=value;return x;};
 function show(id){
  const r=evaluate(id),s=r.scenario;controls.forEach(c=>c.setAttribute("aria-pressed",String(c.getAttribute("data-tg-case")===id)));
  if(panel){panel.replaceChildren();const hero=make("div","result-head",s.category);panel.append(hero,make("h3","",s.label),make("p","",s.summary));
  const stats=make("div","metrics","");for(const [n,t] of [[r.ciCount,"synthetic CIs"],[r.tagCount,"tag pairs"],[r.findings.length,"review findings"]]){const b=make("div","metric","");b.append(make("strong","",n),make("span","",t));stats.append(b);}panel.append(stats);
  const screen=make("div","mock-screen","");screen.append(make("div","mock-title","Illustrative tag policy console — NOT a ServiceNow capture"));const grid=make("div","mock-rows","");
  for(const record of s.records){const row=make("div","mock-row","");row.append(make("strong","",record.ci),make("span","",record.source),make("small","",record.tags.map(pair=>pair.join(" = ")).join(" • ")));grid.append(row);}screen.append(grid);panel.append(screen);
  const result=make("div","decision","");result.append(make("strong","",r.decision),make("p","",r.explanation));panel.append(result);
  const ul=make("ul","finding-list","");if(!r.findings.length)ul.append(make("li","","No synthetic policy exceptions; this does not demonstrate native compliance."));else r.findings.forEach(f=>ul.append(make("li","",f.ci+": "+f.message)));panel.append(make("h4","","Policy and source findings"),ul);
  }
  safeText(doc.getElementById("tg-selected"),s.label);
  safeText(doc.getElementById("tg-gate-count"),gates.filter(g=>g.scenario===id).length+" native checks remain NOT RUN / HOLD.");
  const selected=doc.getElementById("tg-download-selected");if(selected)selected.setAttribute("data-export",id);
 }
 controls.forEach(b=>b.addEventListener("click",()=>show(b.getAttribute("data-tg-case"))));
 doc.querySelectorAll("[data-export]").forEach(b=>b.addEventListener("click",()=>{
   const id=b.getAttribute("data-export"),raw=csv(id);const blob=new Blob([raw],{type:"text/csv;charset=utf-8"}),url=URL.createObjectURL(blob),a=doc.createElement("a");
   a.href=url;a.download=id==="all"?"cmdb-tag-governance-25-native-gates.csv":"cmdb-tag-governance-"+id+"-5-gates.csv";doc.body.append(a);a.click();a.remove();URL.revokeObjectURL(url);
 }));
 show("key-drift");
}
if(typeof document!=="undefined")document.addEventListener("DOMContentLoaded",()=>attach(document));
return {scenarios,gateTypes,gates,headers,canon,value,evaluate,csv,attach};
});
