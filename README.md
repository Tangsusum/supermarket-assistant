# Supermarket Catelogue Assistant with RAG

The Retrieval-Augmented Generation (RAG) model combines retrieval-based and generative-based approaches in natural language processing (NLP). RAG's retriever module enables efficient filtering through vast amounts of data and provides the LLM with relevant documents to intelligently synthesise responses using the retrieved information.

This project introduces a supermarket assistant empowered by Retrieval-Augmented Generation (RAG), designed to streamline the retrieval of Weekly Specials Catalogues from two Australian supermarkets: Coles and Woolworths. Leveraging RAG, the model efficiently extracts item details embedded within HTML code, segments the documents, and stores them in the Chroma vectorDB. When prompted by a user query, the model retrieves pertinent documents and presents selection of items from both Coles and Woolworths. Each item is accompanied by comprehensive information including product name, discounted price, and a relevant image.

USAGE
------------
The model contains data from Woolworths and Coles Specials catalogue and would update vectorDB with the latest catalgoue upon expiry.
To interact with the supermarket assistant, input your question into the ***user*** variable and run ***main.py***.


EXAMPLE
------------
```
User: 
Is chocolate on sale?

Assistant:
Item: Cadbury Medium Bars or Europe Bars 30-60g
Supermarket: Woolworths
Discounted price: $1.25
Discount percentage: 50%
Image Source: https://dduhxx0oznf63.cloudfront.net/images/thumbs/ipad/546611006_0831cf2131eebe5.jpg

Item: Mars M&M's, Maltesers or Pods 120g-180g
Supermarket: Coles
Discounted price: $3.00
Discount percentage: 50%
Image Source: https://dduhxx0oznf63.cloudfront.net/images/products/160x170/546321008_c4fa46de76fe6b9.jpg

Item: Life Savers 150-200g or Darrell Lea Nibs 200g
Supermarket: Woolworths
Discounted price: $2.50
Discount percentage: 50%
Image Source: https://dduhxx0oznf63.cloudfront.net/images/thumbs/ipad/546611008_0831cf2131eebe5.jpg
```