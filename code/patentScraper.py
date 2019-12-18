"""
    File:       patentScraper.py
    Author:     Pascal Jardin
    Date:       5/26/2019
    Version:    1
    Description:
                    This is a webscapper for patents using google.
                Goggle is used becouse it has already grabbed some
                of the text from the patents. Pattent data is then
                stored in pdf and txt folders. When the page gives
                a 404, then that means the patent does not exist
                and will stop the program.
"""

import requests                 #to get webpage
import sys                      #to exit out of program
import os                       #to find program's location
from bs4 import BeautifulSoup   #to decifer webpage

#this is needed, so you dont have to manually update paths
location = os.path.realpath(__file__)
location = location[:-22]

num = 1

#infinate loop till find patent that does not exist
while True:

    page = requests.get("https://patents.google.com/patent/US" + str(num))

    soup = BeautifulSoup(page.content, 'html.parser')

    patent_text = soup.find_all('p')

    #means patents does not exists, so exit and return what was the last patent
    if (patent_text[0].get_text().find("404") != -1):
        print("last patent: US"+str(num - 1))
        sys.exit()

    #gives an update on what curent patent
    print("US" + str(num))

    #from googl's decifer of patents text, store it i txt folder
    with open(location +"/data/txt/US"+str(num)+".txt", "w") as text_file:
        for pt in patent_text:
            text_file.write(pt.get_text() + "\n")


    #pdf name
    pdf = "US"+str(num)+".pdf"

    #url of patent pdf
    href = ""

    #could not get find class to work, so looks through all hrefs and returns what i want
    href_tags = soup.find_all(href=True)
    for tag in href_tags:
        if tag['href'].find(pdf) != -1:
            href = tag['href']
            break

    #now i can download it and write it to pdf folder
    r = requests.get(href)
    with open(location +"/data/pdf/" + pdf, 'wb') as f:
        f.write(r.content)

    #incremenet patent number
    num += 1

    #bellow will be deleted, this is for testing so it actually stops :)
    if num == 3:
        sys.exit()

