# Project Roadmap

Derived from Section 8 of `method_i_doc.txt`, this roadmap outlines the sequential phases for building the Method I Narrative Engine. Each phase references design decisions and prompts defined earlier in the document and guides implementation in manageable stages.

## Phase 1: Foundational Data Models and Schemas
1. **Define Character and Scene Schemas** ✅
   - Create JSON or Pydantic models for Character Dossiers, Scene State Manager, Vector Indexes and In-Scene Grounding.
   - Validate example data against these schemas.
   - Set up database tables or JSON columns reflecting the schema structure.
2. **Implement "Living Dossier" Data Layer**
   - Establish data stores or placeholders for `psych_profile_index` and `linguistic_profile_index`.
   - Implement basic retrieval functions for memories and traits until a full vector DB is integrated.

## Phase 2: Core Logic and LLM Pipeline
3. **Develop Scene Generation Pipeline**
   - Implement the turn-by-turn sequence: retrieve context, invoke Inner Monologue LLM, invoke Dialogue & Action LLM, then update state.
   - Integrate the Inner Monologue and Dialogue prompt templates.
   - Parse JSON outputs and update Scene State; test with dummy responses.
4. **LLM Integration**
   - Connect the pipeline to OpenAI or another LLM provider.
   - Verify prompt formatting and handle errors or timeouts.
5. **Scene Conclusion Logic (Basic)**
   - Add a placeholder stopping rule such as max turns or manual stop to avoid infinite loops.

## Phase 3: Casting Call Subsystem
6. **Implement Character Extraction**
   - Build a service or endpoint that ingests text and uses the casting director prompt to return candidate characters.
   - Parse JSON responses from the prompt.
7. **Implement Review & Selection Logic**
   - Allow marking which extracted characters to keep, storing selections in
     memory or a database.
   - ✅ Provide `GET /casting-call/candidates` to list logged candidates.
8. **Implement Dossier Compilation**
   - For selected candidates, call the dossier compiler prompt and validate returned JSON against the schema.
   - Persist compiled characters to the Characters database.
9. **Casting Call Integration**
   - Orchestrate extraction, selection and dossier compilation behind a single action or workflow.
   - Include logging and error handling for malformed LLM output.

## Phase 4: API Endpoints & Backend Services
10. **Design API Endpoints**
    - Implement FastAPI endpoints for Characters, Casting Call, Scenes, Scene Logs and Users based on the API contract.
    - Secure endpoints if authentication is required.
11. **Database Wiring**
    - Connect endpoints to database tables for characters, scenes and turns using SQLAlchemy or similar.
12. **Internal Module Refactoring**
    - Organize code into modules for dossiers, scene generation, casting call and user management.

## Phase 5: Frontend Development (UI Implementation)
13. **Build Scene Builder UI**
    - Components for character selection, premise entry, transcript display and next-turn generation with loading states.
14. **Build Characters Tab UI**
    - List, edit and delete characters via API calls.
15. **Build Casting Call Tab UI**
    - Interface for entering source text, reviewing candidates and compiling dossiers.
16. **Build Users Tab UI**
    - CRUD interface for user accounts.
17. **Build Scene Logs Tab UI**
    - Display past scenes and allow viewing full transcripts.
18. **Integrate UI with Auth (optional)**
    - Implement login flow and attach tokens to API requests if authentication is used.

## Phase 6: Testing and Quality Assurance
19. **End-to-End Testing**
    - Test character creation, scene generation, transcript logging and dossier editing, including edge cases and error handling.
20. **Performance Tuning (Basic)**
    - Measure turn generation latency and identify obvious inefficiencies.

## Phase 7: Deployment and DevOps
21. **Prepare Deployment Artifacts**
    - Create Dockerfiles or configure Vercel/Fly.io settings and ensure environment variables are externalized.
22. **Deployment (Initial Launch)**
    - Deploy frontend and backend to their respective platforms and run smoke tests.
23. **Deployment Checklist Verification**
    - Verify services, environment variables, seeding and security settings; set up monitoring or alerts.
24. **Documentation & Handoff**
    - Provide user and developer documentation, including prompt designs and architectural overviews.

## Phase 8: Dossier Packaging and Identity Infrastructure

**Goal**: Introduce a reproducible `.dossier` packaging format, IPFS-based identity system, and a remix-aware provenance structure—preserving transparency while enabling uniqueness and shareability.

---

### 25. Modular `.dossier` File Specification

Define a new modular and extensible `.dossier` format that contains:

- `core.json`  
  > Canonical character dossier (name, role, arcs, backstory, dialogue style)

- `indices/`  
  - `psych_profile_index.json`  
  - `linguistic_profile_index.json`  
  > Stored separately to allow evolution or recomputation

- `assets/`  
  - Optional `avatar.png`  
  - Optional `voice_config.json`  
  > Future extensibility: `costume/`, `style_templates/`, `narrative_history/`

- `meta.json`  
  > Metadata block including:
  ```json
  {
    "author": "username_or_hash",
    "timestamp": "ISO string",
    "source_text": "original source or extraction document",
    "method_version": "v1.0",
    "parent_cid": "optional",
    "notes": "creator comment"
  }
  ```

Use deterministic file ordering and hashing rules to ensure reproducible content.

---

### 26. IPFS Integration & Content Addressing

- Automate `.dossier` compression + upload to IPFS via backend process.
- Return **CID** to user on upload completion.
- Store CID + metadata in internal DB for discoverability, if desired.
- Allow optional download of `.dossier` file by CID (IPFS client integration or API gateway).

---

### 27. Remixing & Lineage Protocol

- Define standard for remixing:
  - `parent_cid` is mandatory on remixes
  - Authors can include attribution via `author_signature` field
  - No enforcement of originality or access control; trust is social, not cryptographic

- Future option:  
  - Integrate **graph-based lineage visualizer** to explore character family trees

---

### 28. CID Resolution and Upload UI

- Build lightweight interface for:
  - Uploading `.dossier` via drag-and-drop
  - Resolving `.dossier` from CID and previewing
  - Browsing local + shared characters by CID or name

- Support future plugins for:
  - Dossier diffing (between parent and child)
  - Avatar auto-regeneration (e.g. via AI face generator)

---

### 29. Internal APIs for Packaging Flow

- Backend service to:
  - Validate character inputs and create `.dossier`
  - Compress, hash, upload, and return CID
  - Store CID + metadata (if opted in) for public browsing

- Endpoint Examples:
  - `POST /dossiers/pack`
  - `POST /dossiers/upload`
  - `GET /dossiers/:cid`
  - `GET /dossiers/search?query=x`

---

## Phase 9: Feedback Loop & Live Evolution

**Goal**: Transition into continuous learning and improvement through structured user feedback and real-world dossier performance monitoring.

---

### 30. Usage Analytics (Optional, Glass Box Compliant)

Track:

- Turn latency
- Dossier usage frequency
- Scene coherence failures (e.g. contradictions, stalling)
- Remix activity (diff frequency, lineage depth)

> All tracking must be opt-in and anonymized where applicable.

---

### 31. Narrative Quality Feedback

Prompt an llm for qualitative feedback after scenes:

- “Which character broke tone?”
- “Was this scene emotionally satisfying?”
- “Did the scene feel coherent?”

This should use prompt engineering to pose the llm as a Roman Emperor who has very strong and well informed opinions on literature and dramaturgy. He will give an objective review and a thumb up or thumb down for each generated narrative.

This will replace tradition rlhf by (1) automating anonymized data collection about narrative/character quality and (2) challenging users by presenting the emperor's verdict at the end of a story with a sort of sub conscious reminder to Judge Not Lest Ye Be Judged.
