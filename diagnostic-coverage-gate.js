/* Diagnostic Evidence Coverage Gate — public synthetic training model.
 * Source-informed categories; no instance access, customer data, real evidence or approval.
 * Classification stays MOCK-ONLY / NOT RUN / HOLD for every export.
 */
(function(root){
'use strict';
const packs=Object.freeze([
  ['DIA-P01','ITSM'],['DIA-P02','CMDB & CSDM'],['DIA-P03','ITOM & Discovery'],
  ['DIA-P04','Security Operations'],['DIA-P05','IRM & Risk'],
  ['DIA-P06','Customer Service'],['DIA-P07','HR Service Delivery'],
  ['DIA-P08','Asset Management'],['DIA-P09','Integrations'],
  ['DIA-P10','Platform Flows']
].map(row=>Object.freeze({id:row[0],label:row[1]})));
const outcomes=Object.freeze({
  UNASSESSED:{label:'Not assessed',next:'Confirm scope, entitlement and permitted evidence first.',kind:'hold'},
  ENTITLEMENT_UNKNOWN:{label:'Entitlement not established',next:'Check installed product, subscription and role access.',kind:'hold'},
  INVALID:{label:'Unsafe or invalid envelope',next:'Reject the payload, minimise data and repeat validation.',kind:'hold'},
  CAPPED:{label:'Denominator incomplete',next:'Reconcile full population and truncated aggregates.',kind:'hold'},
  REVIEW_PENDING:{label:'Independent review required',next:'Reconcile evidence provenance and obtain a separate reviewer.',kind:'hold'},
  EXCLUDED:{label:'Proposed scope exclusion',next:'Require explicit scope-owner approval; never score as healthy.',kind:'exclude'},
  REVIEWED:{label:'Synthetic review complete',next:'Still requires actual native execution and independent evidence.',kind:'illustration'}
});
const keys=Object.freeze(Object.keys(outcomes));
const profiles=Object.freeze({
  unassessed:Object.freeze(Array(10).fill('UNASSESSED')),
  mixed:Object.freeze(['REVIEWED','REVIEW_PENDING','CAPPED','ENTITLEMENT_UNKNOWN','INVALID','UNASSESSED','EXCLUDED','REVIEW_PENDING','UNASSESSED','REVIEWED']),
  denominator:Object.freeze(['REVIEWED','REVIEWED','REVIEWED','REVIEWED','CAPPED','REVIEWED','REVIEWED','REVIEWED','REVIEWED','REVIEWED']),
  complete:Object.freeze(Array(10).fill('REVIEWED'))
});
const descriptions=Object.freeze({
 unassessed:'No native evidence submitted. Every area remains not assessed.',
 mixed:'Partial example: evidence, entitlement, scope and independent-review gaps coexist.',
 denominator:'Nine apparently reviewed areas cannot compensate for one unknown denominator.',
 complete:'All ten rows are only simulated as reviewed: native evidence and release approval remain absent.'
});
function evaluate(key){
 if(!Object.prototype.hasOwnProperty.call(profiles,key))throw new Error('Unknown synthetic scenario');
 const profile=profiles[key];
 if(profile.length!==packs.length)throw new Error('Source pack count drift');
 const rows=packs.map((pack,i)=>{
  const code=profile[i],entry=outcomes[code];
  if(!entry)throw new Error('Unknown outcome');
  return Object.freeze({
   id:pack.id,pack:pack.label,code,decision:entry.label,action:entry.next,
   evidence_class:'MOCK-ONLY',native_execution:'NOT RUN',release_decision:'HOLD',
   dev_verified:false,production_verified:false,screenshot_approved:false
  });
 });
 const summary={
  total:rows.length,reviewed_example:rows.filter(r=>r.code==='REVIEWED').length,
  blocked:rows.filter(r=>outcomes[r.code].kind==='hold').length,
  exclusions:rows.filter(r=>r.code==='EXCLUDED').length,
  native_verified:0,release:'HOLD'
 };
 return Object.freeze({scenario:key,description:descriptions[key],rows:Object.freeze(rows),summary:Object.freeze(summary)});
}
const csvHeader=Object.freeze(['control_id','pack','synthetic_status','next_native_action','evidence_class','native_execution','release_decision','dev_verified','production_verified','screenshot_approved']);
function csvEscape(v){
 const s=String(v);
 // Strict spreadsheet injection defence even if future catalogue metadata changes.
 const safe=/^[=+\-@\t\r]/.test(s)?"'"+s:s;
 return '"'+safe.replace(/"/g,'""')+'"';
}
function exportCsv(report){
 if(!report||!profiles[report.scenario]||!Array.isArray(report.rows)||report.rows.length!==packs.length)throw new Error('Invalid report');
 const canonical=evaluate(report.scenario);
 for(let i=0;i<packs.length;i++){
  const a=report.rows[i],b=canonical.rows[i];
  if(!a||Object.keys(b).some(k=>a[k]!==b[k]))throw new Error('Report integrity mismatch');
 }
 const lines=[csvHeader.map(csvEscape).join(',')];
 canonical.rows.forEach(r=>lines.push([r.id,r.pack,r.decision,r.action,r.evidence_class,r.native_execution,r.release_decision,r.dev_verified,r.production_verified,r.screenshot_approved].map(csvEscape).join(',')));
 return '\ufeff'+lines.join('\r\n')+'\r\n';
}
const api=Object.freeze({packs,profiles:Object.freeze(Object.keys(profiles)),outcomes, evaluate,exportCsv});
if(typeof module!=='undefined'&&module.exports)module.exports=api;
root.DiagnosticCoverageGate=api;
if(typeof document==='undefined')return;
const scenario=document.getElementById('coverage-scenario'),filter=document.getElementById('coverage-filter'),body=document.getElementById('coverage-rows');
if(!scenario||!filter||!body)return;
const summary=document.getElementById('coverage-summary'),intro=document.getElementById('coverage-description'),count=document.getElementById('coverage-count'),download=document.getElementById('coverage-download');
let current;
function node(tag,text,cls){const e=document.createElement(tag);if(cls)e.className=cls;e.textContent=text;return e;}
function draw(){
 current=evaluate(scenario.value);
 body.replaceChildren();
 const selected=current.rows.filter(r=>filter.value==='all'||(filter.value==='attention'&&r.code!=='REVIEWED')||(filter.value==='reviewed'&&r.code==='REVIEWED'));
 selected.forEach(r=>{
  const tr=document.createElement('tr');
  tr.append(node('th',r.pack),node('td',r.decision),node('td',r.action),node('td','NOT RUN · HOLD'));
  tr.firstChild.scope='row';body.append(tr);
 });
 intro.textContent=current.description;
 summary.textContent=current.summary.reviewed_example+' synthetic reviewed · '+current.summary.blocked+' blocked · '+current.summary.exclusions+' proposed exclusions · 0 native verified · RELEASE HOLD';
 count.textContent='Showing '+selected.length+' of '+current.rows.length+' source-informed pack categories.';
}
scenario.addEventListener('change',draw);filter.addEventListener('change',draw);
download.addEventListener('click',()=>{
 try{
  const csv=exportCsv(current),url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download='diagnostic-coverage-'+current.scenario+'-mock-only-hold.csv';
  document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
 }catch(err){summary.textContent='Export stopped: source integrity could not be confirmed. HOLD.';}
});
draw();
})(typeof globalThis!=='undefined'?globalThis:this);
