# Snowflake Brand Guidelines for Presentations

Source: Snowflake Template January 2026

## Colors

### Primary Palette
| Name | Hex | Usage |
|------|-----|-------|
| Snowflake Blue | #29B5E8 | Primary brand, cover backgrounds |
| Midnight | #000000 | Titles on light backgrounds |
| Mid-Blue | #11567F | Accent, sections, chapter backgrounds |
| Medium Gray | #5B5B5B | Subheads and body copy |

### Secondary Palette (use sparingly)
| Name | Hex |
|------|-----|
| Star Blue | #75CDD7 |
| Valencia Orange | #FF9F36 |
| First Light | #D45B90 |
| Purple Moon | #7254A3 |

### Text Contrast Rules
- Black text on: Snowflake Blue, Star Blue, Valencia Orange, First Light
- White text on: Midnight, Mid-Blue, Medium Gray, Purple Moon
- Snowflake Blue as text color: minimum 28pt font size
- Never use Star Blue, Valencia Orange, First Light, or Purple Moon as text colors

## Typography

Font family: Arial only (Bold and Regular)

### Deck and Chapter Titles
- Arial Bold, 44pt, ALL CAPS
- Colorstack styling required:
  - On Snowflake Blue background: black text + white text
  - On Mid-Blue background: Snowflake Blue text + white text
  - The word "Snowflake" should be white when possible
  - Do not use alternate colors in colorstack
  - Do not split highlighted text across lines

### Slide Titles
- Arial Bold, 26pt, black (#000000)
- Title Case (AP style): capitalize words of 4+ letters, plus "To" and "In"
- Never ALL CAPS on slide titles
- Left-aligned

### Subtitles
- Arial Regular, 18pt, Medium Gray (#5B5B5B)

### Paragraph Titles
- Arial Bold, 18pt, Mid-Blue (#11567F)

### Body Copy
- Arial Regular, 18pt, Medium Gray (#5B5B5B)
- Line spacing: 1.15 (custom)
- Paragraph spacing: 0pt before, 10pt after
- Left-aligned

## Layout Rules

### General
- One key message per slide
- Embrace white space
- Left-aligned text throughout (including slide titles)
- 40-60 characters per line for body text
- 15-40 characters per line for narrow columns

### Content Guidelines
- Prefer short paragraphs without bullets
- Avoid sub-bullets
- No underlining except for web links
- Use high-quality images only
- Keep slides simple and uncluttered

### Footer (every slide)
- Snowflake logo (small, bottom-left)
- "© 2026 Snowflake Inc. All Rights Reserved"
- Page number (bottom-right)

## Slide Types for Deck Generation

### 1. Cover Slide (Snowflake Blue background)
- Snowflake logo top-left (white)
- Title: Arial Bold, 44pt, ALL CAPS, colorstack (black + white)
- Subtitle: Arial Bold, 18pt
- Presenter name and date: bottom-left
- Background: wave or dot pattern graphics

### 2. Cover Slide with Customer Logo
- Left ~60%: Snowflake Blue with title (colorstack)
- Right ~40%: white background with customer logo centered
- Subtitle below title
- Presenter name and date: bottom-left

### 3. Safe Harbor Slide
- Standard legal disclaimer text
- Must be slide 2 in any external deck
- REV 12.16.25

### 4. Agenda Slide
- Split layout: white left panel with "Agenda" title
- Mid-Blue right panel with arrow bullet items
- Snowflake arrow bullets (>) in Snowflake Blue

### 5. Chapter/Section Title Slide (Mid-Blue background)
- Title: Arial Bold, 44pt, ALL CAPS, colorstack (white + Snowflake Blue)
- Various background options: plain, dot pattern, wave pattern
- No body text

### 6. Content Slides (white background)
- Cyan accent bar on left edge of title
- Title: Arial Bold, 26pt, black, Title Case
- Optional subtitle: Arial, 18pt, medium gray
- Body area below

### 7. Column Layouts
- One column: full-width text
- Two columns: side-by-side text blocks
- Three columns: with optional icons or paragraph titles
- Four columns: with big numbers or icons

### 8. Split Slide
- Left half: image or graphic
- Right half: Mid-Blue background with white text

### 9. Quote Slides
- Large quotation marks in Snowflake Blue
- Quote text: white bold on Mid-Blue bg (or black on white bg)
- Attribution: Name | Title, Company Name

### 10. Thank You / Closing Slide
- Snowflake Blue background
- "THANK YOU" in colorstack
- Contact info or next steps

## Google Slides API Color Values (RGB 0-1 scale)

| Color | R | G | B |
|-------|---|---|---|
| Snowflake Blue #29B5E8 | 0.161 | 0.710 | 0.910 |
| Midnight #000000 | 0.0 | 0.0 | 0.0 |
| Mid-Blue #11567F | 0.067 | 0.337 | 0.498 |
| Medium Gray #5B5B5B | 0.357 | 0.357 | 0.357 |
| White #FFFFFF | 1.0 | 1.0 | 1.0 |
| Star Blue #75CDD7 | 0.459 | 0.804 | 0.843 |
| Valencia Orange #FF9F36 | 1.0 | 0.624 | 0.212 |
| First Light #D45B90 | 0.831 | 0.357 | 0.565 |
| Purple Moon #7254A3 | 0.447 | 0.329 | 0.639 |

## Google Slides API Font Size Values (EMU conversion)

| Element | Points | EMU (pt * 12700) |
|---------|--------|------------------|
| Deck/Chapter title | 44 | 558800 |
| Slide title | 26 | 330200 |
| Subtitle | 18 | 228600 |
| Body copy | 18 | 228600 |
| Paragraph title | 18 | 228600 |

## Template Source Presentation
- Google Slides ID: 1a8SBT4SRc8IUsYYiV3n81_y0HoHtYtJG1dK_Qwhr7w8
- Use this as the source for copying slide layouts via the Slides API
