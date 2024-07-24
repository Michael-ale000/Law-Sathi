from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatMessageSerializer
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_groq import ChatGroq
import os ,json
import PyPDF2
import chainlit as cl
import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

# Create your views here.
load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']
llm_groq = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192", temperature=2)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to save/load ChromaDB
CHROMA_DB_PATH = os.path.join(BASE_DIR, 'Chatbot', 'Finaldb')

# Initialize your conversation chain (this would usually be done once and not in the view)
def initialize_chain():
    docsearch = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=OllamaEmbeddings(model="nomic-embed-text"))

    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm_groq,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )
    return chain
# chain = initialize_chain()
# Handle form submission
@csrf_exempt
async def chat_view(request):
    response = ""
    if request.method == 'POST':
         # Parse JSON request body
        data = json.loads(request.body)
        user_input = data.get('user_input', '')
        # print(user_input)

        # Check if user_input is empty or None
        if not user_input:
            return JsonResponse({'response': 'No input provided'}, status=400)
        chain = initialize_chain()
        # cb = cl.AsyncLangchainCallbackHandler()
        # Call the asynchronous function properly with await
        res = await chain.ainvoke(user_input)
        answer = res["answer"]
        # print(answer)
        response = answer
        return JsonResponse({'response': answer})
    return render(request, 'chat.html')

@csrf_exempt
async def temp_view(request):
    response = ""
    if request.method == 'POST':
         # Parse JSON request body
        data = json.loads(request.body)
        user_input = data.get('user_input', '')
        # print(user_input)

        # Check if user_input is empty or None
        if not user_input:
            return JsonResponse({'response': 'No input provided'}, status=400)
        chain = initialize_chain()
        # cb = cl.AsyncLangchainCallbackHandler()
        # Call the asynchronous function properly with await
        res = await chain.ainvoke(user_input)
        answer = res["answer"]
        # print(answer)
        response = answer
        return JsonResponse({'response': answer})
    return render(request, 'temp.html')

