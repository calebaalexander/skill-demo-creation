---
name: demo-creation
description: "Create complete demo packages including branded Google Slides decks, GitHub repos, and gameplan files. Use for ALL demo creation, demo deck, demo build, demo slides, or demo package requests. Triggers: create demo, build demo, demo creation, demo deck, demo slides, demo package, build deck, create deck, new demo."
---

# Demo Creation

## Content Classification Rules

**CRITICAL: All artifacts are classified as either INTERNAL or EXTERNAL. Enforce this throughout every step.**

| Classification | Description | May Contain |
|---|---|---|
| **INTERNAL** | For Snowflake employees only. NEVER shared with or visible to customers. | Account scoring, consumption data, contract values, competitive positioning, objection handling, internal strategy, pain points, opportunity details, employee names/roles, internal Slack handles |
| **EXTERNAL** | Customer-facing. May be shared, published to GitHub, or presented on screen. | Feature descriptions, SQL scripts, setup instructions, public docs links, deck content |

**Artifact classification:**
- `GAMEPLAN.md` -- INTERNAL
- Google Slides deck -- EXTERNAL
- `scripts/` -- EXTERNAL
- `data/` -- EXTERNAL
- `README.md` (GitHub) -- EXTERNAL

**EXTERNAL files must NEVER include internal account intelligence, employee names, strategic notes, competitive positioning, or references to internal tools/trackers.**

## Prerequisites

No special prerequisites. GitHub CLI (`gh`) must be authenticated for repo creation.

## Workflow

### Step 1: Gather Demo Inputs

**Goal:** Collect all required information from the user.

**Actions:**

1. **Ask** the user for the following using `ask_user_question`:
   - **Account name** (text, required)
   - **Use case / demo ideas** (text, required) -- 3 specific use cases or demo topics, comma-separated
   - **Include slides?** (options: "Yes, full branded deck" / "No slides, just repo and gameplan")
   - **Local save directory** (text, required, default: "~/Desktop/{AccountName}") -- where to write all local files (GAMEPLAN.md, DECK_CONTENT.md, scripts/, PPTX template copy)
   - **GitHub username** (text, required, default: "calebaalexander")
   - **Presenter name** (text, required, default: user's name from context)
   - **Demo duration** (text, required, default: "60 minutes") -- scheduled length of the demo, used to calibrate slide count and script depth
   - **Target audience** (text, optional) -- e.g., "VP of Data Engineering, Data Scientists"
   - **Speaker(s)** (text, optional) -- comma-separated list of speaker names and titles, e.g., "Caleb Alexander, Solutions Engineer; Evan Mendez, Account Executive". Used for the speakers slide in the deck.
   - **Speaker photo URL(s)** (text, optional) -- comma-separated list of photo URLs (LinkedIn profile photo URLs or direct image URLs) corresponding to each speaker above, e.g., "https://media.licdn.com/dms/image/abc123, https://media.licdn.com/dms/image/def456". If not provided, Snowflake-branded initials will be generated automatically.

2. **Create** the local save directory if it does not exist. All subsequent file writes go here.

3. **If user chose slides**, copy the PPTX template from `~/.cortex/skills/demo-creation/assets/SNOWFLAKE_TEMPLATE_JANUARY_2026.pptx` into the local save directory so the user has it alongside the deck content.

4. **Store** all inputs for use in subsequent steps.

**Output:** Validated demo parameters.

### Step 2: Research Account — Pain Points, Industry Context, and Business Value

**Goal:** Build a business-value-first foundation for the demo. Every feature shown must map to a real pain point the customer is experiencing.

**CRITICAL PRINCIPLE: Pain first, feature second.** The demo is not a product tour. It is a conversation about the customer's problems, with Snowflake features as the answers. Every slide, script, and talking point must trace back to a pain point.

**Actions:**

#### 2a. Leverage Account Discovery Analysis (if report exists)

Check if an account-discovery-analysis report already exists for this account:
- Search the local save directory and `~/Desktop/Accounts/{Account}/` for `*Account_Discovery_Analysis*` HTML/MD files
- If found, read and extract: pain points, tech stack, hiring signals, news triggers, use case recommendations, competitive landscape, consumption profile

If no report exists, run a lightweight version of the research below. For a full deep-dive, recommend running the `account-discovery-analysis` skill first.

#### 2b. Industry and Company Pain Point Research

Run web searches in parallel:
- `"{company_name}" challenges OR pain points OR data strategy` -- what they are struggling with
- `"{company_name}" hiring data engineer OR data scientist OR analytics` -- are they staffing up? What roles? This signals where they feel underinvested
- `"{company_name}" layoffs OR restructuring OR cost reduction` -- are they under pressure to do more with less?
- `"{company_name}" earnings call data OR cloud OR AI OR efficiency` -- what leadership is telling investors
- `"{company_name}" news acquisition OR partnership OR product launch` -- recent events that create urgency or opportunity
- `"{company_name}" {industry} trends challenges 2026` -- macro industry pressures

For each signal found, classify it:

| Signal | Type | Pain Point | Urgency | Snowflake Feature Response |
|--------|------|-----------|---------|---------------------------|
| Hiring 3 data engineers | Staffing up | Manual pipeline work is bottlenecking the team | Medium | Cortex Code accelerates pipeline dev 5-10x |
| Q4 earnings: CEO said "AI is a top priority" | Executive mandate | Need to show AI progress to board | High | Cortex AI functions, ML in notebooks, Cortex Agents |
| Competitor launched real-time feature | Market pressure | Need faster data pipelines | High | Dynamic Tables, Snowpipe Streaming |

#### 2c. Internal Account Intelligence

Search local files for account context:
- `~/Desktop/Accounts/{Account}/` -- account folder for notes, prior demos, trackers
- `~/Desktop/Accounts/CAA_USE_CASE_MASTER.md` -- active use cases and pipeline notes
- Check for prior GAMEPLAN.md files from earlier demos

If Snowhouse access is available (via `account-discovery-analysis` skill or direct query), pull:
- **Consumption trajectory** -- are they growing, flat, or declining? Overage/underage prediction?
- **Feature adoption** -- what Snowflake features are they NOT using that map to their pain points?
- **Tech stack** -- what competing tools are in play? What can Snowflake consolidate?
- **Active SFDC use cases** -- what is already in the pipeline? What is stalled?

#### 2d. Build Pain-Point-to-Feature Map

For each of the 3 proposed use cases, build a structured mapping:

```
Use Case: [Name]

Customer Pain Point:
- What problem does the customer have today?
- Evidence: [hiring signal, earnings call quote, news event, tech stack gap, stalled use case]
- Who feels this pain? [role/team]
- Business cost of inaction: [time, money, risk, competitive disadvantage]

Snowflake Feature Response:
- Primary feature being demoed
- How it directly addresses the pain point
- Before/after contrast (what it looks like today vs. with Snowflake)

Business Value:
- Quantified or estimated impact (time saved, cost reduced, capability gained)
- Industry-relevant framing (e.g., for retail: "reduce time-to-insight from days to minutes during peak season")

Demo Story Arc:
- Open with the pain ("Your team currently spends X hours doing Y manually...")
- Show the feature solving it live
- Close with the business outcome
```

#### 2e. Compile Demo Brief

Assemble the research into a demo brief:
- Account name, industry, and current Snowflake footprint summary
- 3 pain-point-to-feature mappings (from 2d)
- Key audience personas and what they care about
- Recent events or signals that create urgency
- Competitive landscape (tools to position against)
- Proposed deck structure (slide count per section)
- Proposed repo structure (scripts and data per use case)
- Recommended demo narrative arc: which use case to lead with, which to close with

**MANDATORY STOPPING POINT**: Present the demo brief to the user for confirmation before proceeding. Highlight the pain-point-to-feature mappings for each use case.

### Step 3: Generate the Gameplan

**Goal:** Create an internal strategy document that ties every demo moment to business value.

**Actions:**

1. **Create** `GAMEPLAN.md` in the working directory with:
   - Demo overview: account, date, presenter, audience, demo duration
   - Objective: what outcome this demo should drive (specific next step, not "show Snowflake")
   - Account context summary:
     - Industry pressures and macro trends
     - Recent events / triggers (hiring, earnings, news, leadership changes)
     - Current tech stack and competitive landscape
     - Consumption trajectory and feature adoption gaps
   - Use case breakdown (for each of the 3 use cases):
     - **Customer pain point** (with evidence source)
     - **Who feels this pain** (role/persona in the room)
     - **Feature to demonstrate** and how it addresses the pain
     - **Business value narrative** (before/after, quantified if possible)
     - **Opening line** (the first thing to say when introducing this use case)
     - Key talking points
     - Expected audience reaction / questions
     - Objection handling (competitive positioning, pricing concerns, "we already have X")
     - Success criteria (what the audience should believe after this section)
   - Demo flow: ordered sequence of what to show, with time allocation per section
   - Risk factors and mitigation
   - Follow-up actions and next steps (specific, with owners and timelines)

**Output:** `GAMEPLAN.md` (INTERNAL)

### Step 4: Generate the Presentation Deck

**Goal:** Produce a branded PPTX file the user can upload directly to Google Slides.

**Skip this step if user chose "No slides".**

**Actions:**

1. **Generate** a slides JSON file following brand guidelines in `references/snowflake-brand-guidelines.md`:

   **Deck structure (target 15-20 slides, calibrate to demo duration):**
   - Slide 1: Cover slide (type: "cover") -- colorstack title, subtitle, presenter + date
   - Slide 2: Safe Harbor (type: "safe_harbor")
   - Slide 3: Your Snowflake Team (type: "speakers") -- speaker photos, names, and titles. If speaker photo URLs were provided in Step 1, include them in the `photo` field. Otherwise, Snowflake-branded initials are generated automatically.
   - Slide 4: Agenda (type: "agenda") -- use cases listed
   - Slides 4-5: Account context / why we are here (type: "content_1col") -- frame around customer pain points, not product features. "Here is what we are hearing from teams like yours..." Lead with their problem, not our solution.
   - Slide 6: Chapter title for Use Case 1 (type: "chapter", variant: "1")
   - Slides 7-8: Use Case 1 content (type: "content_1col" or "content_2col_titled")
   - Slide 9: Chapter title for Use Case 2 (type: "chapter", variant: "2")
   - Slides 10-11: Use Case 2 content
   - Slide 12: Chapter title for Use Case 3 (type: "chapter", variant: "3")
   - Slides 13-14: Use Case 3 content
   - Slide 15: Key takeaways (type: "content_3col_titled")
   - Slide 16: Next steps (type: "content_1col")
   - Slide 17: Thank you (type: "thank_you")

   **Available slide types for the JSON:**
   - `cover` -- fields: title_line1, title_line2 (colorstack), subtitle, presenter, date. **IMPORTANT: Do NOT put the company name in title_line1/title_line2 — the logo already identifies the customer. Use the title for the demo topic (e.g., "DATA PLATFORM" / "STRATEGY").**
   - `safe_harbor` -- no fields needed, clones the template safe harbor as-is
   - `speakers` -- fields: title, speakers (array of {name, title, email, photo, linkedin}). Photos can be direct URLs or LinkedIn profile URLs. If no photo is available, Snowflake-branded circular initials are generated automatically.
   - `agenda` -- fields: agenda_items (array of strings)
   - `chapter` -- fields: title_line1, title_line2 (colorstack), variant ("1"/"2"/"3")
   - `content_1col` -- fields: title, subtitle, body, icon (optional label for right-side icon)
   - `content_2col_titled` -- fields: title, subtitle, left_title, left_body, right_title, right_body
   - `content_3col_titled` -- fields: title, subtitle, col1_title, col1_body, col2_title, col2_body, col3_title, col3_body
   - `thank_you` -- fields: title_line1, title_line2 (colorstack), contact
   - All types support `speaker_notes`
   - The **first slide** in the JSON array should include `"logo_domain": "example.com"` for automatic logo fetching

2. **Write** the slides JSON to `slides.json` in the local save directory.

3. **Run** the PPTX generator:
   ```bash
   uv run --with python-pptx --with Pillow -- python3 \
     ~/.cortex/skills/demo-creation/scripts/generate_pptx.py \
     --template ~/.cortex/skills/demo-creation/assets/SNOWFLAKE_TEMPLATE_JANUARY_2026.pptx \
     --slides-json {save_dir}/slides.json \
     --output {save_dir}/{Account}_Demo.pptx
   ```
   If you have a local logo file, add `--logo {path_to_logo.png}`. If not, include `--logo-domain {domain}` or set `logo_domain` in the first slide of the JSON — the script will auto-fetch a real company logo and convert it to white for dark slide backgrounds.

4. **Confirm** the PPTX was generated and report the file path to the user. The user uploads this file directly to Google Slides with minimal editing needed.

**MANDATORY STOPPING POINT**: Present the slides JSON content outline to the user for review before generating the PPTX.

**Brand compliance checklist:**
- [ ] Cover slide uses colorstack (line 1 white on dark background, line 2 inherited)
- [ ] Chapter titles are ALL CAPS with colorstack (line 1 white, line 2 Snowflake Blue)
- [ ] Slide titles are Title Case (AP style)
- [ ] One key message per slide
- [ ] Safe Harbor is slide 2
- [ ] Speaker notes on every slide
- [ ] **Customer logo on the cover slide** (always required — use `--logo`, `--logo-domain`, or `logo_domain` in JSON)

**Formatting rules (enforced by `generate_pptx.py`):**

These rules are built into the generator. Do NOT change them without understanding the template coordinate system.

- **Logo placement:** Customer logo is placed top-right of the cover slide. Max height 500000 EMU (~0.55"). Aspect ratio preserved. The generator fetches real company logos automatically if `--logo-domain` or `logo_domain` JSON field is set. **Pipeline:** Uplead (no auth, 128px) → Clearbit → Google Favicon. All sources are converted to white via Pillow pixel manipulation for dark slide backgrounds. **Quality gate:** Fetched images smaller than 64x64px are rejected. **No text fallback** — if all sources fail, the deck is generated without a logo. Never generate text as a logo substitute.
- **Body text (1col):** Split into bullet paragraphs by sentence boundaries. Each bullet uses `•` character, 14pt font, 115% line spacing, 6pt space between bullets. Autofit mode is `noAutofit` (text does NOT shrink — overflows are caught by shape height expansion to FOOTER_TOP).
- **Body text (2col/3col):** Same bullet formatting as 1col but 11pt font. A `tIns` (top inset) of 500000 EMU is applied to body shapes to push text below the overlapping column title shapes. This is critical — without it, column titles overlap with the first bullet.
- **Column titles (2col/3col):** Separate shapes that sit ON TOP of the body shapes at the same vertical position (~1371600-1377600 EMU). They are NOT inside the body shape — they are independent shapes.
- **Autofit modes:** Titles use `normAutofit` (shrink to fit). Bodies use `noAutofit` (no shrinking, shape height expanded instead). Never use `spAutoFit` on body shapes.
- **Icons (1col only):** Vector group shapes from template slides 63-71. Placed at bottom-right of body area (ICON_SIZE=1500000 EMU). When an icon is present, body width shrinks to 6261300 EMU to avoid overlap. Icon labels are matched via fuzzy string matching with `ICON_LABEL_OVERRIDES` for known mismatches.
- **Agenda arrows:** Arrows are centered vertically in the text shape using 443089 EMU spacing. Excess arrows are removed to match item count.
- **Shape height expansion:** Body shapes are expanded to `FOOTER_TOP` (4600000 EMU) to maximize available space for bullet text.

**Business value checklist:**
- [ ] "Why We Are Here" slide references the customer's actual pain points (from Step 2 research), not generic product messaging
- [ ] Each use case section opens with the customer problem, not the Snowflake feature
- [ ] Speaker notes include the pain-point-to-feature bridge: "You told us X is a challenge. Here is how Y addresses that."
- [ ] Key takeaways slide maps each takeaway to a business outcome, not a product capability
- [ ] Next steps slide is specific and actionable (not "learn more" or "get in touch")

### Step 5: Provision Demo Environment and Scripts

**Goal:** Create the Snowflake demo environment and SQL scripts.

**Actions:**

1. **For each use case**, generate:
   - DDL scripts to create relevant tables
   - Sample data (INSERT statements or COPY commands)
   - Demo SQL scripts that walk through the use case
   - Each script should be self-contained, commented, and runnable

2. **Create** all scripts in a local `scripts/` directory:
   - `00_setup.sql` -- database, schema, warehouse setup
   - `01_{use_case_1_name}.sql`
   - `02_{use_case_2_name}.sql`
   - `03_{use_case_3_name}.sql`
   - `04_cleanup.sql` -- optional teardown

3. **Create** sample data files in a local `data/` directory:
   - DDL files for table creation
   - Sample data CSVs or INSERT statements

4. **Test** all scripts compile using `snowflake_sql_execute` with `only_compile=true`.

5. **Create** a `broken_{topic}_query.sql` file in `scripts/` with 3-4 intentional bugs (typos, missing columns, GROUP BY errors) for Exercise 1 of the quickstart guide.

**Output:** `scripts/` and `data/` directories with tested SQL.

### Step 6: Generate the Quickstart Guide

**Goal:** Create a self-paced quickstart document so the customer can return and work through the demo async.

**Actions:**

1. **Create** `quickstart_guide.md` in the working directory with this structure:
   - **Prerequisites** -- Snowflake account, role, warehouse, Cortex Code enabled
   - **Setup** -- run `00_setup.sql`, verify row counts
   - **Enable Cortex Code** -- how to open CoCo in Snowsight
   - **Understand the Demo Data** -- table descriptions, key columns, quick explore queries
   - **Exercise 1: Fix Broken SQL** (~5 min) -- paste the broken query, ask CoCo to fix it
   - **Exercise 2** (~15-20 min) -- corresponds to demo pillar 2 (e.g., ML workflow, forecasting, analytics)
   - **Exercise 3** (~10 min) -- corresponds to demo pillar 3 (e.g., agent building, Streamlit dashboard)
   - **Bonus Exercises** -- 3-4 prompts per persona (data engineers, analysts, data scientists, anyone)
   - **Tips and Troubleshooting** -- CoCo tips, common issues table, SQL quick reference
   - **Cleanup** -- run `04_cleanup.sql`, verify database is gone

2. **Adapt exercises to the account's use cases.** Each exercise should map to one of the three demo pillars. Exercise 1 is always "Fix Broken SQL" as a warmup. Exercises 2 and 3 correspond to the demo's second and third pillars.

3. **Include the broken SQL inline** in Exercise 1 and reference the file in `scripts/`.

4. **Contact info** at the bottom should be the presenter's email from Step 1.

**EXTERNAL classification** -- this file goes in the GitHub repo.

### Step 7: Create GitHub Repository


**Goal:** Package all external artifacts into a GitHub repo.

**Actions:**

1. **Confirm** GitHub CLI is authenticated:
   ```bash
   gh auth status
   ```

2. **Create** the repo named `demo-{account}-{date}` (lowercase, kebab-case):
   ```bash
   gh repo create {username}/demo-{account}-{date} --public --clone
   ```

3. **Create** `README.md` for the repo:
   - Demo title and overview
   - Use cases covered
   - Prerequisites (Snowflake account, warehouse, role)
   - Quick start instructions
   - File structure
   - Link to the Google Slides deck (if created)

4. **Populate** the repo with EXTERNAL artifacts only:
   - `README.md`
   - `quickstart_guide.md`
   - `scripts/` -- all SQL demo scripts (including broken query for Exercise 1)
   - `data/` -- DDL and sample data

   **DO NOT include:** GAMEPLAN.md or any INTERNAL artifacts.

5. **Commit and push**:
   ```bash
   git add . && git commit -m "Initial demo package for {Account Name}" && git push
   ```

6. **Return** the repo URL.

**MANDATORY STOPPING POINT**: Present the list of files to be pushed. Confirm NONE contain internal information. Ask user to review before pushing.

### Step 8: Final Summary

**Goal:** Present everything to the user.

**Actions:**

1. **Present** a summary of all artifacts created:

   **INTERNAL (local only):**
   - GAMEPLAN.md

   **EXTERNAL (customer-facing):**
   - PPTX deck (ready to upload to Google Slides)
   - Quickstart guide (self-paced walkthrough with 3 exercises)
   - GitHub repo URL
   - SQL scripts and sample data

   **Snowflake objects:** database, schema, tables (if provisioned)

2. **List** any follow-up items or manual steps needed.

## Stopping Points

- After Step 2: Demo brief confirmation
- After Step 4: Deck review before proceeding
- After Step 7: GitHub repo contents review before push

## Error Handling

- **GitHub CLI not authenticated**: Guide user to run `gh auth login`
- **Snowflake permission errors**: Ask user for correct role/warehouse
- **No account data found locally**: Ask user for industry, use cases, and audience context

## Tools and Scripts

- `scripts/generate_pptx.py` -- Generates branded PPTX from a slides JSON file using the Snowflake template. Requires `python-pptx`.
- Template: `assets/SNOWFLAKE_TEMPLATE_JANUARY_2026.pptx`

## Output

Complete demo creation package:
- Branded PPTX deck ready for upload to Google Slides
- Quickstart guide with 3 self-paced exercises and bonus prompts
- GitHub repo with SQL scripts, sample data, quickstart guide, and README
- Internal gameplan with strategy, talking points, and next steps
