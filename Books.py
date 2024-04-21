import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

Datas = {
    'Book':[],
    'Type': [],
    'Price':[],
    'Stocks':[],
    'Review':[]
}
Ratings = {
    'One'   : 1,
    'Two'   : 2,
    'Three' : 3,
    'Four'  : 4,
    'Five'  : 5,
}
Path = "https://books.toscrape.com/catalogue"
# Fetching  the url and returning the soup object
def Fetch(url):
    req = requests.get(url).content
    soup_object = BeautifulSoup(req , 'lxml')
    return soup_object

#new link to another page. This function returns stocks  and type
def Description_page(Path , api):
    url = Path + api
    soup = Fetch(url)
    li_tags = soup.select("ul.breadcrumb")[0].find_all("li")
    Type = li_tags[2].get_text().strip()
    stock = soup.find("p" , class_="instock availability").get_text()
    return [Type,stock]




# creating a Soup object
def scrape():
        for page in range(1, 51):
            url = pagination(page)
            soup = Fetch(url)
            Books = soup.find_all("li" , class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
            for book in Books:
                title = book.find("h3").find("a").get("title")
                description_url = book.find("h3").find("a")['href']
                description_url = description_url[5:]
                price = book.find("p" , class_="price_color").get_text()
                review = book.find("p" , class_="star-rating")
                review = Ratings[review.get("class")[1]]
                Type , stock = Description_page(Path , description_url)
                stock = stock.split()
                stock = stock[2][1:]
                Datas['Book'].append(title)
                Datas['Price'].append(price)
                Datas['Review'].append(review)
                Datas['Stocks'].append(stock)
                Datas['Type'].append(Type)
                print(title)


#function to go the next page 
def pagination(page):
        if(page == 1):
            url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
        else:
            url = f"https://books.toscrape.com/catalogue/category/books_1/page-{page}.html"
        return url

#automating the file it will scrape every 10 minutes and modify the changes
if __name__ == '__main__':
    scrape()
    time_wait = 10
    time.sleep(time_wait  * 60)
    df = pd.DataFrame.from_dict(Datas)
    df.to_csv('BooksData/books_info.csv' , index=False)
