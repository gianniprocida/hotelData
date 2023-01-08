import time
from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
from collections import deque
import itertools

"""Scraping the first ten links from booking.com """
def grab_links():
    wd=webdriver.Chrome('/usr/bin/chromedriver')

    url="https://www.booking.com/index.html?aid=376363;label=booking-name-L*Xf2U1sq4*GEkIwcLOALQS267777916054:pl:ta:p1:p22,563,000:ac:ap:neg:fi:tiaud-1183547561427:kwd-65526620:lp9043675:li:dec:dm:ppccp=UmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1XFzPnqOODws;ws=&gclid=Cj0KCQjwz7uRBhDRARIsAFqjulkeeGiMTlJ3WPwKB6U6QJxBtBYefQPt9AaQakNLY8PeTGRCAa1sIbQaAiF0EALw_wcB"

    wd.get(url)

    search_bar=wd.find_element(By.ID,'ss')

    time.sleep(4)

    search_bar.send_keys('Berlin')

    search_bar.send_keys(Keys.ENTER)

    try:
        div = WebDriverWait(wd, 20).until(
         EC.presence_of_element_located(
             (By.CLASS_NAME, "e13098a59f"))
     )  
        hrefs = wd.find_elements(By.XPATH,"//a[@class='e13098a59f']")
        q = deque()
        links = [ i.get_property('href') for i in hrefs]

        for i in links[1:15]:
            q.append(i)

    except TimeoutError as e:
        print(e)
        wd.quit()

    return q