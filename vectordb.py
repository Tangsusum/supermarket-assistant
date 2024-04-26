from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class VectorDB:
    def __init__(self):
        self.persist_directory = './chroma_db'
        self.vectordb = None

    def save(self, docs):
        self.vectordb = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings(), persist_directory=self.persist_directory)
        print('✅ Done saving to Chroma')
        return self.vectordb
    
    def load(self):
        self.vectordb = Chroma(persist_directory=self.persist_directory, embedding_function=OpenAIEmbeddings())
        return self.vectordb
    
    def delete(self):
        if not self.vectordb:
            self.vectordb = self.load()
        print('✅ Done deleting Chroma collection')
        self.vectordb.delete_collection()