from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
from selenium import webdriver

start_url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome('C:/Users/ASUS/Desktop/Python/HW/chromedriver.exe')
browser.get(start_url)
time.sleep(10)
scraped_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,'html.parser')
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "wikitable"}):
            td_tags = tr_tag.find_all("td")
            for index, td_tag in enumerate(td_tags):
                try:
                    temp_list.append(td_tag.find_all('a', attrs = {"class", "wikitable"})[0].contents[0])
                except:
                    temp_list.append() 
        scraped_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

star_df_1 = pd.read_csv("updated_scraped_data.csv")

bright_star_table = soup.find("table",attrs = {"class","wikitable"})
table_body = bright_star_table.find('tbody')
table_rows = table_body.find_all('tr')

for row in table_rows:
    table_cols = row.find_all('td')
    temp_list = []

for col_data in table_cols:
    data = col_data.text.strip()
    temp_list.append(data)
    scraped_data.append(temp_list)

stars_data = []

for i in range(0,len(scraped_data)):
    Star_names = scraped_data[i][1]
    Distance = scraped_data[i][3]
    Mass = scraped_data[i][5]
    Radius = scraped_data[i][6]
    Lum = scraped_data[i][7]

    required_data = [Star_names,Distance,Mass,Radius,Lum]
    stars_data.append(required_data)

headers = ['Star_name','Distance','Mass','Radius','Luminosity']

star_df_1 = pd.DataFrame(stars_data, columns=headers)
star_df_1.to_cvs('scraped_data.csv',index = True, index_label = 'id')