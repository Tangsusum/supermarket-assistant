import requests
import re
import datetime
import json
import html2text
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader

class SupermarketScraper:
    def __init__(self, vectordb, supermarket, url):
        self.vectordb = vectordb
        self.supermarket = supermarket
        self.url = url
        self.filename = f'/tmp/{self.supermarket}.txt'
        self.metadata = {"supermarket": self.supermarket}

    def scrap(self):
        headers = {
            'Content-Type': 'application/json'
        }

        sale_id = None
        if self.supermarket == 'Woolworths':
            sale_id = self.get_sale_id_woolies()
        elif self.supermarket == 'Coles':
            sale_id = self.get_sale_id_coles()

        if not sale_id:
            raise Exception("Invalid Sale Id")
        
        composed_url = re.sub(r'{saleId}', sale_id, self.url)
        print(f'ℹ️ scrapping url: {composed_url}')
        response = requests.request("GET", composed_url, headers=headers)
        steralised_response = re.sub(r'[()]', '', response.text)
        json_decoded = json.loads(steralised_response)

        f = open(self.filename, "w")
        # turn html into text
        f.write(html2text.html2text(json_decoded['content']))
        # append relevant metatdata
        self.metadata['start_date'] = int(datetime.datetime.strptime(json_decoded['startDate'], "%Y-%m-%dT%H:%M:%S").timestamp())
        self.metadata['end_date'] = int(datetime.datetime.strptime(json_decoded['endDate'], "%Y-%m-%dT%H:%M:%S").timestamp())
        self.metadata['description'] = json_decoded['saleName']

        print(f'✅ Got {self.supermarket} catalogue')
        f.close()

    def split_doc(self):
        file = open(self.filename, "r")
        docs = file.read()
        text_splitter = CharacterTextSplitter(separator='!', chunk_size=500, chunk_overlap=50, length_function=len, is_separator_regex=False)
        html_docs = text_splitter.create_documents([docs])
        for idx, _ in enumerate(html_docs):
            html_docs[idx].metadata = self.metadata
        return html_docs
    
    def save_to_vectordb(self):
        self.scrap()
        docs = self.split_doc()
        print(f'✅ Save {self.supermarket} catalogue to DB')
        self.vectordb.save(docs)

    def get_apikey_woolies(self):
        url = "https://www.woolworths.com.au/shop/catalogue?icmpid=sm-prnav-sc-catalogue"
        headers = {
            'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }

        session = requests.session()
        response = session.get(url, headers=headers)
        apikey_pattern = r'apikey=w00lw0rth([A-Za-z0-9]{17})'
        match = re.search(apikey_pattern, response.text)
        if match:
            print('✅ Got Woolies API key')
            return match.group(0)
        
        print('❌ Failed to get Woolies API key')
        return None
    
    def get_sale_id_woolies(self):
        print('getting sale id')
        apikey = self.get_apikey_woolies()
        if apikey:
            url = f"https://webservice.salefinder.com.au/index.php/api/sales/retailer/?id=126&{apikey}&format=json&storeId=4881"
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("GET", url, headers=headers)
            steralised_response = json.loads(response.text)
            print('✅ Got Woolies sale id')
            return steralised_response['items'][0]['items']['saleId']
        
        print('❌ Failed to get Woolies sale id')
        return None
    
    def get_sale_id_coles(self):
        url = "https://embed.salefinder.com.au/catalogues/view/148"
        headers = {
            'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }

        session = requests.session()
        response = session.get(url, headers=headers)
        pattern = r'saleId=(\d{5})'
        match = re.search(pattern, response.text)
        if match:
            print('✅ Got Coles sale id')
            return match.group(1)

        # loader = AsyncChromiumLoader(["https://www.coles.com.au/catalogues"])
        # docs = loader.load()
        # print(docs)
        # for doc in docs:
        #     print(doc.page_content)
        #     
        #     match = re.search(pattern, doc.page_content)
        #     if match:
        #         print('✅ Got Coles sale id')
        #         return match.group(1)
            
        print('❌ Failed to get Coles sale id')
        return None
