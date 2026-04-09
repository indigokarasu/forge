# OCAS Inter-Skill Interfaces

Spec Version: 2.0
Author: Indigo Karasu

Changes from 1.5: replaced intake directory pattern with journal payload convention; all inter-skill communication now flows through typed fields in journal entries; eliminated intake directories; consumers scan shared journal tree and filter on payload fields; cooperative read and session-scoped interfaces unchanged.

---

## Purpose

This document defines the contracts for all inter-skill communication in the OCAS ecosystem. Skills communicate through typed payload fields in journal entries written to the shared journal tree at `{agent_root}/commons/journals/`, not through direct calls, shared memory, or intake directories.

---

## General Rules

- Every skill run writes a journal to `{agent_root}/commons/journals/{skill-name}/YYYY-MM-DD/{run_id}.json`.
- When a run produces output relevant to another skill, it includes a typed payload field in the journal entry.
- Consuming skills scan the shared journal tree and filter for entries containing their relevant payload fields.
- Each consumer tracks which `run_id`s it has already processed via an ingestion log in its own `{agent_root}/commons/data/{skill-name}/` directory.
- Journal files are immutable after write. Consumers never modify them.
- See the shared schemas specification for the payload schemas referenced here.

---

## Journal Payload Interfaces

### Elephas Entity Signals

**Payload field:** `signal`

**Producers:** Any skill that observes entities, relationships, or events worth promoting to Chronicle: Sift, Scout, Look, Thread, Corvus, Weave (optional), Triage (optional).

**Consumer:** Elephas

**Format:**
```json
{
  "signal": {
    "entities": [
      {
        "type": "Entity/Person",
        "data": { ... },
        "confidence": "high",
        "user_relevance": "user"
      }
    ]
  }
}
```

**Consumption:** Elephas scans all journals for entries with a `signal` field during `elephas.ingest.journals`. Tracks processed run_ids in `{agent_root}/commons/data/ocas-elephas/ingestion_log.jsonl`.

---

### Briefing Signals (→ Vesper)

**Payload field:** `briefing`

**Producers:** Corvus (opportunity insights), Sands (schedule briefs), Bower (Drive health), Spot (availability alerts), Custodian (system alerts).

**Consumer:** Vesper

**Format:**
```json
{
  "briefing": {
    "surface": true,
    "category": "opportunity_discovery",
    "headline": "Recurring pattern: user researches travel destinations on Mondays",
    "confidence": 0.82,
    "suggested_follow_up": "Vesper could prompt trip planning on Monday mornings"
  }
}
```

**Categories:** `opportunity_discovery`, `routine_prediction`, `anomaly_alert`, `thread_continuation`, `schedule_brief`

**Consumption:** Vesper scans all journals for entries with `briefing.surface: true` during `vesper.briefing.morning`, `vesper.briefing.evening`, or `vesper.briefing.manual`. Vesper owns all filtering and relevance decisions. Tracks processed run_ids in `{agent_root}/commons/data/ocas-vesper/briefings_ingested.jsonl`.

---

### Behavioral Signals (Corvus → Praxis)

**Payload field:** `behavioral_signal`

**Producer:** Corvus

**Consumer:** Praxis

**Format:**
```json
{
  "behavioral_signal": {
    "signal_type": "anomaly_detected",
    "target_skill": "ocas-scout",
    "description": "Scout retry_rate exceeded 0.20 threshold across last 8 runs",
    "evidence_refs": ["r_b3e8d2", "r_c91f4a", "r_d2f1e3"],
    "confidence": "high",
    "suggested_event_type": "failure"
  }
}
```

**Signal types:** `anomaly_detected`, `pattern_validated`, `regression_flagged`

**Consumption:** Praxis scans Corvus journals for entries with `behavioral_signal` during scheduled passes. Praxis decides whether to record an event and extract a lesson — it is not obligated to act on every signal.

---

### Variant Proposals (Mentor → Forge)

**Payload field:** `variant_proposal`

**Producer:** Mentor

**Consumer:** Forge

**Format:**
```json
{
  "variant_proposal": {
    "target_skill": "ocas-scout",
    "base_version": "1.1.0",
    "observed_problem": "verified_claim_ratio below 0.70 target over last 30 runs",
    "supporting_evidence": ["eval_a7f2c1", "r_b3e8d2"],
    "proposed_changes": "Strengthen source corroboration requirement",
    "expected_improvement": "verified_claim_ratio from 0.62 to >= 0.72",
    "evaluation_plan": "Run challenger against benchmark-scout-v1 with 20 requests",
    "minimum_runs": 20,
    "critical_non_regression_conditions": ["entity_resolution_accuracy >= 0.90"]
  }
}
```

**Consumption:** Forge scans Mentor journals for entries with `variant_proposal` during build cycles. Forge builds the variant package and places it for challenger testing.

---

### Variant Decisions (Mentor → Forge)

**Payload field:** `variant_decision`

**Producer:** Mentor

**Consumer:** Forge

**Format:**
```json
{
  "variant_decision": {
    "variant_id": "ocas-scout-variant-20260307",
    "target_skill": "ocas-scout",
    "decision": "promote",
    "rationale": "Challenger exceeded champion on all OKR metrics over 25 runs",
    "aggregate_scores": { ... },
    "confidence": "high",
    "non_regression_check": true,
    "evaluation_window_runs": 25
  }
}
```

**Decisions:** `promote`, `continue_testing`, `archive`, `reject`, `emergency_rollback`

**Consumption:** Forge scans Mentor journals for entries with `variant_decision`. Emergency rollback is acted on immediately regardless of polling cycle.

---

### Experiment Requests (Mentor → Fellow)

**Payload field:** `experiment_request`

**Producer:** Mentor

**Consumer:** Fellow

**Format:**
```json
{
  "experiment_request": {
    "experiment_id": "exp_a7f2c1",
    "target": "ocas-scout",
    "objective": "verified_claim_ratio",
    "benchmark": "benchmark-scout-v1",
    "budget": { "type": "task_count", "value": 20 },
    "constraints": {
      "max_variants": 3,
      "max_cycles": 5,
      "mutation_surface": ["source_corroboration"],
      "protected_surface": ["entity_resolution"]
    }
  }
}
```

**Consumption:** Fellow is purely reactive. Mentor writes the journal entry, then invokes `fellow.experiment.run` directly. Fellow reads the experiment_request from Mentor's most recent journal.

---

### Cycle Results (Fellow → Mentor)

**Payload field:** `cycle_result`

**Producer:** Fellow

**Consumer:** Mentor

**Format:**
```json
{
  "cycle_result": {
    "experiment_id": "exp_a7f2c1",
    "target": "ocas-scout",
    "baseline_score": 0.62,
    "best_variant_id": "ocas-scout-variant-20260307",
    "best_variant_score": 0.74,
    "improvement": 0.12,
    "decision": "promote"
  }
}
```

**Decisions:** `promote`, `no_change`, `abort`

**Consumption:** Mentor scans Fellow journals for entries with `cycle_result` during heartbeat passes. On `promote`, Mentor may emit a `variant_decision`. On `abort`, Mentor logs the failure.

---

### Research Threads (Thread → Corvus)

**Payload field:** `research_thread`

**Producer:** Thread

**Consumer:** Corvus

**Format:**
```json
{
  "research_thread": {
    "thread_id": "thr_b3e8d2",
    "topic_label": "electric vehicle charging infrastructure",
    "sessions": 5,
    "entities": ["Tesla", "ChargePoint"],
    "thread_strength": 0.85,
    "novelty_score": 0.72,
    "interest_candidate": true
  }
}
```

**Consumption:** Corvus scans Thread journals for entries with `research_thread` during analysis cycles as signal context for the Interest Engine and Novelty drive.

---

## Mentor Journal Feed

Mentor reads journals from all skills during heartbeat evaluation passes.

**Path:** `{agent_root}/commons/journals/` (recursive scan)

**Producers:** All skills (every run writes a journal).

**Consumption:** Mentor scans all journals during `mentor.heartbeat.light` and `mentor.heartbeat.deep`. Tracks processed run_ids via `{agent_root}/commons/data/ocas-mentor/ingestion_log.jsonl`.

Mentor and Elephas are independent consumers of the same journal files. Neither blocks the other. Mentor reads for performance evaluation; Elephas reads to extract entity signals.

---

## Cooperative Read Interfaces

Cooperative reads are read-only cross-skill data accesses. They are optional — the requesting skill must degrade gracefully if the cooperating skill's data is absent.

Rules:
- The reading skill opens data as read-only. It must not write, move, or delete files.
- The reading skill must not block on missing data.
- The reading skill documents cooperative reads in its SKILL.md `## Optional skill cooperation` section.

### Sift ↔ Thread: Query Rewriting

Sift reads Thread's active research context to improve query specificity:
```
{agent_root}/commons/data/ocas-thread/active_context.json
```
If absent, Sift proceeds with the unmodified query.

### Sift ↔ Weave: Entity Disambiguation

Sift queries Weave's social graph database to disambiguate entity references:
```
{agent_root}/commons/db/ocas-weave/
```
Read-only. If absent, Sift proceeds with unresolved references.

### Scout ↔ Weave: Identity Context

Scout reads Weave's social graph to pre-populate identity context (known aliases, emails, relationships). Same database path. Scout never writes to Weave.

### Rally → Vesper: Portfolio Outcome

Vesper reads Rally's latest daily report during briefing generation:
```
{agent_root}/commons/data/ocas-rally/reports/{YYYY-MM-DD}-daily.json
```
If absent or stale (>48h), Vesper skips Rally data without error.

### Taste ↔ Sift: Item Enrichment

Direct skill invocation in-session. If Sift is absent, Taste records the item with available data only.

### Voyage ↔ Sift: Venue and Route Enrichment

Direct skill invocation in-session. If Sift is absent, Voyage proceeds with available data.

---

## Session-Scoped Interfaces

These interfaces pass data directly in-session with no file I/O. Used when user confirmation is required before action.

### Vesper → Dispatch: Briefing Delivery

Vesper passes a completed briefing to Dispatch for delivery. Dispatch drafts the message and awaits explicit user confirmation before sending. If Dispatch is not present, Vesper presents the briefing inline.

### Praxis → Dispatch: Action Handoff

Praxis passes communication action decisions to Dispatch for drafting. Dispatch drafts and awaits explicit user approval before any send operation.

---

## Polling and Timing

Consumers scan the shared journal tree on their own schedule. There are no push notifications or event queues.

| Consumer | What it scans | Recommended Cadence |
|---|---|---|
| Elephas | All journals for `signal` field | Every `elephas.ingest.journals` run (~15 min) |
| Mentor | All journals for OKR evaluation; Fellow journals for `cycle_result` | Every heartbeat (~15 min) |
| Vesper | All journals for `briefing.surface: true`; Rally reports (cooperative read) | At briefing generation time |
| Praxis | Corvus journals for `behavioral_signal` | Every scheduled pass or on-demand |
| Forge | Mentor journals for `variant_proposal` and `variant_decision` | Every build cycle or on-demand |
| Corvus | Thread journals for `research_thread` | During analysis cycles |
| Fellow | Mentor journals for `experiment_request` | On `fellow.experiment.run` invocation |
| Custodian | All journals + all errors for health monitoring | Every scan cycle |

---

## Error Handling

If a consumer finds a malformed journal entry:
1. Log the error to its own `decisions.jsonl`.
2. Skip the entry and continue processing.
3. Do not modify the original journal file.

---

## Adding New Interfaces

When a new inter-skill interface is needed:
1. Define the journal payload field name and schema.
2. Add an entry to this spec with producer, consumer, format, and consumption cadence.
3. Update the relevant skill SKILL.md files.
4. Bump this spec's minor version.

Do not create undocumented inter-skill interfaces.
