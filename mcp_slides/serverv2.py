from mcp.server.fastmcp import FastMCP
from typing import Optional
import tools
from auth import get_slides_service, get_drive_service

mcp = FastMCP("Google Slides MCP (Token Auth)")

@mcp.tool()
def create_presentation(title: str) -> str:
    """
    Creates a new Google Slides presentation with the given title.

    Inputs:
    - title (str): The title of the new presentation

    Returns:
    - str: URL of the newly created presentation

    Notes:
    - Will raise an error if a presentation with the same name already exists.
    """
    slides_service = get_slides_service()
    drive_service = get_drive_service()
    return tools.create_presentation(slides_service, drive_service, title)

@mcp.tool()
def get_presentation_metadata(
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> dict:
    """
    Retrieves metadata for a specific presentation.

    Inputs:
    - presentation_id (str, optional): ID of the presentation
    - presentation_name (str, optional): Name of the presentation (used if ID is not provided)

    Returns:
    - dict: Metadata including title, slide count, timestamps, etc.

    Notes:
    - Requires either the ID or name of an existing presentation.
    - Hi this is Johns signature.
    """
    slides_service = get_slides_service()
    drive_service = get_drive_service()

    if not presentation_id and not presentation_name:
        raise ValueError("Either 'presentation_id' or 'presentation_name' must be provided.")

    if presentation_id is None:
        assert presentation_name is not None, "Presentation name must be provided if ID is None"
        presentation_id = tools.find_presentation_id_by_name(drive_service, presentation_name)

    return tools.get_presentation_metadata(slides_service, drive_service, presentation_id)

@mcp.tool()
def add_blank_slide(
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> str:
    """
    Adds a blank slide to a Google Slides presentation.

    Inputs:
    - presentation_id (str, optional): ID of the target presentation.
    - presentation_name (str, optional): Name of the target presentation.

    Returns:
    - str: ID of the newly added blank slide.

    Notes:
    - If both ID and name are provided, ID is prioritized.
    """
    drive_service = get_drive_service()
    slides_service = get_slides_service()
    presentation_id = tools.resolve_presentation_id(drive_service, presentation_id, presentation_name)
    return tools.add_blank_slide(slides_service, presentation_id)

@mcp.tool()
def insert_text(
    text: str,
    slide_index: int = -1,
    font_family: str = "Arial",
    font_size: int = 18,
    color: str = "#000000",
    align: str = "center",
    bullet: bool = False,
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> str:
    """
    Inserts styled text into a slide of a Google Slides presentation.

    Inputs:
    - text (str): The content to insert. Use '\n' for new lines. Use **bold** to style bold text.
    - slide_index (int, optional): Target slide index (default: last slide).
    - font_family (str): Font type to use.
    - font_size (int): Font size.
    - color (str): Text color in hex format.
    - align (str): Text alignment ('left', 'center', 'right').
    - bullet (bool): Whether to add bullet points.
    - presentation_id / presentation_name (optional): Identify target presentation.

    Returns:
    - str: ID of the inserted text box object.
    """
    drive_service = get_drive_service()
    slides_service = get_slides_service()
    presentation_id = tools.resolve_presentation_id(drive_service, presentation_id, presentation_name)
    return tools.insert_text_on_slide(
        slides_service,
        presentation_id,
        text,
        slide_index,
        font_family,
        font_size,
        color,
        align,
        bullet
    )

@mcp.tool()
def insert_image(
    image_url: str,
    slide_index: int = -1,
    width: int = 300,
    height: int = 200,
    x_offset: int = 50,
    y_offset: int = 100,
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> str:
    """
    Inserts an image into a slide.

    Inputs:
    - image_url (str): URL of the image to insert.
    - slide_index (int): Slide index (default: last).
    - width / height (int): Image size.
    - x_offset / y_offset (int): Position in slide.
    - presentation_id / presentation_name (optional): Presentation to target.

    Returns:
    - str: Object ID of the inserted image.
    """
    drive_service = get_drive_service()
    slides_service = get_slides_service()
    presentation_id = tools.resolve_presentation_id(drive_service, presentation_id, presentation_name)
    return tools.insert_image_on_slide(slides_service, presentation_id, image_url, slide_index, width, height, x_offset, y_offset)

@mcp.tool()
def list_slides(
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> list:
    """
    Lists all slides in a presentation.

    Inputs:
    - presentation_id / presentation_name (optional): Presentation to target.

    Returns:
    - list: A list of dictionaries with slide details (index, objectId, etc.)
    """
    drive_service = get_drive_service()
    slides_service = get_slides_service()
    presentation_id = tools.resolve_presentation_id(drive_service, presentation_id, presentation_name)
    return tools.list_slides(slides_service, presentation_id)

@mcp.tool()
def move_slide(
    slide_object_id: str,
    new_index: int,
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> str:
    """
    Moves a slide to a different position in the presentation.

    Inputs:
    - slide_object_id (str): Object ID of the slide to move.
    - new_index (int): Target index position (0-based).
    - presentation_id / presentation_name (optional): Target presentation.

    Returns:
    - str: Confirmation message.
    """
    slides_service = get_slides_service()
    drive_service = get_drive_service()
    pid = tools.resolve_presentation_id(drive_service, presentation_id, presentation_name)
    return tools.update_slide_position(slides_service, pid, slide_object_id, new_index)

@mcp.tool()
def replace_all_text(
    find_text: str,
    replace_text: str,
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> str:
    """
    Replaces all instances of specific text across all slides.

    Inputs:
    - find_text (str): Text to find.
    - replace_text (str): Replacement text.
    - presentation_id / presentation_name (optional): Target presentation.

    Returns:
    - str: Result message.
    """
    slides_service = get_slides_service()
    drive_service = get_drive_service()
    pid = tools.resolve_presentation_id(drive_service, presentation_id, presentation_name)
    return tools.replace_all_text(slides_service, pid, find_text, replace_text)

@mcp.tool()
def delete_text_range(
    object_id: str,
    start_index: int,
    end_index: int,
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> str:
    """
    Deletes a range of text from a text box.

    Inputs:
    - object_id (str): Object ID of the text box.
    - start_index / end_index (int): Range of characters to delete.
    - presentation_id / presentation_name (optional): Target presentation.

    Returns:
    - str: Confirmation of deletion.
    """
    slides_service = get_slides_service()
    drive_service = get_drive_service()
    pid = tools.resolve_presentation_id(drive_service, presentation_id, presentation_name)
    return tools.delete_text_range(slides_service, pid, object_id, start_index, end_index)

@mcp.tool()
def share_presentation(
    emails: list[str],
    role: str = "writer",
    presentation_id: Optional[str] = None,
    presentation_name: Optional[str] = None
) -> str:
    """
    Shares a presentation with specific email addresses.

    Inputs:
    - emails (list[str]): List of email addresses to share with.
    - role (str): Permission role – "reader", "writer", or "commenter".
    - presentation_id / presentation_name (optional): Target presentation.

    Returns:
    - str: Confirmation message listing shared recipients.
    """
    slides_service = get_slides_service()
    drive_service = get_drive_service()
    pid = tools.resolve_presentation_id(drive_service, presentation_id, presentation_name)

    for email in emails:
        drive_service.permissions().create(
            fileId=pid,
            body={
                "type": "user",
                "role": role,
                "emailAddress": email
            },
            fields="id"
        ).execute()

    return f"Shared with: {', '.join(emails)} as {role}"
