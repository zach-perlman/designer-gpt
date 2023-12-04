import chainlit as cl
import shared
from agents.trackable_agent import (
    ObservableAssistantAgent,
    ObservableManager,
    ObservableUserProxyAgent,
)
from autogen import GroupChat, config_list_from_json
from prompts import (
    CRITIC_PROMPT,
    PLANNER_PROMPT,
    SOFTWARE_ENGINEER_PROMPT,
    USER_PROXY_PROMPT,
    UX_DESIGNER_PROMPT,
)


@cl.on_chat_start
async def on_chat_start():
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

    user_proxy = ObservableUserProxyAgent(
        name="User_Proxy",
        system_message=USER_PROXY_PROMPT,
        code_execution_config=False,
        llm_config={"config_list": config_list},
    )

    critic = ObservableAssistantAgent(
        name="Critic",
        system_message=CRITIC_PROMPT,
        code_execution_config=False,
        llm_config={"config_list": config_list},
    )
    planner = ObservableAssistantAgent(
        name="Planner",
        system_message=PLANNER_PROMPT,
        code_execution_config=False,
        llm_config={"config_list": config_list},
    )
    software_engineer = ObservableAssistantAgent(
        name="Software_Engineer",
        system_message=SOFTWARE_ENGINEER_PROMPT,
        code_execution_config=False,
        llm_config={"config_list": config_list},
    )
    ux_designer = ObservableAssistantAgent(
        name="UX_Designer",
        system_message=UX_DESIGNER_PROMPT,
        code_execution_config=False,
        llm_config={"config_list": config_list},
    )

    groupchat = GroupChat(
        agents=[
            user_proxy,
            critic,
            planner,
            software_engineer,
            ux_designer,
        ],
        messages=[],
        max_round=20,
    )
    manager = ObservableManager(
        groupchat=groupchat,
    )

    prompt = await cl.AskUserMessage("What do you want to design today?").send()
    if not prompt:
        return

    prompt = prompt["content"]
    shared.user_prompt = prompt
    await cl.Message(content=prompt).send()
    await cl.make_async(user_proxy.initiate_chat)(
        manager,
        message=prompt,
    )
