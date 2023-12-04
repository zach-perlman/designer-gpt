from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from models.html_code import HTMLCode

model = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
pydantic_parser = PydanticOutputParser(pydantic_object=HTMLCode)
output_parser = OutputFixingParser.from_llm(parser=pydantic_parser, llm=model)

BASE_PROMPT = """\
You are a frontend engineer. Given a wireframe mockup, write complete HTML code
with Tailwind CSS classes for the following. Make sure to provide full HTML code along
with the script tags for Tailwind CSS.

Prompt:
{prompt}

Wireframe:
{wireframe}

{output_instructions}
"""


def generate_webpage(
    prompt: str,
    wireframe: str,
) -> str:
    print("Got prompt", prompt)
    print("Got wireframe", wireframe)
    p = ChatPromptTemplate.from_messages(
        [
            ("human", BASE_PROMPT),
        ]
    )
    inp = p.format_messages(
        prompt=prompt,
        wireframe=wireframe,
        output_instructions=output_parser.get_format_instructions(),
    )

    res = model.invoke(inp)

    out = output_parser.parse(res.content)
    return out.html
