import random
import time

import streamlit as st

from randselect.selector import random_selection

FLASH_SECONDS = 3
FLASH_INTERVAL = 0.1

st.title("Random Selector")

if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "result" not in st.session_state:
    st.session_state.result = None


def _add_name():
    value = st.session_state.name_input.strip()
    if value:
        st.session_state.names.append(value)
    st.session_state.name_input = ""


def _add_question():
    value = st.session_state.question_input.strip()
    if value:
        st.session_state.questions.append(value)
    st.session_state.question_input = ""


col1, col2 = st.columns(2)

with col1:
    st.subheader("Names")
    st.text_input("Add a name", key="name_input")
    st.button("Add name", on_click=_add_name)
    st.write(st.session_state.names)

with col2:
    st.subheader("Questions")
    st.text_input("Add a question", key="question_input")
    st.button("Add question", on_click=_add_question)
    st.write(st.session_state.questions)

no_repeats = st.checkbox("No repeats")

if no_repeats:
    available_names = [
        name for name in st.session_state.names
        if name not in st.session_state.used_names
    ]
else:
    available_names = st.session_state.names

all_exhausted = no_repeats and st.session_state.names and not available_names
draw_disabled = (
    not st.session_state.names
    or not st.session_state.questions
    or all_exhausted
)

if all_exhausted:
    st.warning("All names are selected!")

placeholder = st.empty()

if st.button("Draw", disabled=draw_disabled):
    rng = random.Random()
    end_time = time.time() + FLASH_SECONDS
    while time.time() < end_time:
        flash_name, flash_question = random_selection(
            available_names, st.session_state.questions, rng
        )
        placeholder.markdown(f"### {flash_name}, please answer: {flash_question}")
        time.sleep(FLASH_INTERVAL)

    final_name, final_question = random_selection(
        available_names, st.session_state.questions, rng
    )
    st.session_state.result = (final_name, final_question)
    if no_repeats:
        st.session_state.used_names.add(final_name)
    placeholder.empty()
    st.rerun()

if st.session_state.result is not None:
    name, question = st.session_state.result
    st.success(f"{name}, please answer: {question}")
