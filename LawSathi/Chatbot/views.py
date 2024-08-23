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
from .models import UnknownQuerys,FileUploads
from LawyerRecommendation.models import  Address, LawyerDetails,Lawyerdataset,Booking
from NewsPortal.models import MoreUserInfo
from django.db.models import Count, Avg
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']
# llm_groq = ChatGroq(groq_api_key=groq_api_key, model_name="llama3.1-70b-versatile", temperature=2)
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
    if request.method == 'POST':
        # Parse JSON request body
        data = json.loads(request.body)
        user_input = data.get('user_input', '')

        # Check if user_input is empty or None
        if not user_input:
            return JsonResponse({'response': 'No input provided'}, status=400)

        chain = initialize_chain()

        # Call the asynchronous function properly with await
        res = await chain.ainvoke(user_input)
        answer = res["answer"]

        # Store the conversation in the session
        conversation = await sync_to_async(request.session.get, thread_sensitive=True)('conversation', [])
        conversation.append({'user': user_input, 'bot': answer})
        await sync_to_async(request.session.__setitem__, thread_sensitive=True)('conversation', conversation)
        await sync_to_async(request.session.save, thread_sensitive=True)()

        return JsonResponse({'response': answer})

    elif request.method == 'GET':
        # Load conversation from session
        conversation = await sync_to_async(request.session.get, thread_sensitive=True)('conversation', [])

        # Render template with conversation
        html = render_to_string('chat.html', {'conversation': conversation})
        return HttpResponse(html)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# async def chat_view(request):
#     if request.method == 'POST':
#         # Parse JSON request body
#         data = json.loads(request.body)
#         user_input = data.get('user_input', '')

#         # Check if user_input is empty or None
#         if not user_input:
#             return JsonResponse({'response': 'No input provided'}, status=400)

#         chain = initialize_chain()

#         # Call the asynchronous function properly with await
#         res = await chain.ainvoke(user_input)
#         answer = res["answer"]

#         return JsonResponse({'response': answer})

#     elif request.method == 'GET':
#         # Asynchronous context: manually render template synchronously
#         html = render_to_string('chat.html')
#         return HttpResponse(html)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def report(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('user_query')
            bot_response = data.get('bot_response')

            # Save to the unknown query model or any other appropriate model
            UnknownQuerys.objects.create(user_query=user_query, bot_responses=bot_response)

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            print('Invalid JSON')
            return JsonResponse({'status': 'fail', 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=500)

    print('Invalid Request Method')
    return JsonResponse({'status': 'fail', 'error': 'Invalid request method'}, status=400)

def dashboard_data(request):
    # General Users: Users with MoreUserInfo but not lawyers
    general_users_count = MoreUserInfo.objects.filter(user__lawyerdetails__isnull=True).count()
    
    # Lawyers: Users with both MoreUserInfo and LawyerDetails
    lawyers_count = LawyerDetails.objects.count()

    # Staff: Users who are staff
    staff_count = User.objects.filter(is_staff=True).count()

    # Superusers: Users who are superusers
    superusers_count = User.objects.filter(is_superuser=True).count()
    
    # Total Users: All users
    total_users_count = User.objects.count()

    # Lawyers by Province using Lawyerdataset model
    lawyers_by_province = Lawyerdataset.objects.values('province').annotate(count=Count('province'))

    booking_status_counts = Booking.objects.values('status').annotate(count=Count('status'))

    lawyer_statuses = list(LawyerDetails.objects.values('status').annotate(count=Count('status')))
    handled_queries_count = UnknownQuerys.objects.filter(handled=True).count()
    unhandled_queries_count = UnknownQuerys.objects.filter(handled=False).count()
    file_count = FileUploads.objects.count()

    data = {
        'general_users_count': general_users_count,
        'lawyers_count': lawyers_count,
        'staff_count': staff_count,
        'superusers_count': superusers_count,
        'total_users_count': total_users_count,
        'lawyers_by_province': list(lawyers_by_province),  # Updated to use Lawyerdataset
        'lawyer_statuses': lawyer_statuses,
        'handled_queries_count': handled_queries_count,
        'unhandled_queries_count': unhandled_queries_count,
        'file_count': file_count,
         'booking_status_counts': list(booking_status_counts),  # Add this line
    }

    return JsonResponse(data)
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

