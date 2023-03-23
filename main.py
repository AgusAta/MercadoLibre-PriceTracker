from bs4 import BeautifulSoup
import requests
import numpy as np
import csv
from datetime import datetime

#This is where you enter your desired link
link = "https://listado.mercadolibre.com.ar/playstation-5#D"

#As the name suggest, this function gets the price
def get_prices_by_link(link):
    #This will get the source
    r = requests.get(link)
    #Parse source
    page_parse = BeautifulSoup(r.text, "html.parser")
    #Find items from search
    search_results = page_parse.find("ol", {"class": "ui-search-layout ui-search-layout--stack shops__layout"}).find_all("li", {"class": "ui-search-layout__item shops__layout-item"})

    item_prices = []

    #Loops results in order to get every single one
    for result in search_results:
        price_as_text = result.find("span", {"class": "price-tag-text-sr-only"}).text
        if "Antes" in price_as_text:
            continue
        price = float(price_as_text[:].replace("pesos", ""))
        item_prices.append(price)
        item_prices.sort()
    return item_prices

#Removes anything that's not specified before
def remove_outliers(prices, m=2):
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

#Gets the average of the page
def get_average(prices):
    return np.mean(prices)

#Saves the average price into a csv file named "prices" with the date
def save_prices(prices):
    fields = [datetime.today().strftime("%B-%D-%Y"), np.around(get_average(prices), 2)]
    with open("prices.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == "__main__":
    prices = get_prices_by_link(link)
    prices_without_outliers = remove_outliers(prices)
    print(get_average(prices_without_outliers))
    print(get_prices_by_link(link))
    save_prices(prices)
