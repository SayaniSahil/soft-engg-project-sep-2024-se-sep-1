import pytest
from flask import Flask
from components.llm import ask_question  
import io


def test_ask_question_no_file_or_question(admin_setup_data):
    """Test the case where neither file nor question is provided."""
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    response = client.post('/ask')
    assert response.status_code == 400
    assert response.json == {'error': 'PDF file or question not provided'}

def test_ask_question_no_file(admin_setup_data):
    
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    """Test the case where no file is provided."""
    response = client.post('/ask', data={'question': 'What is AI?'},headers=headers)
    assert response.status_code == 400
    assert response.json == {'error': 'PDF file or question not provided'}

def test_ask_question_no_question(admin_setup_data):
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    """Test the case where no question is provided."""
    data = {'file': (io.BytesIO(b'This is a PDF content'), 'example.pdf')}
    response = client.post('/ask', data=data,headers=headers)
    assert response.status_code == 400
    assert response.json == {'error': 'PDF file or question not provided'}

def test_ask_question_empty_file(admin_setup_data):
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    """Test the case where an empty file is uploaded."""
    data = {
        'file': (io.BytesIO(b''), 'example.pdf'),
        'question': 'What is AI?'
    }
    response = client.post('/ask', data=data,headers=headers)
    assert response.status_code == 400
    assert response.json == {'error': 'No selected file'}

def test_ask_question_valid_request(admin_setup_data, mocker):
    token,client=admin_setup_data
    headers={'Authentication-Token': f'{token}'}
    """Test a valid request."""
    # Mocking the required functions to avoid actual processing
    mocker.patch('your_flask_app.load_pdf', return_value="This is sample text from a PDF.")
    mocker.patch('your_flask_app.chunking', return_value=["Chunked text"])
    mocker.patch('your_flask_app.embeddings', return_value="Mocked vector store")
    mocker.patch('your_flask_app.create_llm_chain', return_value=type('MockChain', (), {"run": lambda self, x: "Mocked response"}))

    data = {
        'file': (io.BytesIO(b'This is a PDF content'), 'example.pdf'),
        'question': 'What is AI?'
    }
    response = client.post('/ask', data=data,headers=headers)
    assert response.status_code == 200
    assert response.json == {'response': 'Mocked response'}

def test_ask_question_exception(client, mocker):
    """Test handling of an exception in the endpoint."""
    # Mocking load_pdf to raise an exception
    mocker.patch('your_flask_app.load_pdf', side_effect=Exception("Mocked exception"))

    data = {
        'file': (io.BytesIO(b'This is a PDF content'), 'example.pdf'),
        'question': 'What is AI?'
    }
    response = client.post('/ask', data=data)
    assert response.status_code == 500
    assert response.json == {'error': 'Mocked exception'}