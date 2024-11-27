from assistant import assistant
from supermarket_scraper import SupermarketScraper
from vectordb import VectorDB

user = "Is chocolate on sale?"

# print(assistant(user))
vectordb = VectorDB().load()
print(vectordb.get())
# suermarket = SupermarketScraper(VectorDB(), "Coles", "https://embed.salefinder.com.au/productlist/view/{saleId}/?rows_per_page=" + "5")
# suermarket.get_sale_id_coles()
# supermarket =  SupermarketScraper(VectorDB(), "Woolworths","https://embed.salefinder.com.au/productlist/view/{saleId}/?rows_per_page=" + "5")
# supermarket.scrap()