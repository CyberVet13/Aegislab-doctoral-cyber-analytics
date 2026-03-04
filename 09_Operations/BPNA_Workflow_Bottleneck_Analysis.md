# AegisLab Workflow — Bottleneck Analysis

**Purpose:** Identify bottlenecks in the AegisLab research workflow (10_Input → Run Agent → Review Queue → 11_Results) and suggest mitigations.

**Last Updated:** 2026-02-21

---

## Implemented Fixes (2026-02-21)

| Fix | Status |
|-----|--------|
| **Parallel processing** | ✅ Workflow API `/process-input` and Auto-Processor now use `ThreadPoolExecutor` (max 3 workers) |
| **File locking** | ✅ `review_queue.json` uses `filelock` for safe concurrent access (Streamlit, Gradio, CLI, API) |
| **Batch approve** | ✅ Streamlit and Gradio Review Queue have "Approve all" button |
| **LLM streaming** | ✅ Streamlit Run Agent: `call_stream()` + "Stream output" checkbox (OpenAI + Anthropic) |
| **PDF/DOCX cache** | ✅ Extracted text cached in `10_Input/.extracted/`; pre-extract on Dashboard upload |

**New dependencies:** `filelock>=3.12.0` (Streamlit_App, Gradio_App, Workflow_API requirements.txt)

---

## Executive Summary

| Bottleneck | Severity | Location | Impact |
|------------|----------|----------|--------|
| LLM call latency | **Critical** | T4 (Run Agent) | 10–60+ sec per file; dominates end-to-end time |
| Sequential file processing | ~~Critical~~ **Mitigated** | Auto-Processor, /process-input | Now parallel (max 3 workers) |
| PI review (human) | ~~High~~ **Mitigated** | T7 (Review Queue) | Batch approve available |
| review_queue.json contention | ~~Medium~~ **Fixed** | Shared file | File locking (filelock) |
| Auto-processor blocking | ~~Medium~~ **Fixed** | watchdog + subprocess | Thread pool (3 workers) |
| Document extraction | ~~Low~~ **Mitigated** | _read_input (PDF/DOCX) | Cached in 10_Input/.extracted/ |

---

## 1. LLM Call (T4) — Critical

**Where:** `aegislab_ui/model_gateway.py` → OpenAI / Anthropic API

**Behavior:** Each agent run makes one synchronous LLM call. Typical latency:
- Claude Sonnet 4.5: ~10–30 seconds
- Claude Opus 4.6: ~20–60+ seconds
- GPT-4o: ~10–40 seconds

**Bottleneck:** The LLM call is the dominant cost in time. No streaming, no parallelization within a run.

**Mitigations:**
- Use streaming where supported (improves perceived latency)
- For batch: run multiple agents in parallel (separate processes/threads)
- Consider smaller/faster models for Daily Driver when quality allows
- Cache repeated prompts if applicable

---

## 2. Sequential File Processing — Critical

**Where:**
- `09_Operations/aegislab_auto_processor.py` — `_process_file()` blocks per file
- `09_Operations/Workflow_API/app.py` — `_run_process_input()` loops files sequentially

**Behavior:**
```
File 1 → LLM (30s) → File 2 → LLM (30s) → File 3 → LLM (30s) ...
```
5 files ≈ 2.5+ minutes minimum (serial).

**Bottleneck:** All files processed one-by-one. No worker pool, no parallel subprocesses.

**Mitigations:**
- **Parallel workers:** Process multiple files concurrently (e.g., `ThreadPoolExecutor` or separate processes)
- **Queue + workers:** Auto-processor could spawn N workers; each picks from queue
- **Rate limits:** Respect API rate limits (e.g., max 2–3 concurrent Anthropic calls)
- **Dashboard /process-input:** Use `concurrent.futures` to run `run_agent()` in parallel (with limit)

---

## 3. PI Review (T7) — Human Bottleneck

**Where:** Streamlit / Gradio Review Queue tab; `review_queue.json`

**Behavior:** Single PI must manually Approve / Request changes / Archive each item. No delegation, no batch approve.

**Bottleneck:** Human throughput is fixed. If 10 deliverables land in queue, PI reviews one at a time.

**Mitigations:**
- Batch approve for low-risk items (e.g., "Approve all Daily Driver outputs from Agent 02")
- Pre-filter: show only items needing attention
- Delegate: allow co-reviewers for specific agent outputs
- Auto-approve rules: e.g., "If Agent 02 + Daily Driver + no safety flags → auto-approve" (with audit)

---

## 4. review_queue.json Contention — Medium

**Where:** `09_Operations/Gradio_App/review_queue.json`

**Behavior:** Streamlit, Gradio, CLI, and Workflow API all read/write this file. No locking. Append and remove operations are read-modify-write.

**Bottleneck:** If two agent runs finish at nearly the same time, both read, both append, both write → one append can be lost. Rare but possible with parallel processing.

**Mitigations:**
- Add file locking (e.g., `fcntl` on Unix, or `msvcrt` on Windows)
- Use a small SQLite DB or Redis for queue instead of JSON
- Serialize queue updates through a single process (e.g., Workflow API as sole writer)

---

## 5. Auto-Processor Blocking — Medium

**Where:** `aegislab_auto_processor.py` — `subprocess.run(..., timeout=300)`

**Behavior:** When a new file is detected, `_process_file()` runs `run_agent_cli.py` and blocks until it completes (up to 5 min). During that time, `on_created` can fire for other files, but each `_process_file` runs in the same thread—effectively serial.

**Bottleneck:** Files dropped in rapid succession are processed one-by-one. The watchdog detects them, but processing is serial.

**Mitigations:**
- Spawn processing in a thread/process pool so multiple files can run in parallel
- Or: add files to an in-memory queue; worker threads consume from queue
- Increase timeout if Deep Dive runs exceed 5 min

---

## 6. Document Extraction — Low

**Where:** `run_agent_cli.py` — `_read_input()` → `_extract_docx()`, `_extract_pdf()`

**Behavior:** PDF and DOCX are extracted synchronously before the LLM call. Large PDFs (100+ pages) can take several seconds.

**Bottleneck:** Minor compared to LLM. Can add up with many large files.

**Mitigations:**
- Pre-extract text when files are uploaded; cache in 10_Input or temp
- Use async extraction if moving to async framework
- Limit PDF page count for very large documents (e.g., first 50 pages)

---

## 7. Flow Diagram — Bottlenecks Annotated

```mermaid
flowchart TB
    subgraph Fast["Fast"]
        T1[Place brief]
        T2[Load context]
        T3[Select Agent]
        T5[Write artifact]
        T6[Add to queue]
    end

    subgraph Slow["Slow"]
        T4[LLM call]
    end

    subgraph Human["Human bottleneck"]
        T7[PI Review]
        T8[Approve/Archive]
    end

    subgraph Serial["Serial bottleneck"]
        AP[Auto-Process]
    end

    T1 --> T2 --> T3 --> T4
    T4 --> T5 --> T6
    T6 --> T7 --> T8
    AP -.->|parallel (3 workers)| T4
```

---

## 8. Recommended Priorities

| Priority | Action | Effort | Status |
|----------|--------|--------|--------|
| 1 | Parallelize `/process-input` and Auto-Processor (2–3 concurrent runs) | Medium | ✅ Done |
| 2 | Add file locking or DB for `review_queue.json` before parallelization | Low | ✅ Done |
| 3 | Batch approve for Review Queue | Low | ✅ Done |
| 4 | Consider streaming for LLM responses (UX) | Medium | ✅ Done |
| 5 | Pre-extract PDF/DOCX on upload (optional) | Low | ✅ Done |

---

## Related

- [BPNA_Workflow.md](BPNA_Workflow.md) — Process model
- [Workflow_Visual.md](Workflow_Visual.md) — Flow diagram
- [Workflow_API/app.py](Workflow_API/app.py) — `_run_process_input()`
- [aegislab_auto_processor.py](aegislab_auto_processor.py) — File watcher
