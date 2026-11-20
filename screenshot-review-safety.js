/* Browser-local screenshot-review receipt guard. No network or storage access.
 * A syntactically complete record is never permission to publish an image. */
(function (root) {
  'use strict';
  const ISSUE_LABELS = Object.freeze({
    invalid_id: 'Use a public-safe alias (letters, digits, hyphens or underscores), not a native record identifier.',
    invalid_digest: 'Enter the SHA-256 of the final flattened PNG: exactly 64 hexadecimal characters.',
    sensitive_notes: 'Review notes contain possible sensitive details. Remove them before exporting.'
  });
  const SENSITIVE = [
    /(?:https?:\/\/|www\.)\S+/i,
    /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i,
    /\b[a-f0-9]{32}\b/i,
    /\b(?:\d{1,3}\.){3}\d{1,3}\b/,
    /\b(?:password|secret|bearer|api[_ -]?key|access[_ -]?token)\b\s*[:=]\s*\S+/i,
    /\b[A-Z0-9.-]+\.service-now\.com\b/i
  ];
  function safeId(id) {
    return /^[A-Za-z][A-Za-z0-9_-]{2,79}$/.test(id) &&
      !/^[a-f0-9]{32}$/i.test(id);
  }
  function validDigest(digest) {
    return /^[a-f0-9]{64}$/i.test(digest) && !/^0{64}$/.test(digest);
  }
  function sensitiveNotes(notes) {
    return SENSITIVE.some(pattern => pattern.test(notes));
  }
  function evaluate(input, controls) {
    const evidenceId = String(input.evidence_id || '').trim();
    const notes = String(input.notes || '').trim();
    const digest = String(input.redacted_file_sha256 || '').trim().toLowerCase();
    const safe = safeId(evidenceId);
    const digestOK = validDigest(digest);
    const notesSensitive = sensitiveNotes(notes);
    const completed = controls.filter(c => c.checked).map(c => c.label);
    const missing = controls.filter(c => !c.checked).map(c => c.label);
    const issues = [];
    if (!safe) issues.push('invalid_id');
    if (!digestOK) issues.push('invalid_digest');
    if (notesSensitive) issues.push('sensitive_notes');
    const complete = !issues.length && !missing.length;
    const exportSafe = safe && !notesSensitive;
    return {
      export_safe: exportSafe,
      issue_labels: issues.map(code => ISSUE_LABELS[code]),
      record: {
        schema: 'portfolio-screenshot-review-v2',
        evidence_id: safe ? evidenceId : '',
        classification: ['unverified', 'source', 'dev', 'mock', 'prod'].includes(input.classification)
          ? input.classification : 'unverified',
        redacted_file_sha256: digestOK ? digest : '',
        notes: notesSensitive ? '[withheld: sensitive content suspected]' : notes,
        content_screening: 'heuristic-only-human-review-required',
        completed_controls: completed,
        missing_controls: missing,
        publication_gate: complete ? 'review_complete_not_auto_authorised' : 'blocked',
        reviewed_at_utc: null
      }
    };
  }
  const api = Object.freeze({ evaluate, safeId, validDigest, sensitiveNotes });
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PortfolioScreenshotReviewSafety = api;
})(typeof window !== 'undefined' ? window : globalThis);
