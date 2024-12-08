from flask import Flask, request, jsonify, Blueprint,redirect,session
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

# UPLOAD_FOLDER = 'uploads'  # Create this folder in your project directory
ALLOWED_EXTENSIONS = {'pdf'}

# llm_bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

load_dotenv()  # Load .env file

HF_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
UPLOAD_FOLDER = "./uploads"  # Folder to store uploaded PDFs
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

file_path = ''

# @llm_bp.route('/upload', methods=['POST'])
# def load_pdf(file_path):
#     # Read the PDF from the local file system
#     with open(file_path, "rb") as file:
#         pdf_reader = PdfReader(file)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text() + '\n'
#     return text

# @llm_bp.route('/upload', methods=['GET', 'POST'])
# def load_pdf():
#     if request.method == 'POST':
#         # Check if a file is uploaded
#         if 'document' not in request.files:
#             return {"No file uploaded"}, 400

#         file = request.files['document']

#         # Check if the file is not empty
#         if file.filename == '':
#             return {"No file selected"}, 400

#         # Process the file
#         if file:
#             try:
#                 pdf_reader = PdfReader(file)
#                 text = ""
#                 for page in pdf_reader.pages:
#                     text += page.extract_text() + '\n'
#                 return text  # Return extracted text as response
#             except Exception as e:
#                 return f"Error reading PDF: {e}", 500



def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@llm_bp.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request has a file part
    global file_path
    print(request)
    if 'document' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['document']

    # Check if a file was selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Validate the file type
    if file and allowed_file(file.filename):
        # Secure the filename and save it to the upload folder
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # You can now process the PDF if needed
        return redirect("localhost:5173")

    return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400
            


def chunking(document_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    documents = text_splitter.create_documents([document_text])
    return documents

def embeddings(documents):
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L12-v2", model_kwargs={"trust_remote_code": True})
    vector_store = FAISS.from_documents(documents, embedding_model)
    return vector_store


# The chain for the question and answer

def create_llm_chain(vectorstore):
    template = """Given the following user question answer the question. 
    Context: {context}
    Question: {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=800,  token=HUGGINGFACEHUB_API_TOKEN)
    
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create a chain for question answering with a retriever from the vector store
    conversation_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type = "stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    chain_type_kwargs={
        "prompt":prompt
    },
    memory=memory,
    )
    return conversation_chain



@llm_bp.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Ensure a file and question are provided
        # if 'file' not in request.files or 'question' not in request.form:
        #     return jsonify({'error': 'PDF file or question not provided'}), 400

        global file_path
        print(file_path)
        
        body = request.get_json()
        user_question = body.get('question')

        if file_path == '':
            return jsonify({'error': 'No selected file'}), 400

        # Process the PDF
        pdf_reader = PdfReader(file_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + '\n'
        
        document_text = text
        documents = chunking(document_text)
        vector_store = embeddings(documents)

        # Create the conversation chain
        conversation_chain = create_llm_chain(vector_store)

        # Get response from the conversation chain
        print(user_question)
        response = conversation_chain.run(user_question)

        # Return the response
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# The chain for generating the milestones

def generate_milestone(vectorstore):
    template = """ 
    You are helping the instructor generate tasks (milestones) to guide the students and maintain a check on their project progress. 

    1. You will get an input number of milestones in numbers example: 1,2,4,5....[X]. Where X is a number. 
    Your job is to generate milestone descriptions. 

    2. Maintain a flow in the breakdown of the project description into milestones. 

    **OUTPUT**

    1. Give the output in the following format.

    *** Title: Title of the Milestone (in not more than 10 words)

    *** Description: Description of the milestone

    *** "END" (Add this keyword "END" at the end of each milestone to delimit and seperate the different milestones distinctively)


    **RESPONSE TYPE**

    Give the output in [X] number of descriptions as the number of milestones mentioned ONLY.  Where X is a number of milestones recieved as an input.

    Context: {context}
    Number of Milestones : {question}

    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    llm = HuggingFaceEndpoint(repo_id=repo_id, token=HUGGINGFACEHUB_API_TOKEN)
    
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create a chain for question answering with a retriever from the vector store
    conversation_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type = "stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    chain_type_kwargs={
        "prompt":prompt
    },
    memory=memory,
    )
    return conversation_chain



@llm_bp.route('/milestone', methods=['POST'])
def generate_milestones():
    try:
        DELIMITER = "END"
        body = request.get_json()
        project_desc = body.get('description')
        number_of_milestones = body.get('numbermilestones')

        if project_desc == '':
            return jsonify({'error': 'Enter the project Description'}), 400

        
        document_text = f"""Project Description : {project_desc}"""
        documents = chunking(document_text)
        vector_store = embeddings(documents)

        # Create the conversation chain
        conversation_chain = generate_milestone(vector_store)

        # Get response from the conversation chain
        print(number_of_milestones)
        string_response = conversation_chain.run(str(number_of_milestones))

        response = string_response.split(DELIMITER)
        titles = []
        descriptions = []
        for i in range(len(response)-1):
            response[i] = response[i].split('Title: ')[1]
            temp = response[i].split('Description: ')
            titles.append(temp[0].split('\n')[0])
            descriptions.append(temp[1].split('\n')[0])
        
        response = (titles,descriptions)
        # Return the response 
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

