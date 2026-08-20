from pydantic import BaseModel


class Microstandard(BaseModel):
    id: str
    name: str
    domain: str  # engineering | business | psychology | universal
    situation: str  # "Если..."
    resolution: str  # "То..."
    constraints: str | None = None
    resources: str | None = None
    example: str | None = None
    tags: list[str] = []
    source: str | None = None


class SearchMatch(BaseModel):
    id: str
    score: int
    why: str
