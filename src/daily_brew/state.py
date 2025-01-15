import operator
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing_extensions import List, Annotated

class Brew(BaseModel):
    title: str = Field(
        description="Punchy summary title for the daily brew",
    )
    brew: str = Field(
        description="Content of the daily brew",
    )

@dataclass(kw_only=True)
class State:
    brew: Brew = field(default=None)

