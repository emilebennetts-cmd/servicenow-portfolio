'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { evaluate, safeId, validDigest, sensitiveNotes } = require('../screenshot-review-safety.js');
const all = [
  { label: 'Original inspected', checked: true },
  { label: 'Rights confirmed', checked: true },
  { label: 'Final pixels approved', checked: true }
];
const base = {
  evidence_id: 'PUBLIC-IMG-01', classification: 'dev',
  redacted_file_sha256: 'a'.repeat(64),
  notes: 'Dated evidence in controlled owner review; public caption requires approval'
};
test('safe alias never accepts native sys_id, whitespace or a URI', () => {
  assert.ok(safeId('DWB-IMG_23'));
  for (const value of ['deadbeefdeadbeefdeadbeefdeadbeef', 'unsafe id', 'https://example.org', ''])
    assert.equal(safeId(value), false);
});
test('digest requires 64 hex and rejects blank or all-zero placeholders', () => {
  assert.ok(validDigest('A'.repeat(64)));
  for (const value of ['', '0'.repeat(64), '1'.repeat(63), 'z'.repeat(64)])
    assert.equal(validDigest(value), false);
});
test('fully checked review is still not image publication authorisation', () => {
  const state = evaluate(base, all);
  assert.equal(state.export_safe, true);
  assert.equal(state.record.publication_gate, 'review_complete_not_auto_authorised');
  assert.equal(state.record.redacted_file_sha256, 'a'.repeat(64));
  assert.equal(state.record.reviewed_at_utc, null);
});
test('unchecked control always yields blocked receipt', () => {
  const s = evaluate(base, [{label:'Independent reviewer', checked:false}]);
  assert.equal(s.record.publication_gate, 'blocked');
  assert.deepEqual(s.record.missing_controls, ['Independent reviewer']);
});
test('missing digest blocks review completion even when all boxes checked', () => {
  const s = evaluate({...base, redacted_file_sha256: ''}, all);
  assert.equal(s.record.publication_gate, 'blocked');
  assert.equal(s.record.redacted_file_sha256, '');
  assert.ok(s.issue_labels.some(v => v.includes('SHA-256')));
});
test('notes with emails, instance URLs, sys_ids, IPs or credentials are blocked and never echoed', () => {
  const suspect = [
    'consultant@example.org', 'https://dev123.service-now.com/nav_to.do',
    'record ffeeddccbbaa99887766554433221100',
    'endpoint 10.4.2.1',
    'api_key = sensitive-token-value',
    'www.example.org/document'
  ];
  for (const notes of suspect) {
    assert.ok(sensitiveNotes(notes), notes);
    const result = evaluate({...base,notes},all);
    assert.equal(result.export_safe,false,notes);
    assert.equal(result.record.publication_gate,'blocked',notes);
    assert.ok(!JSON.stringify(result).includes(notes),notes);
  }
});
test('safe narrative notes are retained without making a runtime claim', () => {
  const r = evaluate(base, all);
  assert.equal(r.record.notes, base.notes);
  assert.equal(r.record.content_screening, 'heuristic-only-human-review-required');
});
test('invalid identity prevents a downloadable receipt', () => {
  const s=evaluate({...base,evidence_id:'1234'},all);
  assert.equal(s.export_safe,false);
  assert.equal(s.record.evidence_id,'');
  assert.equal(s.record.publication_gate,'blocked');
});
test('unexpected classification fails closed to unverified', () => {
  assert.equal(evaluate({...base,classification:'production-approved'},all).record.classification,'unverified');
});
test('incomplete review with safe identity still permits a HOLD-only draft', () => {
  const s=evaluate({...base,redacted_file_sha256:''},[]);
  assert.equal(s.export_safe,true);
  assert.equal(s.record.publication_gate,'blocked');
});
