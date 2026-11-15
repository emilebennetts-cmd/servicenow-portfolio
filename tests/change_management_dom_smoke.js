/* Public Change Management lab behavioural regression.
 * Node built-ins only. Fake DOM exercises the actual inline page JavaScript.
 * This is browser-logic testing, never a ServiceNow native acceptance claim.
 */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'change-management-implementation-lab.html'), 'utf8');
const match = html.match(/<script[^>]*>([\s\S]*?)<\/script>/);
assert.ok(match, 'inline script must exist');

class Element {
  constructor(tag) {
    this.tagName = tag;
    this.children = [];
    this.dataset = {};
    this.events = {};
    this.attrs = {};
    this.textContent = '';
    this.checked = false;
  }
  addEventListener(event, callback) { this.events[event] = callback; }
  setAttribute(name, value) { this.attrs[name] = value; }
  append(...items) { this.children.push(...items); }
  replaceChildren(...items) { this.children = [...items]; }
  click() {
    if (this.events.click) this.events.click();
    if (this.tagName === 'a') downloads.push(this);
  }
  remove() {}
}

const ids = {};
for (const id of ['gates', 'progress', 'interpretation', 'scenario-title',
                  'scenario-explainer', 'export', 'reset']) ids[id] = new Element('div');
const buttons = ['normal', 'standard', 'emergency'].map(model => {
  const button = new Element('button');
  button.dataset.model = model;
  return button;
});
const downloads = [], blobs = [];
const document = {
  body: new Element('body'),
  getElementById(id) { assert.ok(ids[id], 'unexpected ID: ' + id); return ids[id]; },
  querySelectorAll(selector) { assert.equal(selector, '[data-model]'); return buttons; },
  createElement(tag) { return new Element(tag); }
};
class TestBlob {
  constructor(parts, options) { this.payload = parts.join(''); this.type = options.type; blobs.push(this); }
}
const URL = { createObjectURL: () => 'blob:test', revokeObjectURL: () => {} };
vm.runInNewContext(match[1], {document, URL, Blob: TestBlob, setTimeout() {}},
                   {timeout: 2000, filename: 'change-management-inline.js'});

assert.equal(ids.gates.children.length, 7, 'normal criteria');
assert.match(ids.progress.textContent, /^0 of 7/);
const first = ids.gates.children[0].children[0].children[0];
first.checked = true;
first.events.change();
assert.match(ids.progress.textContent, /^1 of 7/);
buttons[1].click();
assert.match(ids['scenario-title'].textContent, /Standard/);
assert.match(ids.progress.textContent, /^0 of 7/, 'changing model resets marks');
assert.equal(ids.gates.children.length, 7, 'standard criteria');
for (const gate of ids.gates.children) {
  const checkbox = gate.children[0].children[0];
  checkbox.checked = true;
  checkbox.events.change();
}
assert.match(ids.progress.textContent, /7 of 7.*NOT RUN.*HOLD/);
assert.match(ids.interpretation.textContent, /no gate has passed/);
ids.export.click();
assert.equal(blobs.length, 1, 'exactly one CSV created');
assert.equal(downloads.length, 1, 'exactly one download click');
const lines = blobs[0].payload.trim().split(/\r\n/);
assert.equal(lines.length, 8, 'header plus seven criteria');
assert.ok(lines.slice(1).every(line => line.includes('"NOT RUN","HOLD","MOCK-ONLY"')));
assert.equal(downloads[0].download, 'change-management-standard-acceptance-HOLD.csv');
buttons[2].click();
assert.match(ids['scenario-title'].textContent, /Emergency/);
assert.match(ids.progress.textContent, /^0 of 7/);
assert.equal(ids.gates.children.length, 7, 'emergency criteria');
ids.reset.click();
assert.match(ids.progress.textContent, /^0 of 7/);
console.log('PASS: three model selections, reading reset, seven criteria each, fail-closed CSV and no native verification claims');
