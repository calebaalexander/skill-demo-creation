# Demo Creation Skill for Cortex Code

A [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) skill that generates complete, branded demo packages for Snowflake customer presentations.

**What it produces:**
- Branded PPTX deck (ready to upload to Google Slides)
- Internal gameplan with strategy, talking points, and objection handling
- SQL demo scripts with sample data
- Self-paced quickstart guide for leave-behind
- GitHub repo with all customer-facing artifacts

## Install

```bash
git clone https://github.com/calebaalexander/skill-demo-creation.git
cd skill-demo-creation
./install.sh
```

This copies the skill to `~/.snowflake/cortex/skills/demo-creation/`. Restart Cortex Code and the skill will be available immediately.

### Manual Install

If you prefer, just copy the `demo-creation/` folder directly:

```bash
cp -R demo-creation ~/.snowflake/cortex/skills/demo-creation
```

## Usage

Open Cortex Code and say:

```
$demo-creation create a demo for Acme Corp
```

Or just say "create a demo for [account]" -- the skill auto-triggers on keywords like: *create demo, build demo, demo deck, demo slides, demo package*.

The skill will walk you through:
1. Gathering account name, use cases, audience, and preferences
2. Researching the account (web + internal data if available)
3. Generating a strategy gameplan (INTERNAL)
4. Building a branded PPTX deck
5. Creating SQL scripts and sample data
6. Packaging everything into a GitHub repo

## What's Included

```
demo-creation/
├── SKILL.md                          # Skill definition (workflow, rules, formatting)
├── assets/
│   └── SNOWFLAKE_TEMPLATE_JANUARY_2026.pptx  # 72-slide branded master template
├── scripts/
│   ├── generate_pptx.py              # PPTX generator (python-pptx)
│   └── generate_slides.py            # Google Slides API generator (alternative)
├── references/
│   └── snowflake-brand-guidelines.md # Brand colors, fonts, layout rules
└── examples/
    └── slides.json                   # Example slide content JSON
```

### Template Details

The PPTX template (`SNOWFLAKE_TEMPLATE_JANUARY_2026.pptx`) contains 72+ master slides including:

| Slide Type | Template Index | Fields |
|---|---|---|
| `cover` | 19 | title_line1, title_line2, subtitle, presenter, date |
| `safe_harbor` | 2 | (none -- cloned as-is) |
| `agenda` | 44 | agenda_items[] |
| `chapter` | 22/23/24 | title_line1, title_line2, variant (1/2/3) |
| `content_1col` | 32 | title, subtitle, body, icon |
| `content_2col_titled` | 34 | title, subtitle, left_title, left_body, right_title, right_body |
| `content_3col_titled` | 36 | title, subtitle, col1_title/body, col2_title/body, col3_title/body |
| `thank_you` | 72 | title_line1, title_line2, contact |

Vector icons are embedded in template slides 63-71 (Performance Scale, Security, Users, Cloud, Snowflake Intelligence, Launch, etc.) and automatically matched by label via fuzzy string matching.

### Formatting Engine

The `generate_pptx.py` script handles all formatting automatically:

- **Customer logo**: Auto-fetched via Clearbit/Google Favicon from `logo_domain` in the JSON, or pass `--logo` for a local file
- **Body text**: Split into bullet paragraphs by sentence. `•` character, 14pt (1col) or 11pt (2col/3col), 115% line spacing
- **2col/3col layouts**: Column titles are separate shapes overlaying body shapes. A 500K EMU top inset pushes body text below titles
- **Autofit**: Titles shrink-to-fit (`normAutofit`), bodies never shrink (`noAutofit`, height expanded instead)
- **Icons**: 1.65" vector icons placed bottom-right of body area on `content_1col` slides
- **Agenda arrows**: Auto-centered vertically with consistent spacing, excess arrows removed

## Slides JSON Format

The deck content is defined in a JSON array. See `examples/slides.json` for a complete example.

Key points:
- The **first slide** should include `"logo_domain": "company.com"` for automatic logo fetching
- All slide types support `"speaker_notes"` 
- Body text is automatically split into bullets at sentence boundaries (period + space)
- Chapter titles use "colorstack" -- line 1 is white, line 2 is Snowflake Blue

## Running the Generator Standalone

You can run the PPTX generator directly without the full skill workflow:

```bash
uv run --with python-pptx --with Pillow -- python3 \
  ~/.snowflake/cortex/skills/demo-creation/scripts/generate_pptx.py \
  --template ~/.snowflake/cortex/skills/demo-creation/assets/SNOWFLAKE_TEMPLATE_JANUARY_2026.pptx \
  --slides-json slides.json \
  --output My_Demo.pptx \
  --logo-domain acmecorp.com
```

Or with a local logo:
```bash
uv run --with python-pptx --with Pillow -- python3 \
  ~/.snowflake/cortex/skills/demo-creation/scripts/generate_pptx.py \
  --template ~/.snowflake/cortex/skills/demo-creation/assets/SNOWFLAKE_TEMPLATE_JANUARY_2026.pptx \
  --slides-json slides.json \
  --output My_Demo.pptx \
  --logo ./customer_logo.png
```

## Dependencies

Installed automatically when the skill runs (via `uv`):
- `python-pptx` -- PPTX generation
- `Pillow` -- Image processing for logo placement

No manual pip install needed.

## Customization

**Adding icons**: Add new icon slides to the template PPTX (slides 63+). Each icon slide should have a text label shape and a vector group shape. The generator indexes them automatically.

**Changing formatting**: Edit the constants at the top of `generate_pptx.py`:
- `FOOTER_TOP` -- Bottom boundary for body text expansion
- `ICON_SIZE` -- Icon dimensions
- `LOGO_MAX_HEIGHT` -- Customer logo size on cover slide
- `ICON_LABEL_OVERRIDES` -- Remap icon labels for better fuzzy matching

**Adding slide types**: Add a new `apply_*` function in `generate_pptx.py`, map it in the `APPLY_FN` dict, and add the template index in `template_index_for_type`.
