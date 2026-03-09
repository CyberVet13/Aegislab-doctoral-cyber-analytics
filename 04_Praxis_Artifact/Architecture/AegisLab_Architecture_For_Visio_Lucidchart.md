# AegisLab Architecture — For Visio & Lucidchart

This document provides a consolidated architecture diagram and step-by-step instructions for importing it into **Microsoft Visio** or **Lucidchart**.

---

## Option 1: Lucidchart (Recommended — Easiest)

Lucidchart has **built-in Mermaid support** — no plugin required.

### Steps

1. **Sign up** at [lucidchart.com](https://www.lucidchart.com) (free tier works).
2. **Create a new document** → Blank diagram.
3. **Add Mermaid diagram:**
   - Click the **Diagram as code** icon in the Primary Toolbar (or **+** → **Diagram as code**).
   - Click **Generate** and paste the Mermaid code below.
   - Click **+ New Mermaid diagram** to create it on the canvas.
4. Lucidchart will generate the diagram. You can then:
   - Rearrange nodes
   - Change colors and styles
   - Export as PNG, PDF, or SVG
   - Share and collaborate

**Note:** Lucidchart supports flowchart, sequence, class, state, C4, Gantt, and ER diagrams. Generated diagrams may render as static images; for fully editable shapes, use Lucid AI or redraw manually.

### Lucidchart + VS Code / Cursor

There is **no official Lucidchart plugin** for VS Code or Cursor. To work with diagrams in your editor:

- **Option A:** Use the exported PNG/SVG from the automation script — open in Lucidchart when you need to edit.
- **Option B:** Use the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) VS Code extension — edit `.drawio` files in Cursor, then export to Lucidchart or Visio as needed.

---

## Option 2: Visio

Visio does not import Mermaid directly. Use one of these approaches:

### Method A: Export from Mermaid Live (PNG/SVG → Visio)

1. Go to [mermaid.live](https://mermaid.live).
2. Paste the Mermaid code below into the editor.
3. Click **Export** → **PNG** or **SVG**.
4. In Visio: **Insert** → **Pictures** → select the exported file.
5. Or: Create a new diagram and use the image as a reference to redraw with Visio shapes.

### Method B: Use draw.io (Free) as intermediary

1. Go to [app.diagrams.net](https://app.diagrams.net) (draw.io).
2. **Arrange** → **Insert** → **Advanced** → **Mermaid**.
3. Paste the Mermaid code and insert.
4. **File** → **Export as** → **VSDX** (Visio format).
5. Open the `.vsdx` file in Microsoft Visio.

---

## Consolidated Mermaid Diagram (Copy Below)

Copy everything between the triple backticks:

```
flowchart TB
    subgraph User["👤 User Layer"]
        PI["PI / Researcher"]
    end

    subgraph Entry["🖥️ Entry Points"]
        Streamlit["Streamlit Dashboard<br/>localhost:8501<br/>Run Agent · Review Queue · Audit"]
        Gradio["Gradio Workflow<br/>localhost:7860<br/>Input → Run → Review"]
        API["Workflow API<br/>localhost:8002<br/>Zapier / Webhooks"]
        CLI["CLI<br/>run_agent_cli.py"]
    end

    subgraph Backend["⚙️ aegislab_ui (Shared Backend)"]
        Config["config"]
        Validator["repo_validator"]
        Loader["templates_loader"]
        Router["router"]
        Gateway["model_gateway"]
        Logging["logging_audit"]
        RAG["rag"]
        Safety["safety"]
    end

    subgraph Agents["🤖 11 Specialized Agents"]
        A1["01 PI Orchestrator"]
        A2["02 Research Methodologist"]
        A3["03 Praxis Architect"]
        A4["04 Threat & Adversary"]
        A5["05 Zero Trust Architecture"]
        A6["06 Cryptography"]
        A7["07 Security Analytics"]
        A8["08 Visualization"]
        A9["09 Doctoral Writing"]
        A10["10 Defense Simulation"]
        A11["11 Ethics & Governance"]
    end

    subgraph LLM["🧠 LLM Providers"]
        OpenAI["OpenAI<br/>GPT-5.2"]
        Anthropic["Anthropic<br/>Claude Sonnet · Opus"]
    end

    subgraph Data["📁 Data & Persistence"]
        Input["10_Input<br/>Briefs · Prompts"]
        Results["11_Results<br/>PI-Approved Deliverables"]
        ChromaDB["ChromaDB<br/>RAG Index"]
        SessionLogs["Session_Logs"]
        DecisionLogs["Decision_Logs"]
        ReviewQueue["review_queue.json"]
        Gov["00_Governance<br/>Authorship_Log · AI_Use"]
    end

    PI --> Streamlit
    PI --> Gradio
    PI --> API
    PI --> CLI

    Streamlit --> Router
    Gradio --> Router
    API --> Router
    CLI --> Router

    Router --> Loader
    Loader --> Agents
    Router --> Gateway
    Gateway --> OpenAI
    Gateway --> Anthropic
    Router --> RAG
    RAG --> Gateway
    RAG --> ChromaDB
    Gateway --> Logging
    Logging --> SessionLogs
    Logging --> Gov
    Logging --> ReviewQueue
    Router --> DecisionLogs

    Input --> Streamlit
    Input --> Gradio
    Gateway --> Results
```

---

## Simplified High-Level Diagram (Alternative)

For a cleaner, executive-summary style diagram:

```
flowchart LR
    subgraph In["Input"]
        I[10_Input]
    end

    subgraph UIs["User Interfaces"]
        S[Streamlit]
        G[Gradio]
        A[API]
    end

    subgraph Core["Core"]
        B[aegislab_ui]
        Ag[11 Agents]
    end

    subgraph Ext["External"]
        O[OpenAI]
        An[Anthropic]
    end

    subgraph Out["Output"]
        R[11_Results]
        Q[Review Queue]
    end

    I --> UIs
    UIs --> B
    B --> Ag
    Ag --> O
    Ag --> An
    Ag --> R
    Ag --> Q
```

---

## Data Flow Diagram

```
flowchart LR
    A["📥 10_Input<br/>Briefs & Prompts"] --> B["🤖 Run Agent<br/>Streamlit/Gradio/API/CLI"]
    B --> C["🧠 LLM Call<br/>OpenAI / Anthropic"]
    C --> D["📄 Artifact +<br/>Session Log +<br/>Review Queue"]
    D --> E["👤 PI Review<br/>Approve / Request / Archive"]
    E --> F["📤 11_Results<br/>Committee-Ready"]
```

---

## Automation: Export to PNG/SVG

A script automates export so you don't need to copy-paste into mermaid.live.

### Run the export script

From the repo root:

```powershell
python 09_Operations/scripts/export_architecture_diagram.py
```

**Output:** `04_Praxis_Artifact/Architecture/diagrams/`

| File | Description |
|------|-------------|
| `AegisLab_architecture_full.png` / `.svg` | Full architecture diagram |
| `AegisLab_architecture_simple.png` / `.svg` | Simplified high-level view |
| `AegisLab_data_flow.png` / `.svg` | Data flow diagram |

**Requirements:** Python 3, internet (uses [Kroki.io](https://kroki.io) API).

**Use the exports:**
- **Visio:** Insert → Pictures → select the PNG or SVG
- **Lucidchart:** Import the SVG, or drag-and-drop the PNG
- **Docs:** Embed PNG/SVG in markdown or Word

### Optional: Run on architecture changes

Add a pre-commit hook or run manually after editing the Mermaid in this file. The script reads from this document and regenerates all diagrams.

---

## Quick Reference: What You Need

| Tool | Account | Import Method |
|------|---------|---------------|
| **Lucidchart** | Free at lucidchart.com | Import Data → Mermaid → Paste code |
| **Visio** | Microsoft 365 or standalone | Export from mermaid.live (PNG/SVG) or draw.io (VSDX) |
| **draw.io** | None (browser) | Arrange → Insert → Advanced → Mermaid |

---

**Last Updated:** March 2026
