from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from constants import PERSIST_DIR, EMBEDDING_MODEL, LLM_MODEL, LLM_CONFIG
import os
import time
def load_existing_vectordb():
    if os.path.exists(os.path.join(PERSIST_DIR, "chroma-collections.parquet")):
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    return None

def create_vectordb(documents):
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    vectordb.persist()
    return vectordb

def create_retrieval_chain(vectordb):
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    llm = Ollama(model=LLM_MODEL, **LLM_CONFIG)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff"
    )