import streamlit as st

from rag import generate_answer

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📚",
    layout="wide",
)

st.title("📚 RAG Chatbot")
st.caption("Ask questions about your documents and receive answers with source citations.")

st.divider()

question = st.text_area(
    "Your question:",
    placeholder="What is Artificial Intelligence?",
    height=100,
)
question = question.strip()

ask_button = st.button("Ask", type="primary")

if not question:
    st.warning("Please enter a question.")
else:
    with st.spinner("Searching your documents and generating an answer..."):
        try:
            result, documents = generate_answer(question)
            st.subheader("Answer")
            st.write(result.answer)

            # Answer
            if result.insufficient_context:
                st.warning("The available documents may not contain enough information "
                           "to answer this question completely")
            else:
                st.success("Answer generated successfully.")

            # Citations
            if result.citations:
                for index, citation in enumerate(result.citations, start=1):
                    st.markdown(f"**[{index}]** `{citation.source}` | Page {citation.page_number}")
            else:
                st.info("No citations found.")

            # Retrieved documents
            with st.expander("View retrieved document passages"):
                if documents:
                    for index, document in enumerate(documents, start=1):
                        st.markdown(f"**Passage {index}** | `{document.source}` | Page {document.page_number}")
                        st.caption(f"Retrieval distance: {document.distance}")
                        st.write(document.text)
                        st.divider()
                else:
                    st.write("No relevant passages were retrieved")


        except Exception as e:
            st.error( "Something went wrong while processing your question. Check the terminal for details.")
            print(f"Error generating answer: {e}")

st.divider()
st.caption("Answers are based on the documents available in the local knowledge base.")


