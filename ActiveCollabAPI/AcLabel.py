from dataclasses import dataclass


@dataclass
class AcLabel:
    color: str
    darker_text_color: str
    id: int
    is_default: bool
    is_global: bool
    lighter_text_color: str
    name: str
    position: str
    project_id: int | None
    url_path: str
