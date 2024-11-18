from flask import Flask, request, jsonify, Blueprint 
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint
from PyPDF2 import PdfReader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import HuggingFaceHub
from werkzeug.utils import secure_filename

# Create Blueprint
llm_bp = Blueprint('llm', __name__)

load_dotenv()  # Load .env file

HF_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
UPLOAD_FOLDER = "./uploaded_pdfs"  # Folder to store uploaded PDFs
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

def load_pdf(file_path):
    # Read the PDF from the local file system
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + '\n'
    return text

def chunking(document_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    documents = text_splitter.create_documents([document_text])
    return documents

def embeddings(documents):
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L12-v2", model_kwargs={"trust_remote_code": True})
    vector_store = FAISS.from_documents(documents, embedding_model)
    return vector_store

def create_llm_chain(vectorstore):
    template = """Given the following user question. You are helping an instructor to summarize and understand the text provided.
    Context: {context}
    Question: {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.7, token=HUGGINGFACEHUB_API_TOKEN)
    
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create a chain for question answering with a retriever from the vector store
    conversation_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    memory=memory,
    input_key="question"  # Change the expected input key
    )

   
    return conversation_chain

@llm_bp.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Ensure a file and question are provided
        if 'file' not in request.files or 'question' not in request.form:
            return jsonify({'error': 'PDF file or question not provided'}), 400

        pdf_file = request.files['file']
        user_question = request.form['question']

        if pdf_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file locally
        filename = secure_filename(pdf_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        pdf_file.save(file_path)

        # Process the PDF
        document_text = load_pdf(file_path)
        documents = chunking(document_text)
        vector_store = embeddings(documents)

        # Create the conversation chain
        conversation_chain = create_llm_chain(vector_store)

        # Get response from the conversation chain
        response = conversation_chain.run({"question": user_question})

        # Return the response
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
