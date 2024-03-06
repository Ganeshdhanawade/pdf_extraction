import google.generativeai as genai
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from PyPDF2 import PdfReader,PdfFileReader
import os
import io

#from langchain.vectorstores import faiss
from langchain.vectorstores import faiss
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
#genai.configure(api_key="YOUR_API_KEY")


class utils:
    ## reade each pdf and get text insite it
    def get_pdf_text(pdf_docs):
        text=''
        for pdf in pdf_docs:
            #string_io = io.BytesIO(pdf_docs.get_value()   #decode('utf-8')) #getvalues())
            pdf_reader=PdfReader(pdf_docs)
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        
 
    ## find the chunks of pdf
    def get_text_chunks(text):
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
        chunks=text_splitter.split_text(text)
        return chunks

    ### store that chunks in vectors with text embedding
    def get_vector_store(text_chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
        vector_store = faiss.FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")

    ### create that quation answer of pdf containt
    def get_conversational_chain():

        prompt_template = """
        Your main objective is to learn all the paper and according to paper 
        you can take the perfect summary and according to user requirement you provide the detail information becouse user need the brief information about all the paper not a small
        containt, so make shure your answer is perfect for user.\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """

        model = ChatGoogleGenerativeAI(model="gemini-pro",
                                temperature=0.3)

        prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        return chain