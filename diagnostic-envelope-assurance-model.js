/* Diagnostic DIAG Envelope Assurance Lab.
 * Source-informed public contract: Diagnostic-Workbench2/README_BUILD.md and
 * tools/wb2_catalog.json (reviewed 2026-11-16). Only fixed synthetic examples.
 * Not an instance connector, envelope importer, script executor or approval.
 */
(function(root){
'use strict';
const BEGIN='DIAG_ENVELOPE_BEGIN',END='DIAG_ENVELOPE_END';
const common=Object.freeze({
 collector:'ITSM_INC_001',version:'1.0',schema_version:'1.0',
 module:'ITSM',category:'Incident',captured_at:'2026-09-01 10:00:00',
 read_only:true,classification:'Internal',contains_pii:false,
 record_count:1,metrics:{total:120,open:38},
 results:[{kind:'state_breakdown',field:'state',value:'In Progress',count:38}],
 entities:[],relationships:[],notes:[]
});
const cases=Object.freeze([
 ['valid','Bounded aggregate candidate','CAN_REVIEW','A syntactically valid aggregate is still unverified and needs an authorised reviewer.'],
 ['markers','Missing wrapper marker','REJECT','An incomplete DIAG wrapper cannot establish an authentic complete envelope.'],
 ['schema','Unsupported schema','REJECT','Schema identity must be independently mapped before any interpretation.'],
 ['write','Write safety declaration false','REJECT','The stated collector safety contract is not read-only.'],
 ['pii','Consumer-data flag raised','REJECT','Potential personal data must remain in authorised private custody.'],
 ['not-applicable','Missing product table','NOT_APPLICABLE','A missing product table is not a passing zero-defect assessment.'],
 ['capped','Capped group population','INCOMPLETE','The denominator cannot be trusted after a cap or truncation.'],
 ['zero','Zero-record observation','REVIEW','Zero rows need entitlement, scope and completeness reconciliation.'],
 ['sensitive','Sensitive-content note','REJECT','Potential credential material is rejected rather than shown or exported.'],
 ['no-groups','No groups but nonzero incident total','CAN_REVIEW','Collector record_count is the number of output groups, not the incident-table denominator.'],
 ['count-drift','Declared group count disagrees','INCOMPLETE','The number of returned groups must reconcile with record_count.'],
 ['open-over-total','Open count exceeds total','INCOMPLETE','Metric populations are inconsistent even if the wrapper is present.'],
 ['payload-injection','Unexpected identity field','REJECT','Unknown properties are outside this sanitised example contract.'],
 ['unsafe-result','Sensitive group label','REJECT','Unexpected free-text group labels cannot enter this public demonstration.'],
 ['malformed-note','Non-text collector note','REJECT','Notes require bounded text rather than arbitrary nested objects.']
].map(v=>Object.freeze({id:v[0],title:v[1],expected:v[2],guidance:v[3]})));
const nativeGates=Object.freeze([
 ['DEA-N01','Read back target app scope, installed version and catalogue lineage','Installed record and source fingerprint'],
 ['DEA-N02','Approve collector execution authority and least-privilege roles','Platform owner sign-off and negative persona test'],
 ['DEA-N03','Confirm product entitlement and table existence','Installed product/role entitlement evidence'],
 ['DEA-N04','Verify DIAG wrapper and schema_version on bounded native output','Private intact wrapper, version and parser receipt'],
 ['DEA-N05','Confirm read_only and no consumer-data disclosure','Privacy/security review and controlled sample'],
 ['DEA-N06','Reconcile result cap and metric denominators','Source query and complete population comparison'],
 ['DEA-N07','Validate missing-table and zero-row semantics','Independent N/A versus genuine zero test'],
 ['DEA-N08','Independently review findings before Delivery handoff','Named reviewer decision and authorised release receipt']
].map(r=>Object.freeze({id:r[0],action:r[1],evidence:r[2]})));
function fixture(key){
 if(!cases.some(x=>x.id===key))throw Error('Unknown synthetic case');
 const env={...common,metrics:{...common.metrics},results:common.results.map(r=>({...r})),entities:[],relationships:[],notes:[]};
 if(key==='schema')env.schema_version='99.0';
 if(key==='write')env.read_only=false;
 if(key==='pii')env.contains_pii=true;
 if(key==='not-applicable'){env.metrics.total=-1;env.metrics.open=-1;env.results=[];env.record_count=0;env.notes=['incident table is not available on this instance.'];}
 if(key==='capped')env.notes=['assignment grouping capped at 400 groups.'];
 if(key==='zero'){env.record_count=0;env.results=[];env.metrics.total=0;env.metrics.open=0;}
 if(key==='no-groups'){env.record_count=0;env.results=[];}
 if(key==='count-drift')env.record_count=2;
 if(key==='open-over-total')env.metrics.open=130;
 if(key==='payload-injection')env.user_email='not-permitted@example.invalid';
 if(key==='unsafe-result')env.results[0].value='person@example.invalid';
 if(key==='malformed-note')env.notes=[{value:'nested data'}];
 if(key==='sensitive')env.notes=['credential material included'];
 const raw=BEGIN+'\n'+JSON.stringify(env)+'\n'+(key==='markers'?'DIAG_END_MISSING':END);
 return raw;
}
function parse(raw){
 if(typeof raw!=='string'||raw.length>24576)throw Error('Envelope too large or non-text');
 if(raw.split(BEGIN).length!==2||raw.split(END).length!==2)throw Error('Wrapper markers absent or duplicated');
 const before=raw.indexOf(BEGIN),after=raw.indexOf(END);
 if(before<0||after<=before+BEGIN.length)throw Error('Wrapper order invalid');
 if(raw.slice(0,before).trim()||raw.slice(after+END.length).trim())throw Error('Extra text outside wrapper');
 let env;
 try{env=JSON.parse(raw.slice(before+BEGIN.length,after).trim());}catch(_){throw Error('Malformed JSON');}
 if(!env||Array.isArray(env)||typeof env!=='object')throw Error('Envelope object required');
 return env;
}
function evaluate(raw){
 let env;
 try{env=parse(raw);}catch(_){return Object.freeze({decision:'REJECT',reason:'Missing, incomplete or invalid DIAG wrapper',checks:Object.freeze(['wrapper'])});}
 const outcome=(decision,reason,checks)=>Object.freeze({decision,reason,checks:Object.freeze(checks)});
 // This public model permits only its synthetic sample subset; it is NOT the
 // private intake parser and must never be used to ingest actual instance output.
 const allowed=['collector','version','schema_version','module','category','captured_at','read_only','classification','contains_pii','record_count','metrics','results','entities','relationships','notes'];
 if(Object.keys(env).some(k=>!allowed.includes(k)))return outcome('REJECT','Unexpected field outside the public fixture contract',['shape']);
 if(env.schema_version!=='1.0'||env.collector!=='ITSM_INC_001')return outcome('REJECT','Collector identity or schema mismatch',['schema']);
 if(env.read_only!==true)return outcome('REJECT','Read-only safety declaration failed',['read_only']);
 if(env.contains_pii!==false||env.classification!=='Internal')return outcome('REJECT','Privacy or classification check failed',['privacy']);
 if(!Array.isArray(env.notes)||env.notes.length>16||env.notes.some(n=>typeof n!=='string'||n.length>240))return outcome('REJECT','Collector notes require bounded text',['shape']);
 if(!Array.isArray(env.results)||env.results.length>100||!Array.isArray(env.entities)||env.entities.length||!Array.isArray(env.relationships)||env.relationships.length)return outcome('REJECT','Public subset accepts aggregate groups only',['shape']);
 if(!Number.isSafeInteger(env.record_count)||env.record_count<0)return outcome('REJECT','Invalid output group count',['shape']);
 if(!env.metrics||typeof env.metrics!=='object'||Array.isArray(env.metrics)||
    !Number.isSafeInteger(env.metrics.total)||!Number.isSafeInteger(env.metrics.open)||
    Object.values(env.metrics).some(n=>typeof n!=='number'||!Number.isFinite(n)))return outcome('REJECT','Metric value shape invalid',['metrics']);
 const states=['New','In Progress','On Hold','Resolved','Closed','(empty)'];
 const groupSafe=r=>r&&typeof r==='object'&&!Array.isArray(r)&&
    Object.keys(r).every(k=>['kind','field','value','count'].includes(k))&&
    ((r.kind==='state_breakdown'&&r.field==='state'&&states.includes(r.value))||
     (r.kind==='priority_breakdown'&&r.field==='priority'&&['1','2','3','4','5','(empty)'].includes(r.value)))&&
    Number.isSafeInteger(r.count)&&r.count>=0;
 if(!env.results.every(groupSafe))return outcome('REJECT','Unexpected or sensitive result-group content',['privacy','shape']);
 if(/credential|password|token|secret|bearer|api.key|authorization/i.test(env.notes.join(' ')))return outcome('REJECT','Sensitive-content signal detected',['privacy']);
 // Crucial source correction: ITSM-INC-001 sets record_count = results.length;
 // metrics.total is a separate GlideAggregate incident-table population.
 if(env.record_count!==env.results.length)return outcome('INCOMPLETE','Returned group count does not match record_count',['group_count']);
 if(env.metrics.total===-1||env.metrics.open===-1||env.notes.some(n=>/not available/i.test(n)))return outcome('NOT_APPLICABLE','Unavailable product/table is not a zero finding',['applicability']);
 if(env.metrics.total<0||env.metrics.open<0)return outcome('REJECT','Negative metric outside the explicit N/A sentinel',['metrics']);
 if(env.notes.some(n=>/capp?ed|truncat/i.test(n)))return outcome('INCOMPLETE','Capped or truncated result denominator',['denominator']);
 if(env.metrics.open>env.metrics.total)return outcome('INCOMPLETE','Open incidents exceed total incident population',['denominator']);
 if(env.metrics.total===0)return outcome('REVIEW','Zero incident population requires independent scope review',['population']);
 return outcome('CAN_REVIEW','Synthetic shape checks passed; source population and native assurance remain HOLD',['wrapper','schema','read_only','privacy','group_count','population']);
}
function assess(id){
 const item=cases.find(x=>x.id===id);
 if(!item)throw Error('Unknown synthetic case');
 const outcome=evaluate(fixture(id));
 if(outcome.decision!==item.expected)throw Error('Source-informed example drift');
 return Object.freeze({id:item.id,title:item.title,expected:item.expected,decision:outcome.decision,
  reason:outcome.reason,guidance:item.guidance,checks:outcome.checks,
  evidence_class:'MOCK-ONLY',native_execution:'NOT RUN',release_decision:'HOLD',
  dev_verified:false,production_verified:false,screenshot_approved:false});
}
function csvField(value){
 const text=String(value);
 const safe=/^[=+\-@\t\r]/.test(text)?"'"+text:text;
 return '"'+safe.replace(/"/g,'""')+'"';
}
function csv(rows){return '\ufeff'+rows.map(row=>row.map(csvField).join(',')).join('\r\n')+'\r\n';}
function exportCases(){
 const rows=[['case_id','synthetic_example','decision','next_review_action','evidence_class','native_execution','release_decision']];
 for(const item of cases){const r=assess(item.id);rows.push([r.id,r.title,r.decision,r.guidance,r.evidence_class,r.native_execution,r.release_decision]);}
 return csv(rows);
}
function exportNativeGates(){
 const rows=[['control_id','native_action','independent_evidence_required','execution','review','release','dev_verification','production_verification','evidence_reference','reviewer']];
 for(const gate of nativeGates)rows.push([gate.id,gate.action,gate.evidence,'NOT RUN','UNREVIEWED','HOLD','NOT VERIFIED','NOT VERIFIED','','']);
 return csv(rows);
}
const api=Object.freeze({cases,nativeGates,fixture,parse,evaluate,assess,exportCases,exportNativeGates});
if(typeof module!=='undefined'&&module.exports)module.exports=api;
root.DiagnosticEnvelopeAssurance=api;
if(typeof document==='undefined')return;
const choice=document.getElementById('scenario'),status=document.getElementById('decision'),reason=document.getElementById('reason'),next=document.getElementById('next'),steps=document.getElementById('steps'),summary=document.getElementById('summary');
if(!choice||!status||!reason||!next||!steps||!summary)return;
function paint(){
 const r=assess(choice.value);
 status.textContent=r.decision;status.setAttribute('data-decision',r.decision);
 reason.textContent=r.reason;next.textContent=r.guidance;
 steps.replaceChildren();
 ['Wrapper','Schema / collector','Read-only / PII','Applicability','Denominator','Independent approval'].forEach((x,i)=>{
  const li=document.createElement('li');
  const hit=r.checks.some(c=>({0:['wrapper'],1:['schema'],2:['read_only','privacy'],3:['applicability'],4:['denominator','population'],5:[]}[i]||[]).includes(c));
  li.textContent=x+' — '+(hit?'Observed synthetic signal':'Requires native evidence');
  steps.appendChild(li);
 });
 summary.textContent='Example '+r.id+' · '+r.evidence_class+' · '+r.native_execution+' · RELEASE '+r.release_decision+' · DEV-VERIFIED 0';
}
function download(text,name){
 const url=URL.createObjectURL(new Blob([text],{type:'text/csv;charset=utf-8'}));
 const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
 setTimeout(()=>URL.revokeObjectURL(url),0);
}
choice.addEventListener('change',paint);
document.getElementById('download-examples').addEventListener('click',()=>download(exportCases(),'diagnostic-envelope-synthetic-cases.csv'));
document.getElementById('download-gates').addEventListener('click',()=>download(exportNativeGates(),'diagnostic-envelope-native-hold-gates.csv'));
paint();
})(typeof globalThis!=='undefined'?globalThis:this);
