import streamlit as st
from rich import spinner

from rag import generate_answer

st.set_page_config(
    page_title="RAG Lab",
    page_icon="📚",
    layout="wide",
)

# Styling
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 4rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        .main-title {
            font-size: 2.4rem;
            font-weight: 700;
            letter-spacing: -1px;
            margin-bottom: 0.25rem;
        }

        .subtitle {
            font-size: 1rem;
            opacity: 0.75;
            margin-bottom: 1.5rem;
        }

        .section-label {
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            opacity: 0.7;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.divider()

# Side bar
with st.sidebar:
    st.title("📚 RAG Lab")
    st.caption("Document question answering")
    st.divider()

    st.markdown("### Your Workspace")
    st.markdown("Ask questions about your documents and inspect the evidence behind generated answers.")
    st.divider()

    st.markdown("### Knowledge base")

    st.markdown("📄 PDF documents")
    st.markdown("🔎 Semantic search")
    st.markdown("📑 Page-level citations")
    st.divider()

    st.markdown("### About")
    st.caption(
        "An open-source Retrieval-Augmented Generation "
        "project built with Python, ChromaDB, OpenAI, "
        "Pydantic, and Streamlit."
    )
    st.caption("Answers are grounded in retrieved document context.")


# Main header
st.markdown(
    '<div class="main-title">Document Question Answering</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">'
    'Ask questions. Explore your documents. Inspect the evidence.'
    '</div>',
    unsafe_allow_html=True,
)
st.divider()


# Question input
st.markdown(
    '<div class="section-label">ASK YOUR DOCUMENTS</div>',
    unsafe_allow_html=True,
)

with st.form("question form"):
    question = st.text_area(
        "Your question:",
        placeholder="What is Artificial Intelligence?",
        height=100,
        label_visibility='collapsed',
    )
    submitted = st.form_submit_button(
        "Search documents and answer",
        type="primary",
        use_container_width=True,
    )


# Answer generation
if submitted:
    question = question.strip()

    if not question:
        st.warning("Please enter a question first.")

    else:
        with st.spinner("Searching your documents and generating an answer..."):
            try:
                result, documents = generate_answer(question)
                st.session_state["last_question"] = question
                st.session_state["last_result"] = result
                st.session_state["last_documents"] = documents


            except Exception as e:
                st.error("Something went wrong while processing your question. Check the terminal for details.")
                print(f"Error generating answer: {e}")


# Display latest answer
last_question = st.session_state.get("last_question", "")
result = st.session_state.get("last_result")
documents = st.session_state.get("last_documents", [])

if result is not None:
    st.divider()
    st.markdown(
        '<div class="section-label">YOUR QUESTION</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**{last_question}**")

    st.markdown("## Answer")
    st.write(result.answer)

    if result.insufficient_context:
        st.warning(
            "The available documents may not contain enough information "
            "to answer this question completely."
        )

    # Citations
    if result.citations:
        for index, citation in enumerate(result.citations, start=1):
            with st.container(border=True):
                st.markdown(f"**[{index}] {citation.source}**")
                st.caption(f"Page {citation.page_number}")
    else:
        st.info("No citations were returned for this answer.")

    # Retrieved passages
    with st.expander("🔎 Inspect retrieved evidence"):
        if documents:
            for index, document in enumerate(documents, start=1):
                with st.container(border=True):
                    st.markdown(f"**Passage {index}**")
                    st.caption(
                        f"{document.source} · Page {document.page_number}"
                    )
                    st.caption(
                        f"Retrieval distance: {document.distance:.3f}"
                    )
                    st.write(document.text)
        else:
            st.write("No document passages were retrieved.")

    if st.button("Clear current answer"):
        for key in (
                "last_question",
                "last_result",
                "last_documents",
        ):
            st.session_state.pop(key, None)

        st.rerun()

# Footer
st.divider()

st.caption(
    "RAG Lab"
)


