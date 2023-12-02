import base64
import re
from typing import Dict, Optional, Union

import chainlit as cl
from autogen import Agent, AssistantAgent, GroupChatManager, UserProxyAgent


def extract_mermaid_content(string):
    pattern = r"```mermaid(.*?)```"
    matches = re.findall(pattern, string, re.DOTALL)
    if matches:
        return matches[0].strip().replace('"', "'")
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
                    content=f'*Sending message to "{recipient.name}":*\n\n{msg}',
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
                    content=f'*Sending message to "{recipient.name}":*\n\n{msg}',
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
            res = cl.run_sync(
                ask_helper(
                    cl.AskActionMessage,
                    content="Continue or provide feedback?",
                    actions=[
                        cl.Action(
                            name="continue", value="continue", label="✅ Continue"
                        ),
                        cl.Action(
                            name="feedback",
                            value="feedback",
                            label="💬 Provide feedback",
                        ),
                        cl.Action(
                            name="exit", value="exit", label="🔚 Exit Conversation "
                        ),
                    ],
                )
            )
            if res.get("value") == "continue":
                return ""
            if res.get("value") == "exit":
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
                    content=f'*Sending message to "{recipient.name}":*\n\n{msg}',
                    author="AssistantAgent",
                ).send()
            )

        super(ObservableUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )
