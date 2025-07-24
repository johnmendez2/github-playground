import os 

def create_presentation(service, drive_service, title: str) -> str:
    """
    Creates a new Google Slides presentation if one with the same name doesn't exist.

    Parameters:
    - service: Authenticated Slides API service
    - drive_service: Authenticated Drive API service
    - title (str): Title of the new presentation

    Returns:
    - str: URL of the newly created presentation

    Raises:
    - ValueError: If a presentation with the same name already exists
    """
    # Check if a file with the same name exists
    response = drive_service.files().list(
        q=f"name='{title}' and mimeType='application/vnd.google-apps.presentation'",
        spaces='drive',
        fields="files(id, name)"
    ).execute()

    files = response.get("files", [])
    if files:
        raise ValueError(f"A presentation named '{title}' already exists.")

    presentation = service.presentations().create(
        body={"title": title}
    ).execute()

    presentation_id = presentation["presentationId"]
    return f"https://docs.google.com/presentation/d/{presentation_id}"



from typing import Any

def find_presentation_id_by_name(drive_service: Any, name: str) -> str:
    """
    Finds a presentation's ID by its name using the Drive API.
    Returns the first match.
    """
    response = drive_service.files().list(
        q=f"name='{name}' and mimeType='application/vnd.google-apps.presentation'",
        fields="files(id, name)",
        spaces='drive'
    ).execute()

    files = response.get("files", [])
    if not files:
        raise ValueError(f"No presentation found with name: {name}")
    return files[0]["id"]

def add_blank_slide(service, presentation_id: str) -> str:
    """
    Adds a blank slide to a presentation using its ID.
    """
    requests = [
        {
            "createSlide": {
                "slideLayoutReference": {
                    "predefinedLayout": "BLANK"
                }
            }
        }
    ]
    response = service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()

    return response.get("replies", [])[0]["createSlide"]["objectId"]

# tools.py
import os
import re

def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def parse_bold_spans(text: str):
    spans = []
    clean_text = ""
    i = 0
    while i < len(text):
        if text[i:i+2] == "**":
            start = len(clean_text)
            i += 2
            while i < len(text) and text[i:i+2] != "**":
                clean_text += text[i]
                i += 1
            end = len(clean_text)
            spans.append((start, end))
            i += 2
        else:
            clean_text += text[i]
            i += 1
    return clean_text, spans

def insert_text_on_slide(service, presentation_id: str, text: str, slide_index: int = -1,
                         font_family: str = "Arial", font_size: int = 18, color: str = "#000000",
                         align: str = "center", bullet: bool = False) -> str:
    rgb = hex_to_rgb(color)
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get("slides", [])
    if not slides:
        raise ValueError("The presentation has no slides.")
    slide_id = slides[slide_index]["objectId"]

    text_box_id = f"textbox_{int(os.urandom(2).hex(), 16)}"
    plain_text, bold_spans = parse_bold_spans(text)

    requests = [
        {
            "createShape": {
                "objectId": text_box_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": 100, "unit": "PT"},
                        "width": {"magnitude": 400, "unit": "PT"}
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 50,
                        "translateY": 100,
                        "unit": "PT"
                    }
                }
            }
        },
        {
            "insertText": {
                "objectId": text_box_id,
                "insertionIndex": 0,
                "text": plain_text
            }
        },
        {
            "updateTextStyle": {
                "objectId": text_box_id,
                "style": {
                    "fontFamily": font_family,
                    "fontSize": {
                        "magnitude": font_size,
                        "unit": "PT"
                    },
                    "foregroundColor": {
                        "opaqueColor": {
                            "rgbColor": {
                                "red": rgb[0],
                                "green": rgb[1],
                                "blue": rgb[2]
                            }
                        }
                    }
                },
                "textRange": {
                    "type": "ALL"
                },
                "fields": "fontFamily,fontSize,foregroundColor"
            }
        },
        {
            "updateParagraphStyle": {
                "objectId": text_box_id,
                "style": {
                    "alignment": align.upper()
                },
                "textRange": {
                    "type": "ALL"
                },
                "fields": "alignment"
            }
        }
    ]

    for start, end in bold_spans:
        requests.append({
            "updateTextStyle": {
                "objectId": text_box_id,
                "style": {"bold": True},
                "textRange": {
                    "type": "FIXED_RANGE",
                    "startIndex": start,
                    "endIndex": end
                },
                "fields": "bold"
            }
        })

    if bullet:
        requests.append({
            "createParagraphBullets": {
                "objectId": text_box_id,
                "textRange": {"type": "ALL"},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
            }
        })

    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()

    return text_box_id

# tools.py (continuation with 4 new tools + name-or-id resolver)
import requests
import uuid
from typing import Optional

# Tool 2: Get presentation metadata
def get_presentation_metadata(service, drive_service, presentation_id: str) -> dict:
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    file = drive_service.files().get(
        fileId=presentation_id,
        fields="id, name, createdTime, modifiedTime"
    ).execute()

    return {
        "title": file["name"],
        "presentation_id": file["id"],
        "created": file["createdTime"],
        "modified": file["modifiedTime"],
        "slide_count": len(presentation.get("slides", []))
    }

# Tool 3: Insert image from URL into a slide
def insert_image_on_slide(service, presentation_id: str, image_url: str, slide_index: int = -1,
                           width: int = 300, height: int = 200, x_offset: int = 50, y_offset: int = 100) -> str:
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get("slides", [])
    if not slides:
        raise ValueError("No slides available to insert the image.")
    slide_id = slides[slide_index]["objectId"]
    image_id = f"image_{uuid.uuid4().hex[:8]}"

    requests = [
        {
            "createImage": {
                "objectId": image_id,
                "url": image_url,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "height": {"magnitude": height, "unit": "PT"},
                        "width": {"magnitude": width, "unit": "PT"}
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": x_offset,
                        "translateY": y_offset,
                        "unit": "PT"
                    }
                }
            }
        }
    ]

    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()
    return image_id

# Tool 4: List slides
def list_slides(service, presentation_id: str) -> list:
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get("slides", [])

    slide_data = []

    for i, slide in enumerate(slides):
        slide_info = {
            "index": i,
            "objectId": slide.get("objectId"),
            "notesPageId": slide.get("notesPage", {}).get("objectId"),
            "texts": []
        }

        # Extract all text from shapes
        for element in slide.get("pageElements", []):
            shape = element.get("shape")
            if shape:
                text_elements = shape.get("text", {}).get("textElements", [])
                for text_element in text_elements:
                    text_run = text_element.get("textRun")
                    if text_run:
                        content = text_run.get("content", "").strip()
                        if content:
                            slide_info["texts"].append(content)

        slide_data.append(slide_info)

    return slide_data


# ID Resolver Helper
def resolve_presentation_id(drive_service, presentation_id: Optional[str], presentation_name: Optional[str]) -> str:
    if not presentation_id and not presentation_name:
        raise ValueError("Either 'presentation_id' or 'presentation_name' must be provided.")
    if presentation_id:
        return presentation_id
    assert presentation_name is not None
    return find_presentation_id_by_name(drive_service, presentation_name)


# Move slide to a new position
def update_slide_position(service, presentation_id: str, slide_object_id: str, new_index: int) -> str:
    requests = [{
        "updateSlidesPosition": {
            "slideObjectIds": [slide_object_id],
            "insertionIndex": new_index
        }
    }]
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()
    return f"Slide {slide_object_id} moved to index {new_index}"

# Replace all text
def replace_all_text(service, presentation_id: str, find_text: str, replace_text: str) -> str:
    requests = [{
        "replaceAllText": {
            "containsText": {"text": find_text, "matchCase": True},
            "replaceText": replace_text
        }
    }]
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()
    return f"Replaced all instances of '{find_text}' with '{replace_text}'"

# Delete text from a range
def delete_text_range(service, presentation_id: str, object_id: str, start_index: int, end_index: int) -> str:
    requests = [{
        "deleteText": {
            "objectId": object_id,
            "textRange": {
                "type": "FIXED_RANGE",
                "startIndex": start_index,
                "endIndex": end_index
            }
        }
    }]
    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()
    return f"Deleted text in range {start_index}-{end_index} from {object_id}"


def share_presentation(drive_service, presentation_id: str, emails: list[str], role: str = "writer") -> str:
    """
    Shares a presentation with the specified emails.

    Inputs:
    - drive_service: Authenticated Google Drive API service instance.
    - presentation_id (str): ID of the presentation.
    - emails (list[str]): List of email addresses to share the presentation with.
    - role (str): Sharing role – "reader", "writer", or "commenter".

    Returns:
    - str: Confirmation message.
    """
    for email in emails:
        drive_service.permissions().create(
            fileId=presentation_id,
            body={
                "type": "user",
                "role": role,
                "emailAddress": email
            },
            fields="id",
            sendNotificationEmail=False
        ).execute()

    return f"Presentation shared with: {', '.join(emails)} as '{role}'"