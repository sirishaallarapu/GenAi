import streamlit as st
import PyPDF2
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Set API Key
GOOGLE_API_KEY = "AIzaSyDvmhpLuwIzaegbN9Zm2x7ArOsHkGkcljY"

# Initialize Embeddings Model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=GOOGLE_API_KEY
)

# Initialize LLM Model (Gemini AI)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)

# Streamlit UI
st.title("🤖 AI-Powered RAG Chatbot")

st.write("Upload a PDF, and chat with AI to ask questions based on the document content.")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    raw_text = ""
    for page in pdf_reader.pages:
        raw_text += page.extract_text() + "\n"

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(raw_text)

    # Convert to LangChain Documents
    documents = [Document(page_content=text) for text in texts]

    # Create FAISS Vector Store
    vector_store = FAISS.from_documents(documents, embeddings)

    # Initialize Chat History
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User Input
    user_query = st.text_input("Ask a question about the document:")

    if st.button("Send"):
        if user_query:
            # Retrieve Relevant Chunks
            docs = vector_store.similarity_search(user_query, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])

            # Define Prompt
            prompt_template = PromptTemplate(
                input_variables=["query", "context"],
                template="Based on the following document excerpts, answer the question:\n\n{context}\n\nQuestion: {query}\nAnswer:"
            )

            # Format Prompt
            final_prompt = prompt_template.format(query=user_query, context=context)
            response = llm.invoke(final_prompt)

            # Update Chat History
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=response.content))

        # Display Chat History
        st.subheader("Chat History:")
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                st.write(f"**You:** {message.content}")
            else:
                st.write(f"**AI:** {message.content}")
