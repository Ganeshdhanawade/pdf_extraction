from Utiles import utils
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import faiss
import streamlit as st

def user_input(user_quation):

    embeddings =GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    ##check the similer word in faiss embedding of input dataset
    new_db =faiss.FAISS.load_local('faiss_index',embeddings)
    docs=new_db.similarity_search(user_quation)
     
    ##tell the quation with the chain
    chain=utils.get_conversational_chain()
    
    
    response = chain(
        {"input_documents":docs, "question": user_quation}
        , return_only_outputs=True)
    
    #print(response)
    st.write("Reply: ", response["output_text"])
