/* Offline Chromium regression for KI matrix intake, public synthetic data only. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const {pathToFileURL}=require("node:url");
const {chromium}=require("playwright");

(async()=>{
const root=path.resolve(__dirname,"..");
const browser=await chromium.launch({headless:true});
const pages=["knowledge-intelligence-acceptance-matrix.html","ki-matrix-intake.html"];
const urls=Object.fromEntries(pages.map(x=>[x,pathToFileURL(path.join(root,x)).href]));
let checked=0;
// File.text() resolves asynchronously after the click handler returns. Wait for
// the completed assessment, not merely the click event, to avoid false failures.
async function assessFile(page, expectedText){
 await page.locator("#check").click();
 await page.waitForFunction(text=>(document.getElementById("status")?.textContent||"").includes(text),expectedText,{timeout:10000});
}
try{
 for(const width of [390,768,1024,1440]){
  const page=await browser.newPage({viewport:{width,height:900},acceptDownloads:true});
  const outgoing=[];page.on("request",r=>{if(/^https?:/.test(r.url()))outgoing.push(r.url());});
  await page.goto(urls["knowledge-intelligence-acceptance-matrix.html"]);
  const p=page.waitForEvent("download");
  await page.locator("#ki-export-all").click();
  const d=await p;
  const content=fs.readFileSync(await d.path());
  const csv=content.toString("utf8");
  assert.equal(csv.trim().split("\n").length,181,"180 planned tests expected");
  assert.equal((csv.match(/"SOURCE-ONLY"/g)||[]).length,180);
  assert.equal((csv.match(/"PROPOSED"/g)||[]).length,180);
  await page.goto(urls["ki-matrix-intake.html"]);
  assert.equal(await page.locator("h1").count(),1);
  assert.equal(await page.locator("#receipt").isDisabled(),true);
  await page.locator("#matrix-file").setInputFiles({name:"ki-matrix.csv",mimeType:"text/csv",buffer:content});
  await assessFile(page,"Full plan structurally aligned");
  assert.match(await page.locator("#status").innerText(),/Full plan structurally aligned: 180 cases/);
  assert.equal(await page.locator("#row-count").innerText(),"180");
  assert.equal(await page.locator("#module-count").innerText(),"45");
  assert.equal(await page.locator("#gap-count").innerText(),"0");
  assert.equal(await page.locator("#receipt").isEnabled(),true);
  const receiptDownload=page.waitForEvent("download");
  await page.locator("#receipt").click();
  const receipt=JSON.parse(fs.readFileSync(await (await receiptDownload).path(),"utf8"));
  assert.equal(receipt.dev_verified,false);
  assert.equal(receipt.production_verified,false);
  assert.equal(receipt.publication_approval,"HOLD");
  assert.equal(receipt.customer_data_included,false);
  assert.equal(receipt.reviewed_test_rows,180);
  assert(!JSON.stringify(receipt).includes("evidence_reference"));
  // BOM-prefixed UTF-8 CSVs from common spreadsheet tools are also accepted.
  await page.locator("#matrix-file").setInputFiles({name:"ki-bom.csv",mimeType:"text/csv",buffer:Buffer.concat([Buffer.from([0xEF,0xBB,0xBF]),content])});
  await assessFile(page,"Full plan structurally aligned");
  assert.match(await page.locator("#status").innerText(),/Full plan structurally aligned: 180 cases/);
  // Filtered export with exactly four scenarios for one module.
  const lines=csv.trim().split(/\r?\n/);
  const subset=lines.slice(0,5).join("\r\n")+"\r\n";
  await page.locator("#matrix-file").setInputFiles({name:"ki-filtered.csv",mimeType:"text/csv",buffer:Buffer.from(subset)});
  await assessFile(page,"Filtered plan structurally aligned");
  assert.match(await page.locator("#status").innerText(),/Filtered plan structurally aligned: 1\/45 modules/);
  assert.equal(await page.locator("#gap-count").innerText(),"44");
  // Tampering with a native approval/status flag must not be accepted.
  const tampered=subset.replace('"NOT RUN"','"PASS"');
  await page.locator("#matrix-file").setInputFiles({name:"ki-tampered.csv",mimeType:"text/csv",buffer:Buffer.from(tampered)});
  assert.equal(await page.locator("#receipt").isDisabled(),true,"stale receipt must be invalidated on selection");
  await assessFile(page,"Structural exceptions detected");
  assert.match(await page.locator("#status").innerText(),/Structural exceptions detected/);
  assert.match(await page.locator("#issues").innerText(),/unreviewed plan flags were changed/);
  // Duplicate ID, missing scenario and malformed quotes are rejected or held.
  const duplicate=lines.slice(0,4).concat(lines[1]).join("\r\n");
  await page.locator("#matrix-file").setInputFiles({name:"duplicate.csv",mimeType:"text/csv",buffer:Buffer.from(duplicate)});
  await assessFile(page,"Structural exceptions detected");
  assert.match(await page.locator("#status").innerText(),/Structural exceptions detected/);
  await page.locator("#matrix-file").setInputFiles({name:"malformed.csv",mimeType:"text/csv",buffer:Buffer.from('"unclosed')});
  await assessFile(page,"Unable to assess");
  assert.match(await page.locator("#status").innerText(),/Unable to assess/);
  assert.equal(await page.locator("#receipt").isDisabled(),true);
  // Synthetic demo must never imply full coverage.
  await page.locator("#example").click();
  assert.match(await page.locator("#status").innerText(),/Filtered plan structurally aligned/);
  assert.equal(await page.locator("#module-count").innerText(),"1");
  await page.locator("#reset").click();
  assert.equal(await page.locator("#receipt").isDisabled(),true);
  const layout=await page.evaluate(()=>({document:document.documentElement.scrollWidth,viewport:innerWidth,offenders:[...document.querySelectorAll("body *")].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,12).map(e=>({tag:e.tagName,id:e.id,cls:typeof e.className==="string"?e.className.slice(0,80):"",right:Math.round(e.getBoundingClientRect().right),width:Math.round(e.getBoundingClientRect().width),scroll:e.scrollWidth,client:e.clientWidth,overflow:getComputedStyle(e).overflowX}))}));
  assert.equal(layout.document<=layout.viewport+1,true,"horizontal overflow at "+width+": "+JSON.stringify(layout));
  assert.deepEqual(outgoing,[],"no network requests in public KI pages");
  await page.close();
  checked++;
 }
 console.log("PASS: KI matrix original export, 180-case import, filtered coverage, tamper detection, malformed CSV, receipt HOLD, offline network isolation and responsive layouts at 390/768/1024/1440 ("+checked+"/4).");
}catch(e){console.error(e);process.exitCode=1;}finally{await browser.close();}
})();