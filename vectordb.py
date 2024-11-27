# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

class VectorDB:
    def __init__(self):
        self.collection_name = "supermarket_collection"
        # self.persist_directory = '/tmp/chroma_db'
        chromadb.HttpClient(host="54.79.182.224", port=8000)
        self.vectordb = None

    def save(self, docs):
        self.vectordb = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings(), collection_name=self.collection_name)
        print('✅ Done saving to Chroma')
        return self.vectordb
    
    def load(self):
        self.vectordb = Chroma(embedding_function=OpenAIEmbeddings(), collection_name=self.collection_name)
        return self.vectordb
    
    def delete(self):
        if not self.vectordb:
            self.vectordb = self.load()
        print('✅ Done deleting Chroma collection')
        self.vectordb.delete_collection()