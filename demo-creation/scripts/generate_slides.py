#!/usr/bin/env python3
"""Generate a branded Snowflake Google Slides deck using the Slides API.

Usage:
    uv run generate_slides.py \
        --title "DEMO TITLE" \
        --account "Account Name" \
        --presenter "First Last" \
        --date "March 2026" \
        --slides-json slides_content.json

The slides-json file should contain an array of slide objects. See README or
run with --help for the expected schema.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]

SCRIPT_DIR = Path(__file__).parent

COLORS = {
    "snowflake_blue": {"red": 0.161, "green": 0.710, "blue": 0.910},
    "midnight": {"red": 0.0, "green": 0.0, "blue": 0.0},
    "mid_blue": {"red": 0.067, "green": 0.337, "blue": 0.498},
    "medium_gray": {"red": 0.357, "green": 0.357, "blue": 0.357},
    "white": {"red": 1.0, "green": 1.0, "blue": 1.0},
    "star_blue": {"red": 0.459, "green": 0.804, "blue": 0.843},
    "valencia_orange": {"red": 1.0, "green": 0.624, "blue": 0.212},
    "first_light": {"red": 0.831, "green": 0.357, "blue": 0.565},
    "purple_moon": {"red": 0.447, "green": 0.329, "blue": 0.639},
}

PT = 12700  # 1 point in EMU

SLIDE_WIDTH = 9144000   # 10 inches
SLIDE_HEIGHT = 5143500  # 5.625 inches (16:9)

FONT_SIZES = {
    "deck_title": 44 * PT,
    "slide_title": 26 * PT,
    "subtitle": 18 * PT,
    "body": 18 * PT,
    "footer": 8 * PT,
    "paragraph_title": 18 * PT,
}

SAFE_HARBOR_TEXT = (
    "Other than statements of historical fact, all statements contained in these "
    "materials and any accompanying oral commentary (collectively, the \"Materials\") "
    "are forward-looking statements within the meaning of Section 27A of the Securities "
    "Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, "
    "as amended, including statements regarding (i) Snowflake's business strategy, plans, "
    "opportunities, or priorities; (ii) Snowflake's new or enhanced products, services, "
    "and technology offerings, including those that are under development or not generally "
    "available; (iii) market size and growth, trends, and competitive considerations; "
    "(iv) Snowflake's vision, strategy, and expected benefits relating to artificial "
    "intelligence (\"AI\"), Snowpark, Snowflake Marketplace, the AI Data Cloud, and AI "
    "Data Clouds for specific industries or product categories, including the expected "
    "benefits and network effects of the AI Data Cloud; and (v) the integration, "
    "interoperability, and availability of Snowflake's products, services, or technology "
    "offerings with or on third-party platforms or products, including public cloud "
    "platforms. These forward-looking statements are subject to a number of known and "
    "unknown risks, uncertainties, and assumptions. In light of these risks, the future "
    "events and trends discussed in the Materials may not occur, and actual results could "
    "differ materially and adversely from those expressed or implied. As a result, you "
    "should not rely on any forward-looking statements as predictions of future events.\n\n"
    "Any future product or roadmap information is intended to outline general product "
    "direction and is not a commitment, promise, or legal obligation to deliver any "
    "future products, features, or functionality."
)

SAFE_HARBOR_FOOTER = (
    "\u00a9 2026 Snowflake Inc. All rights reserved. Snowflake, the Snowflake logo, "
    "and all other Snowflake product, feature and service names mentioned in the "
    "Materials are registered trademarks or trademarks of Snowflake Inc. in the "
    "United States and other countries."
)


def get_credentials():
    creds = None
    token_path = SCRIPT_DIR / "token.json"
    creds_path = SCRIPT_DIR / "credentials.json"

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not creds_path.exists():
                print(
                    f"ERROR: credentials.json not found at {creds_path}\n"
                    "Please download OAuth credentials from Google Cloud Console\n"
                    "and place them at the path above.",
                    file=sys.stderr,
                )
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return creds


def rgb(color_name):
    return {"rgbColor": COLORS[color_name]}


def create_text_style(font_size, color_name, bold=False):
    style = {
        "fontSize": {"magnitude": font_size / PT, "unit": "PT"},
        "foregroundColor": {"opaqueColor": rgb(color_name)},
        "fontFamily": "Arial",
        "bold": bold,
    }
    return style


def add_text_box(requests, page_id, object_id, text, x, y, w, h,
                 font_size, color_name, bold=False, alignment="START",
                 line_spacing=None, space_above=None, space_below=None):
    requests.append({
        "createShape": {
            "objectId": object_id,
            "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": page_id,
                "size": {
                    "width": {"magnitude": w, "unit": "EMU"},
                    "height": {"magnitude": h, "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1, "scaleY": 1,
                    "translateX": x, "translateY": y,
                    "unit": "EMU",
                },
            },
        }
    })
    requests.append({
        "insertText": {
            "objectId": object_id,
            "text": text,
            "insertionIndex": 0,
        }
    })
    style_req = {
        "updateTextStyle": {
            "objectId": object_id,
            "style": create_text_style(font_size, color_name, bold),
            "fields": "fontSize,foregroundColor,fontFamily,bold",
        }
    }
    requests.append(style_req)

    para_style = {"alignment": alignment}
    fields = ["alignment"]
    if line_spacing is not None:
        para_style["lineSpacing"] = line_spacing * 100
        fields.append("lineSpacing")
    if space_above is not None:
        para_style["spaceAbove"] = {"magnitude": space_above, "unit": "PT"}
        fields.append("spaceAbove")
    if space_below is not None:
        para_style["spaceBelow"] = {"magnitude": space_below, "unit": "PT"}
        fields.append("spaceBelow")

    requests.append({
        "updateParagraphStyle": {
            "objectId": object_id,
            "style": para_style,
            "fields": ",".join(fields),
        }
    })


def add_footer(requests, page_id, slide_num, id_prefix):
    footer_text = f"\u00a9 2026 Snowflake Inc. All Rights Reserved"
    add_text_box(
        requests, page_id, f"{id_prefix}_footer",
        footer_text,
        x=400000, y=4900000, w=5000000, h=200000,
        font_size=FONT_SIZES["footer"], color_name="medium_gray",
    )
    add_text_box(
        requests, page_id, f"{id_prefix}_pagenum",
        str(slide_num),
        x=8700000, y=4900000, w=300000, h=200000,
        font_size=FONT_SIZES["footer"], color_name="medium_gray",
        alignment="END",
    )


def set_background(requests, page_id, color_name):
    requests.append({
        "updatePageProperties": {
            "objectId": page_id,
            "pageProperties": {
                "pageBackgroundFill": {
                    "solidFill": {
                        "color": rgb(color_name),
                    }
                }
            },
            "fields": "pageBackgroundFill.solidFill.color",
        }
    })


def add_cover_slide(requests, page_id, title, subtitle, presenter, date):
    set_background(requests, page_id, "snowflake_blue")

    title_upper = title.upper()
    words = title_upper.split()
    mid = len(words) // 2
    line1 = " ".join(words[:mid]) if mid > 0 else title_upper
    line2 = " ".join(words[mid:]) if mid > 0 else ""
    full_title = f"{line1}\n{line2}" if line2 else title_upper

    add_text_box(
        requests, page_id, f"{page_id}_title",
        full_title,
        x=400000, y=1500000, w=7500000, h=1800000,
        font_size=FONT_SIZES["deck_title"], color_name="midnight", bold=True,
    )

    if subtitle:
        add_text_box(
            requests, page_id, f"{page_id}_subtitle",
            subtitle,
            x=400000, y=3300000, w=7000000, h=400000,
            font_size=FONT_SIZES["subtitle"], color_name="white", bold=True,
        )

    presenter_date = f"{presenter}  |  {date}" if presenter and date else presenter or date or ""
    if presenter_date:
        add_text_box(
            requests, page_id, f"{page_id}_presenter",
            presenter_date,
            x=400000, y=4400000, w=5000000, h=300000,
            font_size=FONT_SIZES["subtitle"], color_name="midnight",
        )

    add_text_box(
        requests, page_id, f"{page_id}_copyright",
        "\u00a9 2026 Snowflake Inc. All Rights Reserved",
        x=400000, y=4900000, w=5000000, h=200000,
        font_size=FONT_SIZES["footer"], color_name="white",
    )


def add_safe_harbor_slide(requests, page_id, slide_num):
    add_text_box(
        requests, page_id, f"{page_id}_title",
        "Safe Harbor and Disclaimers",
        x=400000, y=200000, w=8000000, h=500000,
        font_size=FONT_SIZES["slide_title"], color_name="midnight", bold=True,
    )
    add_text_box(
        requests, page_id, f"{page_id}_body",
        SAFE_HARBOR_TEXT,
        x=400000, y=800000, w=8200000, h=3500000,
        font_size=10 * PT, color_name="medium_gray",
        line_spacing=1.15, space_above=0, space_below=10,
    )
    add_text_box(
        requests, page_id, f"{page_id}_legal",
        SAFE_HARBOR_FOOTER,
        x=400000, y=4500000, w=8200000, h=400000,
        font_size=6 * PT, color_name="medium_gray",
    )
    add_footer(requests, page_id, slide_num, page_id)


def add_chapter_slide(requests, page_id, title, slide_num):
    set_background(requests, page_id, "mid_blue")

    title_upper = title.upper()
    words = title_upper.split()
    mid = len(words) // 2
    line1 = " ".join(words[:mid]) if mid > 0 else title_upper
    line2 = " ".join(words[mid:]) if mid > 0 else ""
    full_title = f"{line1}\n{line2}" if line2 else title_upper

    add_text_box(
        requests, page_id, f"{page_id}_title_l1",
        line1,
        x=400000, y=2000000, w=7500000, h=600000,
        font_size=FONT_SIZES["deck_title"], color_name="white", bold=True,
    )
    if line2:
        add_text_box(
            requests, page_id, f"{page_id}_title_l2",
            line2,
            x=400000, y=2600000, w=7500000, h=600000,
            font_size=FONT_SIZES["deck_title"], color_name="snowflake_blue", bold=True,
        )

    add_text_box(
        requests, page_id, f"{page_id}_copyright",
        "\u00a9 2026 Snowflake Inc. All Rights Reserved",
        x=400000, y=4900000, w=5000000, h=200000,
        font_size=FONT_SIZES["footer"], color_name="white",
    )


def add_content_slide(requests, page_id, title, body, subtitle=None, slide_num=1):
    requests.append({
        "createShape": {
            "objectId": f"{page_id}_accent",
            "shapeType": "RECTANGLE",
            "elementProperties": {
                "pageObjectId": page_id,
                "size": {
                    "width": {"magnitude": 50000, "unit": "EMU"},
                    "height": {"magnitude": 500000, "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1, "scaleY": 1,
                    "translateX": 200000, "translateY": 200000,
                    "unit": "EMU",
                },
            },
        }
    })
    requests.append({
        "updateShapeProperties": {
            "objectId": f"{page_id}_accent",
            "shapeProperties": {
                "shapeBackgroundFill": {
                    "solidFill": {"color": rgb("snowflake_blue")}
                },
                "outline": {"outlineFill": {"solidFill": {"color": rgb("snowflake_blue")}}, "weight": {"magnitude": 0, "unit": "PT"}},
            },
            "fields": "shapeBackgroundFill.solidFill.color,outline",
        }
    })

    add_text_box(
        requests, page_id, f"{page_id}_title",
        title,
        x=400000, y=200000, w=8200000, h=500000,
        font_size=FONT_SIZES["slide_title"], color_name="midnight", bold=True,
    )

    body_y = 750000
    if subtitle:
        add_text_box(
            requests, page_id, f"{page_id}_subtitle",
            subtitle,
            x=400000, y=700000, w=8200000, h=300000,
            font_size=FONT_SIZES["subtitle"], color_name="medium_gray",
        )
        body_y = 1100000

    add_text_box(
        requests, page_id, f"{page_id}_body",
        body,
        x=400000, y=body_y, w=8200000, h=3600000 - (body_y - 750000),
        font_size=FONT_SIZES["body"], color_name="medium_gray",
        line_spacing=1.15, space_above=0, space_below=10,
    )

    add_footer(requests, page_id, slide_num, page_id)


def add_agenda_slide(requests, page_id, items, slide_num):
    set_background(requests, page_id, "mid_blue")

    add_text_box(
        requests, page_id, f"{page_id}_title",
        "Agenda",
        x=200000, y=200000, w=2500000, h=500000,
        font_size=FONT_SIZES["slide_title"], color_name="midnight", bold=True,
    )

    requests.append({
        "createShape": {
            "objectId": f"{page_id}_left_bg",
            "shapeType": "RECTANGLE",
            "elementProperties": {
                "pageObjectId": page_id,
                "size": {
                    "width": {"magnitude": 3000000, "unit": "EMU"},
                    "height": {"magnitude": SLIDE_HEIGHT, "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1, "scaleY": 1,
                    "translateX": 0, "translateY": 0,
                    "unit": "EMU",
                },
            },
        }
    })
    requests.append({
        "updateShapeProperties": {
            "objectId": f"{page_id}_left_bg",
            "shapeProperties": {
                "shapeBackgroundFill": {
                    "solidFill": {"color": rgb("white")}
                },
                "outline": {"outlineFill": {"solidFill": {"color": rgb("white")}}, "weight": {"magnitude": 0, "unit": "PT"}},
            },
            "fields": "shapeBackgroundFill.solidFill.color,outline",
        }
    })

    agenda_text = "\n".join(f">  {item}" for item in items)
    add_text_box(
        requests, page_id, f"{page_id}_items",
        agenda_text,
        x=3500000, y=1000000, w=5000000, h=3500000,
        font_size=FONT_SIZES["body"], color_name="white",
        line_spacing=2.0,
    )

    add_text_box(
        requests, page_id, f"{page_id}_copyright",
        "\u00a9 2026 Snowflake Inc. All Rights Reserved",
        x=400000, y=4900000, w=5000000, h=200000,
        font_size=FONT_SIZES["footer"], color_name="medium_gray",
    )


def add_three_column_slide(requests, page_id, title, columns, slide_num):
    add_text_box(
        requests, page_id, f"{page_id}_title",
        title,
        x=400000, y=200000, w=8200000, h=500000,
        font_size=FONT_SIZES["slide_title"], color_name="midnight", bold=True,
    )

    requests.append({
        "createShape": {
            "objectId": f"{page_id}_accent",
            "shapeType": "RECTANGLE",
            "elementProperties": {
                "pageObjectId": page_id,
                "size": {
                    "width": {"magnitude": 50000, "unit": "EMU"},
                    "height": {"magnitude": 500000, "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1, "scaleY": 1,
                    "translateX": 200000, "translateY": 200000,
                    "unit": "EMU",
                },
            },
        }
    })
    requests.append({
        "updateShapeProperties": {
            "objectId": f"{page_id}_accent",
            "shapeProperties": {
                "shapeBackgroundFill": {
                    "solidFill": {"color": rgb("snowflake_blue")}
                },
                "outline": {"outlineFill": {"solidFill": {"color": rgb("snowflake_blue")}}, "weight": {"magnitude": 0, "unit": "PT"}},
            },
            "fields": "shapeBackgroundFill.solidFill.color,outline",
        }
    })

    col_width = 2600000
    col_gap = 200000
    start_x = 400000

    for i, col in enumerate(columns[:3]):
        col_x = start_x + i * (col_width + col_gap)
        col_title = col.get("title", "")
        col_body = col.get("body", "")

        if col_title:
            add_text_box(
                requests, page_id, f"{page_id}_col{i}_title",
                col_title,
                x=col_x, y=900000, w=col_width, h=400000,
                font_size=FONT_SIZES["paragraph_title"], color_name="mid_blue", bold=True,
            )

        add_text_box(
            requests, page_id, f"{page_id}_col{i}_body",
            col_body,
            x=col_x, y=1400000, w=col_width, h=3000000,
            font_size=FONT_SIZES["body"], color_name="medium_gray",
            line_spacing=1.15, space_above=0, space_below=10,
        )

    add_footer(requests, page_id, slide_num, page_id)


def add_thank_you_slide(requests, page_id, slide_num):
    set_background(requests, page_id, "snowflake_blue")
    add_text_box(
        requests, page_id, f"{page_id}_title_l1",
        "THANK",
        x=400000, y=1800000, w=7500000, h=700000,
        font_size=FONT_SIZES["deck_title"], color_name="midnight", bold=True,
    )
    add_text_box(
        requests, page_id, f"{page_id}_title_l2",
        "YOU",
        x=400000, y=2500000, w=7500000, h=700000,
        font_size=FONT_SIZES["deck_title"], color_name="white", bold=True,
    )
    add_text_box(
        requests, page_id, f"{page_id}_copyright",
        "\u00a9 2026 Snowflake Inc. All Rights Reserved",
        x=400000, y=4900000, w=5000000, h=200000,
        font_size=FONT_SIZES["footer"], color_name="white",
    )


def build_deck(slides_service, title, account, presenter, date, slides_content):
    presentation = slides_service.presentations().create(body={"title": f"{account} - {title}"}).execute()
    pres_id = presentation["presentationId"]

    first_slide_id = presentation["slides"][0]["objectId"]

    requests = []
    page_ids = []

    for i in range(len(slides_content)):
        pid = f"slide_{i+1:03d}"
        page_ids.append(pid)
        requests.append({"createSlide": {"objectId": pid, "insertionIndex": i + 1}})

    requests.append({"deleteObject": {"objectId": first_slide_id}})

    slides_service.presentations().batchUpdate(
        presentationId=pres_id, body={"requests": requests}
    ).execute()

    content_requests = []
    slide_num = 1

    for i, slide_def in enumerate(slides_content):
        pid = page_ids[i]
        stype = slide_def.get("type", "content")

        if stype == "cover":
            add_cover_slide(
                content_requests, pid,
                slide_def.get("title", title),
                slide_def.get("subtitle", account),
                slide_def.get("presenter", presenter),
                slide_def.get("date", date),
            )
        elif stype == "safe_harbor":
            add_safe_harbor_slide(content_requests, pid, slide_num)
        elif stype == "agenda":
            add_agenda_slide(content_requests, pid, slide_def.get("items", []), slide_num)
        elif stype == "chapter":
            add_chapter_slide(content_requests, pid, slide_def.get("title", ""), slide_num)
        elif stype == "content":
            add_content_slide(
                content_requests, pid,
                slide_def.get("title", ""),
                slide_def.get("body", ""),
                slide_def.get("subtitle"),
                slide_num,
            )
        elif stype == "three_column":
            add_three_column_slide(
                content_requests, pid,
                slide_def.get("title", ""),
                slide_def.get("columns", []),
                slide_num,
            )
        elif stype == "thank_you":
            add_thank_you_slide(content_requests, pid, slide_num)
        else:
            add_content_slide(
                content_requests, pid,
                slide_def.get("title", "Untitled"),
                slide_def.get("body", ""),
                slide_def.get("subtitle"),
                slide_num,
            )

        slide_num += 1

    if content_requests:
        batch_size = 50
        for j in range(0, len(content_requests), batch_size):
            batch = content_requests[j:j + batch_size]
            slides_service.presentations().batchUpdate(
                presentationId=pres_id, body={"requests": batch}
            ).execute()

    return pres_id


def main():
    parser = argparse.ArgumentParser(description="Generate branded Snowflake Google Slides deck")
    parser.add_argument("--title", required=True, help="Deck title")
    parser.add_argument("--account", required=True, help="Account name")
    parser.add_argument("--presenter", default="", help="Presenter name")
    parser.add_argument("--date", default="", help="Presentation date")
    parser.add_argument("--slides-json", required=True, help="Path to JSON file or inline JSON with slide content")
    args = parser.parse_args()

    if os.path.isfile(args.slides_json):
        with open(args.slides_json) as f:
            slides_content = json.load(f)
    else:
        slides_content = json.loads(args.slides_json)

    creds = get_credentials()
    service = build("slides", "v1", credentials=creds)

    pres_id = build_deck(service, args.title, args.account, args.presenter, args.date, slides_content)

    url = f"https://docs.google.com/presentation/d/{pres_id}/edit"
    print(f"Deck created: {url}")
    return url


if __name__ == "__main__":
    main()
