import base64
from urllib.parse import unquote_plus

from chainlit.server import app
from fastapi import HTTPException
from fastapi.responses import HTMLResponse


@app.get("/display", response_class=HTMLResponse)
async def read_html(html: str):
    try:
        unquoted_html = unquote_plus(html).replace(" ", "+")
        decoded_html = base64.b64decode(unquoted_html).decode("utf-8")
        return decoded_html
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid Base64 HTML string")
