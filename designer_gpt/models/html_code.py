from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, validator


class HTMLCode(BaseModel):
    html: str = Field(description="The generated HTML code")
