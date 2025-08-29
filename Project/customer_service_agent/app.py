import os
import sys
import asyncio

import streamlit as st
from dotenv import load_dotenv

# Ensure we can import the sibling package `customer_service_agent`
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from customer_service_agent.agent import agent as customer_service_agent
from customer_service_agent.utils import (
    add_user_query_to_history,
    add_agent_response_to_history,
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


def run_async(coro):
    return asyncio.run(coro)


async def run_agent_query(runner, user_id, session_id, query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_text = None
    agent_name = None

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.author:
            agent_name = event.author
        if (
            event.is_final_response()
            and event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_text = event.content.parts[0].text.strip()

    if final_text and agent_name:
        await add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_text,
        )

    return agent_name, final_text


def init_app():
    load_dotenv()
    st.set_page_config(page_title="Customer Service", page_icon="💬")

    if "session_service" not in st.session_state:
        st.session_state.session_service = InMemorySessionService()

    if "app_name" not in st.session_state:
        st.session_state.app_name = "Customer Support"
    if "user_id" not in st.session_state:
        st.session_state.user_id = "aiwithbrandon"

    if "session_id" not in st.session_state:
        initial_state = {
            "user_name": "Rishiraj Bal",
            "purchased_courses": [],
            "interaction_history": [],
        }
        new_session = run_async(
            st.session_state.session_service.create_session(
                app_name=st.session_state.app_name,
                user_id=st.session_state.user_id,
                state=initial_state,
            )
        )
        st.session_state.session_id = new_session.id

    if "runner" not in st.session_state:
        st.session_state.runner = Runner(
            agent=customer_service_agent,
            app_name=st.session_state.app_name,
            session_service=st.session_state.session_service,
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []


def render_sidebar():
    with st.sidebar:
        st.subheader("Session State")
        try:
            session = run_async(
                st.session_state.session_service.get_session(
                    app_name=st.session_state.app_name,
                    user_id=st.session_state.user_id,
                    session_id=st.session_state.session_id,
                )
            )
            st.json(session.state)
        except Exception as e:
            st.warning(f"Unable to load session state: {e}")


def render_chat():
    st.title("Customer Service Chat")

    # Replay history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Type your message")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Update interaction history
        run_async(
            add_user_query_to_history(
                st.session_state.session_service,
                st.session_state.app_name,
                st.session_state.user_id,
                st.session_state.session_id,
                prompt,
            )
        )

        # Run agent and display response
        agent_name, response_text = run_async(
            run_agent_query(
                st.session_state.runner,
                st.session_state.user_id,
                st.session_state.session_id,
                prompt,
            )
        )

        if response_text:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text,
                }
            )
            with st.chat_message("assistant"):
                st.markdown(response_text)
        else:
            st.info("No response generated.")


def main():
    init_app()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()


