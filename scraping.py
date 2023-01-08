import requests
from bs4 import  BeautifulSoup
import json
import re
import pandas as pd
from textblob import TextBlob
from collections import deque, defaultdict

"""Scaping data from the URL below"""
""" Use Chromium Web Browser to loop uo the html content"""
headers = {"User-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}
URL = "https://www.booking.com/hotel/de/kempinskibristolberlin.en-gb.html?aid=1649686;label=kempinskibristolberlin-BxmtH89CeFt5COrk%2AP71ywS323958243077%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atiaud-617622003811%3Akwd-395949224771%3Alp9043675%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YdwTcLIbWZlfefYGj3m2lIc;sid=716df04b0ec19f628bf5155e8ffa1fa5;all_sr_blocks=6066428_340785799_2_2_0;checkin=2022-02-10;checkout=2022-02-11;dest_id=-1746443;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=6066428_340785799_2_2_0;hpos=1;matching_block_id=6066428_340785799_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=6066428_340785799_2_2_0__13356;srepoch=1643632855;srpvid=b32a592a2c420297;type=total;ucfs=1&#tab-main"
url="https://www.booking.com/hotel/de/precise-tale-berlin.en-gb.html?aid=1649686&label=kempinskibristolberlin-BxmtH89CeFt5COrk%2AP71ywS323958243077%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atiaud-617622003811%3Akwd-395949224771%3Alp9043675%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YdwTcLIbWZlfefYGj3m2lIc&sid=cb953c75d3a16fbfb02e176ba32b2278&dest_id=-1746443;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=3;hpos=3;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1662654895;srpvid=d6c374962567011c;type=total;ucfs=1&#hotelTmpl"
class hotelWebsite():
    def __init__(self,URL):
        self.URL = URL
        self.r = requests.get(self.URL,headers)
        self.webpage = BeautifulSoup(self.r.content,"html.parser")

    def get_stars(self):
        span_ratingCircle = self.webpage.find('span',class_="fbb11b26f5 e23c0b1d74")
        countStars=0
        for child in span_ratingCircle:
            countStars+=1
        return (countStars)

    def get_Info(self):
        if self.webpage.find('h2'):
            hotelName = self.webpage.find('h2',class_="pp-header__title").get_text().splitlines()[1]

        if self.webpage.find('span'):
           string_withAddress = self.webpage.find('span',
                                                class_="hp_address_subtitle js-hp_address_subtitle jq_tooltip").get_text().split()
           for i in range(len(string_withAddress)):
               if ',' in string_withAddress[i]:
                   string_withAddress[i] = string_withAddress[i].replace(',',"")

           streetName = f'{string_withAddress[0]}{string_withAddress[1]}'
         #  houseNumber = f'{string_withAddress[1]}'
         #  borough = f'{string_withAddress[2]}'
         #  cap = f'{string_withAddress[3]}'

           # Get stars
           span_ratingCircle = self.webpage.find('span',
                                                 class_="fbb11b26f5 e23c0b1d74")
           countStars = 0
           for child in span_ratingCircle:
               countStars += 1
           return (hotelName,streetName,countStars)



    def get_reviews(self):
        scores = [ i.get_text() for i in self.webpage.find_all('span',class_='c-score-bar__score')]
        scores = [float(i) for i in scores]
        categories = [ j.get_text().replace("\xa0"," ") for j in self.webpage.find_all('span',class_='c-score-bar__title')]
        tup = zip(categories,scores)
        cat_scorewithDupl = list(tup)
        s = set()
        cat_score = []
        for i in cat_scorewithDupl:
            if i not in s:
                s.add(i)
                cat_score.append(i)
            elif i in s:
                break
        scores = []

        for cat,score in cat_score:
            scores.append(score)
        scores = tuple(scores)
        # s = set()
        # for i in tup:
        #     if i not in s:
        #         s.add(i)
        # Categ_Score = list(s) # List of tuples
        return scores


    def get_PopularFacilities(self):
        PopFac_withDuplicates=[]
        for i in self.webpage.find_all('div',class_="important_facility"):
            PopFac_withDuplicates.append(i.get_text().strip())
        for i in range(len(PopFac_withDuplicates)):
            PopFac_withDuplicates[i] = ('_'.join(PopFac_withDuplicates[i].split()),'YES')

        d = dict.fromkeys(['Free_WiFi', 'Family_rooms', 'Pets_allowed', 'Non-smoking_rooms',
                           'Restaurant', 'Facilities_for_disabled_guests','Heating'])
        d = defaultdict(lambda: False,d)
        # Remove duplicates ( which occur at the end of the list)
        PopFac = []
        s = set()

        for i in PopFac_withDuplicates:
            if i not in s:
                s.add(i)
                PopFac.append(i)
            elif i in s:
                break
            else:
                pass
        for key,value in PopFac:
            if key in d:
                d[key] = 'YES'
        PopFac = tuple(d.values())
        return PopFac



if __name__=='__main__':

     hotel_bristolberlin = hotelWebsite(url)
    #
    # streetName,_,_,_ = hotel_bristolberlin.get_address()
    #
    # _,houseNumber,_,_ = hotel_bristolberlin.get_address()
    #
    # _,_,borough,_ = hotel_bristolberlin.get_address()
    #
    # _,_,_,cap = hotel_bristolberlin.get_address()

    # d = {'HotelName':hotel_bristolberlin.get_hotelname(),
    #      'StreetName':streetName,'HouseNumber':houseNumber,
    #      'borough':borough,'cap':cap,
    #      'Stars':hotel_bristolberlin.get_stars(),'Reviews':hotel_bristolberlin.get_reviews(),
    #      'Facilities':hotel_bristolberlin.get_PopularFacilities()
    #      }



    # d={'Address':hotel_bristolberlin.get_address(),
    #    'Stars':hotel_bristolberlin.get_stars(),
    #            'Stars':hotel_bristolberlin.get_stars(),'Address':hotel_bristolberlin.get_address(),
    #       'Det':hotel_bristolberlin.get_roomsTable(),
    #      'Reviews':hotel_bristolberlin.get_reviews(),
    #    'WhatTheyLoved':hotel_bristolberlin.get_whattheylovedTable()}
