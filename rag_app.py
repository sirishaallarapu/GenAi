import os
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document

# ✅ Set API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDvmhpLuwIzaegbN9Zm2x7ArOsHkGkcljY"

# 🌟 Initialize Gemini Model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)

# 🎯 Streamlit UI
st.title("📚 RAG-Powered Chatbot")
st.write("Upload a PDF and ask questions using **Retrieval-Augmented Generation (RAG)**!")

# 📂 File Upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    # 📌 Load and Split PDF into Chunks
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    loader = PyPDFLoader("temp.pdf")
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # 🔍 Create FAISS Vector Store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(docs, embeddings)

    st.success("✅ PDF Indexed! You can now ask questions.")

    # ✨ User Query Input
    query = st.text_input("Ask a question from the document:")

    if st.button("Search"):
        # 🔎 Retrieve Relevant Documents
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})
        retrieved_docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        # 🤖 AI-Powered Answer Generation
        prompt = f"Use the following document excerpts to answer the query:\n{context}\n\nQuery: {query}"
        response = llm.invoke(prompt)

        # 📌 Display Answer
        st.subheader("📌 Answer:")
        st.write(response.content)
