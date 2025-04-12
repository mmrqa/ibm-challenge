import streamlit as st
import tempfile
from utils import extract_docx_clauses, extract_pdf_clauses, split_clause_into_chunks
from watson import query_clause_similarity

st.set_page_config(page_title="NDA Analyzer", layout="wide")
st.title("NDA Clause Checker (Watson Discovery)")

uploaded_file = st.file_uploader("Upload your NDA (.docx or .pdf)", type=["docx", "pdf"])

# User-adjustable similarity threshold
threshold = st.slider("🔎 Flag clauses with similarity below:", 0.0, 1.0, 0.75, step=0.01)

if uploaded_file:
    ext = uploaded_file.name.split('.')[-1].lower()
    st.write(f"✅ File uploaded: `{uploaded_file.name}` (.{ext})")

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
        st.write(f"📂 Temp file saved at: {tmp_path}")

    # Extract text
    try:
        if ext == "docx":
            clauses = extract_docx_clauses(tmp_path)
        elif ext == "pdf":
            clauses = extract_pdf_clauses(tmp_path)
        else:
            st.error("Unsupported file type.")
            st.stop()
    except Exception as e:
        st.error(f"❌ Error extracting text: {e}")
        st.stop()

    st.success(f"✅ Extracted {len(clauses)} paragraphs.")

    # Process each clause with Watson
    flagged = []
    with st.spinner("🔍 Analyzing with Watson Discovery..."):
        for i, clause in enumerate(clauses):
            if not clause.strip():
                continue

            try:
                # Split long clauses into chunks
                chunks = split_clause_into_chunks(clause)
                chunk_results = []

                for chunk in chunks:
                    chunk_result = query_clause_similarity(chunk)
                    chunk_results.append(chunk_result)

                if chunk_results:
                    # Use the lowest similarity score across all chunks
                    worst_chunk = min(chunk_results, key=lambda r: r['score'])
                    score = worst_chunk['score']
                    match = worst_chunk['match']

                    if score < threshold:
                        flagged.append({
                            "clause": clause,
                            "match": match,
                            "score": score,
                            "comment": f"Lowest similarity among {len(chunks)} chunk(s): {score:.2f}"
                        })

            except Exception as e:
                st.error(f"❌ Watson query failed on clause {i+1}: {e}")
                continue

    # Show flagged results
    st.subheader("🚩 Flagged Clauses")
    if flagged:
        for item in flagged:
            st.markdown("---")
            st.markdown(f"**Clause:**\n{item['clause']}")
            st.markdown(f"**Closest Match:**\n{item['match']}")
            st.markdown(f"**Similarity Score:** `{item['score']:.2f}`")
            st.warning(item['comment'])
    else:
        st.success("✅ No concerning clauses found!")
