import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
sheet_url = "https://docs.google.com/forms/d/e/1FAIpQLScDAJdvFdxGS6kr0VFZUm7QxL2dySpQB1qFvefJWD03V84M3g/viewform?usp=header"
link = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(link)
response.raise_for_status()
data = response.text
soup = BeautifulSoup(data,"html.parser")

links_elements = soup.select(".StyledPropertyCardDataWrapper a")

links = [link["href"] for link in links_elements]

address_elements = soup.select(".StyledPropertyCardDataWrapper address")

addresses = [address.text.strip() for address in address_elements]

price_elements = soup.select(".PropertyCardWrapper span")
prices = [price.text for price in price_elements]
# print(prices)

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.get(sheet_url)




def write_to_google_docs(link,address,price,driver):
    address_answer_box = driver.find_elements(By.CSS_SELECTOR,".whsOnd.zHQkBf")[0]
    price_answer_box = driver.find_elements(By.CSS_SELECTOR,".whsOnd.zHQkBf")[1]
    link_answer_box = driver.find_elements(By.CSS_SELECTOR,".whsOnd.zHQkBf")[2]
    time.sleep(2)
    address_answer_box.send_keys(str(address))
    price_answer_box.send_keys(str(price))
    link_answer_box.send_keys(str(link))
    send = driver.find_element(By.CSS_SELECTOR,".NPEfkd.RveJvd.snByac")
    send.click()
    time.sleep(3)
    return_box = driver.find_element(By.CSS_SELECTOR,".c2gzEf a")
    return_box.click()
    time.sleep(3)
    
for address,price,link in zip(addresses,prices,links):
    write_to_google_docs(link=link,address=address,price=price,driver=driver)
    
driver.quit()