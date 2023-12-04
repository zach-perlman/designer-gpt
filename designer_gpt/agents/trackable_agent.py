import base64
import re
from typing import Dict, Optional, Union
from urllib.parse import quote_plus

import chainlit as cl
import server  # Add routes
import shared
from autogen import Agent, AssistantAgent, GroupChatManager, UserProxyAgent
from chains.generate_webpage import generate_webpage

last_mermaid_code = None


def extract_mermaid_content(string):
    global last_mermaid_code
    pattern = r"```mermaid(.*?)```"
    matches = re.findall(pattern, string, re.DOTALL)
    if matches:
        code = matches[0].strip()
        last_mermaid_code = code
        shared.wireframe_code = code
        return code

    return None


async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res


class ObservableManager(GroupChatManager):
    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ) -> bool | None:
        msg = message.get("content", "") if isinstance(message, dict) else message
        mermaid_code = extract_mermaid_content(msg)
        if mermaid_code:
            b64_diagram = base64.b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
            print(f"https://mermaid.ink/img/{b64_diagram}")
            cl.run_sync(
                cl.Image(
                    name="wireframe",
                    url=f"https://mermaid.ink/img/{b64_diagram}",
                    display="inline",
                ).send()
            )
        else:
            cl.run_sync(
                cl.Message(
<<<<<<< HEAD
                    content=f'*Sending message from "{self.name}" to "{recipient.name}":*\n\n{msg}',
=======
                    content=f'*Sending message from {self.name} to "{recipient.name}":*\n\n{msg}',
>>>>>>> efbae07 (Add HTML preview feature)
                    author="AssistantAgent",
                ).send()
            )

        super(ObservableManager, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )


class ObservableAssistantAgent(AssistantAgent):
    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ) -> bool | None:
        msg = message.get("content", "") if isinstance(message, dict) else message
        mermaid_code = extract_mermaid_content(msg)
        if mermaid_code:
            b64_diagram = base64.b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
            print(f"https://mermaid.ink/img/{b64_diagram}")
            cl.run_sync(
                cl.Image(
                    name="wireframe",
                    url=f"https://mermaid.ink/img/{b64_diagram}",
                    display="inline",
                ).send()
            )
        else:
            cl.run_sync(
                cl.Message(
                    content=f'*Sending message from "{self.name}" to "{recipient.name}":*\n\n{msg}',
                    author="AssistantAgent",
                ).send()
            )
        super(ObservableAssistantAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )


class ObservableUserProxyAgent(UserProxyAgent):
    def get_human_input(self, prompt: str) -> str:
        ptrn = r"Provide feedback to .*"
        if re.match(ptrn, prompt):
            actions = [
                cl.Action(name="continue", value="continue", label="✅ Continue"),
                cl.Action(
                    name="feedback",
                    value="feedback",
                    label="💬 Provide feedback",
                ),
                cl.Action(name="exit", value="exit", label="🔚 Exit Conversation"),
            ]

            # Check if we had previous mermaid code
            if last_mermaid_code:
                actions.append(
                    cl.Action(
                        name="Generate HTML",
                        value="generate_html",
                        label="📄 Generate HTML",
                    )
                )

            res = cl.run_sync(
                ask_helper(
                    cl.AskActionMessage,
                    content="Continue or provide feedback?",
                    actions=actions,
                )
            )
            if res.get("value") == "continue":
                return ""
            if res.get("value") == "exit":
                return "exit"
            if res.get("value") == "generate_html":
                og_html_code = generate_webpage(
                    shared.user_prompt, shared.wireframe_code
                )
                # Tab over all lines in html_code
                html_code = "\n".join(
                    ["\t" + line for line in og_html_code.splitlines()]
                )
                encoded_html = base64.b64encode(og_html_code.encode("utf-8")).decode(
                    "utf-8"
                )
                encoded_html = quote_plus(encoded_html)
                content = "*Here is the HTML code for your wireframe:*\n\n"
                content += f"\t{html_code}\n"
                content += "\n\n"
                content += f"Please visit [this link](/display?html={encoded_html}) to view the rendered HTML code."

                print(content)
                txt = cl.Text(name="Your Website!", content=content, display="inline")
                cl.run_sync(
                    cl.Message(
                        content="Generated HTML code!",
                        author="AssistantAgent",
                        elements=[txt],
                    ).send()
                )

                return "exit"

        reply = cl.run_sync(ask_helper(cl.AskUserMessage, content=prompt, timeout=60))

        return reply["content"].strip()

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        msg = message.get("content", "") if isinstance(message, dict) else message
        mermaid_code = extract_mermaid_content(msg)
        if mermaid_code:
            b64_diagram = base64.b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
            print(f"https://mermaid.ink/img/{b64_diagram}")
            cl.run_sync(
                cl.Image(
                    name="wireframe",
                    url=f"https://mermaid.ink/img/{b64_diagram}",
                    display="inline",
                ).send()
            )
        else:
            cl.run_sync(
                cl.Message(
                    content=f'*Sending message from "{self.name}" to "{recipient.name}":*\n\n{msg}',
                    author="AssistantAgent",
                ).send()
            )

        super(ObservableUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )
