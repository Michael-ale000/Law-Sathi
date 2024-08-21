from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from .models import FileUploads,UnknownQuerys
import os,PyPDF2
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from django.template.response import TemplateResponse


# Register your models here.

# file upload admin

class FileUploadAdmin(admin.ModelAdmin):

    list_display = ('name','file','uploaded_by','uploaded_date', 'description')
    search_fields = ('name', 'description')
    readonly_fields = ('uploaded_date', 'uploaded_by')  # Make these fields read-only
    # variables for chroma db
   

    def save_model(self,request,obj,form,change):
        if not obj.pk:
            obj.uploaded_by = request.user
        super().save_model(request,obj,form,change)

        if not change :
            self.process_and_store_embeddings(obj)

    def process_and_store_embeddings(self, file_upload):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        CHROMA_DB_PATH =os.path.join(BASE_DIR, 'Chatbot', 'Finaldb')
        file_path = file_upload.file.path
        texts = []
        metadatas = []

         # Read the PDF file
        with open(file_path, "rb") as file:
            pdf = PyPDF2.PdfReader(file)
            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text()

            # Split the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=50)
            file_texts = text_splitter.split_text(pdf_text)
            texts.extend(file_texts)

            # Create metadata for each chunk
            file_metadatas = [{"source": f"{i}-{os.path.basename(file_path)}"} for i in range(len(file_texts))]
            metadatas.extend(file_metadatas)

            # Create a Chroma vector store
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        docsearch = Chroma.from_texts(texts, embeddings, metadatas=metadatas, persist_directory=CHROMA_DB_PATH)

admin.site.register(FileUploads,FileUploadAdmin)


# for handeling unknown query
@admin.register(UnknownQuerys)
class UnknownQueryAdmin(admin.ModelAdmin):
    list_display = ('user_query', 'bot_responses', 'bot_querytimestamp', 'handled')  # Fix spacing and add missing comma
    list_filter = ('handled',)

    actions = ['mark_as_handled']

    def mark_as_handled(self, request, queryset):
        queryset.update(handled=True)
    mark_as_handled.short_description = "Mark selected queries as handled"




        