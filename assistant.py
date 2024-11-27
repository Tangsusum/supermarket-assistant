import datetime
from vectordb import VectorDB
from supermarket_scraper import SupermarketScraper
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_openai import (ChatOpenAI, OpenAI)
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

def scrap_supermarkets(item_num):
    vectordb_init = VectorDB()
    # clean up before re-scraping pages
    vectordb_init.delete()
    coles = SupermarketScraper(vectordb_init, "Coles", "https://embed.salefinder.com.au/productlist/view/{saleId}/?rows_per_page=" + item_num)
    coles.save_to_vectordb()
    woolies = SupermarketScraper(vectordb_init, "Woolworths","https://embed.salefinder.com.au/productlist/view/{saleId}/?rows_per_page=" + item_num)
    woolies.save_to_vectordb()
    return vectordb_init.load()

def vectordb_checks():
    ITEM_NUM = "10"
    vectordb = VectorDB().load()
    now = datetime.datetime.timestamp(datetime.datetime.now())
    current_docs = vectordb.get()

    # fetch data if vecotr store is empty
    if len(current_docs['documents']) == 0:
        return scrap_supermarkets(ITEM_NUM)
    if now > current_docs['metadatas'][0]['end_date']:
        # check if the catelogue has expired, if so scrap new data
        return scrap_supermarkets(ITEM_NUM)
    # return vectordb if pass all checks
    print('✅ VectorDB passes all checks')
    return vectordb

def assistant(question):
    vectordb = vectordb_checks()
    metadata_field_info = [
        AttributeInfo(
            name="supermarket",
            description="The supermarket the item is from.",
            type="string",
        ),
        AttributeInfo(
            name="description",
            description="Description of the html page.",
            type="string",
        ),
    ]
    llm = OpenAI(temperature=0.3)
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vectordb,
        "Supermarket items information",
        metadata_field_info,
        verbose=True
    )

    template="""
        You are a supermarket assiant who has knowledge to two super supermarkets - Coles and Woolworths' catalogue pages and will determine if items of interest are available to the user.
        Only use information from these html pages and do not return items that are not from the html pages.
        Find all relevant item(s) from both Woolworths and Coles unless specified.
        The now discounted price is in a span tag with class 'sf-pricedisplay'.
        Provide which supermarket is the item from (get the information from the document's metadata, supermarket attribute), the item's name, the now discounted price, and the percentage discount for the item.
        Include the item's image source url.
        
        For example provide answer in the following format. <> act as placeholder for the item details.
        Display all relevant items to the user and do not limit the number of items shown to the user:
        Item: <Item Name>
        Supermarket: <Supermarket Name>
        Discounted price: <Price>
        Discount percentage: <Discount Percentage>
        Image Source: <Image Source>

        {context}
        Question: {question}
        Helpful Answer:"""

    custom_rag_prompt = PromptTemplate.from_template(template)

    llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")

    rag_chain = (
        {"context": retriever, "question":  RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    # for chunk in rag_chain.stream(question):
    #     print(chunk, end="", flush=True)

    return rag_chain.invoke(question)