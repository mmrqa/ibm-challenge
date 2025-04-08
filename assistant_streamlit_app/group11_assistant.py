import streamlit as st
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import os
import re
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load environment variables
load_dotenv()

# Watson Assistant setup
authenticator = IAMAuthenticator(os.getenv("WATSON_API_KEY"))
assistant = AssistantV2(version='2024-08-25', authenticator=authenticator)
assistant.set_service_url(os.getenv("WATSON_SERVICE_URL"))
assistant_id = os.getenv("WATSON_ENVIRONMENT_ID")

# Helper functions
def sanitize_text(text):
    return re.sub(r'[\t\n\r]+', ' ', text)

def split_text(text, max_length=500):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def get_relevant_chunks(query, chunks, vectorizer):
    query_vec = vectorizer.transform([query])
    chunk_vecs = vectorizer.transform(chunks)
    similarities = cosine_similarity(query_vec, chunk_vecs).flatten()
    top_chunk_indices = np.argsort(similarities)[::-1][:3]  # Top 3 relevant chunks
    return [chunks[i] for i in top_chunk_indices]

# Streamlit app
st.title("IBM Watson Assistant Document-based Chat")

uploaded_file = st.file_uploader("Upload a file (docx)", type=["docx"])

if uploaded_file:
    file_content = docx2txt.process(uploaded_file)
    sanitized_content = sanitize_text(file_content)
    document_chunks = split_text(sanitized_content)

    vectorizer = TfidfVectorizer().fit(document_chunks)

    # Initialize Watson session
    session = assistant.create_session(assistant_id=assistant_id).get_result()
    session_id = session['session_id']

    st.subheader("Ask a Question")

    user_query = st.text_input("Type your question here")

    if st.button("Submit") and user_query:
        # Get the top relevant text chunks
        relevant_chunks = get_relevant_chunks(user_query, document_chunks, vectorizer)
        
        st.write("**Top Relevant Chunks and their Responses:**")
        # Loop through each chunk and get a separate response from Watson Assistant
        for idx, chunk in enumerate(relevant_chunks, start=1):
            # Build a prompt for the current chunk
            prompt = (f"Based on the following context, answer the question:"
                      f"Context: {chunk}"
                      f"Question: {user_query}")
            
            response = assistant.message(
                assistant_id=assistant_id,
                session_id=session_id,
                environment_id=assistant_id,
                input={'message_type': 'text', 'text': prompt}
            ).get_result()
            
            st.markdown(f"**Chunk {idx}:**")

            response_text = ""
            for output in response['output']['generic']:
                if output['response_type'] == 'conversational_search':
                    response_text += output['text'] + " "               
                    st.write(f"**Response:** {response_text}")
            
            

    # End the Watson session
    assistant.delete_session(assistant_id=assistant_id, session_id=session_id)
