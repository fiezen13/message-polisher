import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.ai_service import generate_polish_result
from app.services.text_service import clean_text


RECIPIENT_OPTIONS = ["professor", "recruiter", "manager", "client", "teammate", "unknown"]
TONE_OPTIONS = ["formal", "apologetic", "friendly", "assertive", "neutral"]
PURPOSE_OPTIONS = [
    "request_extension",
    "follow_up",
    "apology",
    "scheduling",
    "escalation",
    "gratitude",
    "other",
]
SOURCE_LANGUAGE_OPTIONS = ["vi", "ja", "en"]
DETAIL_LEVEL_OPTIONS = ["concise", "balanced", "detailed"]


def main():
    st.set_page_config(page_title="Message Polisher", layout="wide")
    st.title("Context-aware Message Polisher")
    st.caption("Japanese-first assistant: input context, get polished Japanese + quick variants.")

    if "result" not in st.session_state:
        st.session_state.result = None

    col_left, col_right = st.columns([1, 1], gap="large")
    with col_left:
        st.subheader("Input")

        with st.form("polish_form", clear_on_submit=False):
            original_message = st.text_area(
                "Original message",
                placeholder="Ví dụ: Em muốn xin lùi deadline thêm 2 ngày",
                height=160,
            )
            ui_col_1, ui_col_2, ui_col_3 = st.columns(3)
            with ui_col_1:
                source_language = st.selectbox("Source language", SOURCE_LANGUAGE_OPTIONS, index=0)
            with ui_col_2:
                recipient_type = st.selectbox("Recipient", RECIPIENT_OPTIONS, index=0)
            with ui_col_3:
                tone = st.selectbox("Tone", TONE_OPTIONS, index=1)
            purpose = st.selectbox("Purpose", PURPOSE_OPTIONS, index=0)
            detail_level = st.selectbox(
                "Detail level",
                DETAIL_LEVEL_OPTIONS,
                index=1,
                help="concise: short request-style; balanced: default; detailed: more explanation when needed",
            )
            submitted = st.form_submit_button("Polish message", type="primary", use_container_width=True)

        if submitted:
            if not original_message.strip():
                st.error("Please provide a message.")
            else:
                with st.spinner("Generating Japanese output..."):
                    try:
                        cleaned_input = clean_text(original_message)
                        st.session_state.result = generate_polish_result(
                            original_message=cleaned_input,
                            recipient_type=recipient_type,
                            tone=tone,
                            purpose=purpose,
                            language="ja",
                            source_language=source_language,
                            detail_level=detail_level,
                        )
                    except Exception as exc:
                        st.session_state.result = None
                        st.error(f"Failed to generate output: {exc}")

    with col_right:
        st.subheader("Output")
        result = st.session_state.result
        if not result:
            st.info("Submit a message to see Japanese output and variants.")
            return

        st.markdown("**Main output (Japanese)**")
        st.text_area("Rewritten", value=result["rewritten_message"], height=120, key="rewritten_result")

        st.markdown("**Quick variants**")
        tab_formal, tab_friendly, tab_concise, tab_prof = st.tabs(
            ["Formal", "Friendly", "Concise", "Highly professional"]
        )
        with tab_formal:
            st.text_area("Formal", value=result["quick_variants"]["formal"], height=110, key="var_formal")
        with tab_friendly:
            st.text_area("Friendly", value=result["quick_variants"]["friendly"], height=110, key="var_friendly")
        with tab_concise:
            st.text_area("Concise", value=result["quick_variants"]["concise"], height=110, key="var_concise")
        with tab_prof:
            st.text_area(
                "Highly professional",
                value=result["quick_variants"]["highly_professional"],
                height=110,
                key="var_professional",
            )

        with st.expander("Meta and safety flags"):
            st.json({"meta": result["meta"], "safety_flags": result["safety_flags"]})


if __name__ == "__main__":
    main()
