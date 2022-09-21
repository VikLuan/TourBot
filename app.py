
import telebot
from urllib import request
from flask import Flask
from flask import send_from_directory, request
import requests
from bs4 import BeautifulSoup
import wikipedia
import googlemaps

API_TOKEN = '5483608488:AAHTv_dchI4Nprr5KMEA1GbG9mYNHNCLS8A'

API_KEY = 'AIzaSyBRtO0nXXLZo9wkZg6Z125dI3sfOdUpNhw'

# url lista luoghi generici
URL_GENERIC_PLACES = "https://www.charmingpuglia.com/it/10-posti-da-visitare-in-puglia"
# url lista castelli
URL_CASTLE_LIST = "https://www.alpitour.it/racconti/10-castelli-da-visitare-in-puglia"
# url lista parchi naturali
URL_PARK_LIST = "https://www.alpitour.it/racconti/i-10-parchi-naturali-piu-belli-della-puglia"
#url lista spiagge
URL_BEACH_LIST = "https://www.alpitour.it/racconti/le-10-spiagge-piu-belle-della-puglia"
#url lista paesi
URL_CITY_LIST = "https://www.travel365.it/borghi-puglia.htm"
#url lista monumenti
URL_MONUMENT_LIST = "https://www.visititaly.it/monumenti/puglia.aspx"
#url lista chiese
URL_CHURCH_LIST = "https://www.puglianelmondo.com/go/196/chiese-e-cattedrali.aspx"

wikipedia.set_lang("it")

bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

gmaps = googlemaps.Client(key=API_KEY)

def road_info(city1, city2):
    fulfillment = ""
    my_dist = gmaps.distance_matrix(city1, city2)['rows'][0]['elements'][0]
    km = "I due punti d'interesse distano " + my_dist.get("distance").get("text") + "\n" + "La durata prevista del viaggio è " + my_dist.get("duration").get("text")
    fulfillment = str(km)
    return fulfillment

def pass_specific_info_about_something(something):
    fulfillmentText = ""
    text = str(wikipedia.summary(something))
    print(text)
    if ("Puglia" in text) or ("Foggia" in text) or ("Barletta" in text) or \
            ("Andria" in text) or ("Trani" in text) or ("Bari" in text) or \
            ("Taranto" in text) or ("Brindisi" in text) or ("Lecce" in text):
        fulfillmentText = text
    else :
        fulfillmentText = "Tale luogo non si trova in Puglia"
    if fulfillmentText:
        return fulfillmentText

def parsing_html(url):
    response = requests.get(url=url)
    response_html = response.text
    return BeautifulSoup(response_html, 'html.parser')

def castle_list_scraping(url):
    fulfillmentText = ""
    soup = parsing_html(url)
    castle_list = []
    for name in soup.findAll('a'):
        castles = name.text
        while("\n" in castles):
            castles = castles[:-1]
        castle_list.append(castles);
    for castle in castle_list:
        fulfillmentText += str(castle) + "\n"
    return fulfillmentText

def beach_list_scraping(url):
    fulfillmentText = ""
    soup = parsing_html(url)
    beach_list = []
    for name in soup.findAll('div', class_="ArticleParagraphsComponent_heading__3508n"):
        beaches = name.text + "\n"
        beach_list.append(beaches);
    for beach in beach_list:
        fulfillmentText += str(beach)
    return fulfillmentText

def park_list_scraping(url):
    fulfillmentText = ""
    soup = parsing_html(url)
    park_list = []
    for name in soup.findAll('div', class_="ArticleParagraphsComponent_heading__3508n"):
        parks = name.text + "\n"
        park_list.append(parks);
    for park in park_list:
        fulfillmentText += str(park)
    return fulfillmentText

def city_list_scraping(url):
    fulfillmentText = ""
    soup = parsing_html(url)
    city_list = []
    for name in soup.findAll('li', class_="index_ol_li"):
        cities = name.text + "\n"
        city_list.append(cities);
    for city in city_list:
        fulfillmentText += str(city)
    return fulfillmentText

def monument_list_scraping(url):
    fulfillmentText = ""
    soup = parsing_html(url)
    monument_list = []
    for name in soup.findAll('h3', class_="NomePoi22"):
        monuments = name.text + "\n"
        monument_list.append(monuments);
    for monument in monument_list:
        fulfillmentText += str(monument)
    return fulfillmentText

def church_list_scraping(url):
    fulfillmentText = ""
    soup = parsing_html(url)
    church_list = []
    for name in soup.findAll('a'):
        if ("Cattedrale" in name.text) or ("Santuario" in name.text) or \
                ("Convento" in name.text) or ("Basilica" in name.text) or \
                ("Duomo" in name.text) or ("Abbazia" in name.text) or ("Santurio" in name.text):
            churches = name.text + "\n"
            church_list.append(churches);
    for church in church_list:
        fulfillmentText += str(church)
    return fulfillmentText

def generic_places_scraping(url):
    fulfillmentText = ""
    soup = parsing_html(url)
    name_list = []
    for name in soup.find_all("h2"):
        names = name.text
        names = names[3:]
        if names[:1] == " ":
            names = names[1:]
        name_list.append(names)
    i = 0
    while i < 15:
        fulfillmentText += str(name_list[i]) + "\n"
        i = i + 1
    return fulfillmentText

@app.route('/webhook', methods=['POST'])
def webhook():
    fulfillmentText = ""
    req = request.get_json(force = True)
    print(req)
    if (req.get("queryResult").get("intent").get("displayName") == "Get Road Info"):
        city_list = req.get("queryResult").get("parameters").get("geo-city")
        city1 = str(city_list[0])
        city2 = str(city_list[1])
        print(city1)
        print(city2)
        fulfillmentText = road_info(city1, city2)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get Lista Generica"):
        fulfillmentText = generic_places_scraping(URL_GENERIC_PLACES)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get List Of Castles"):
        fulfillmentText = castle_list_scraping(URL_CASTLE_LIST)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get List Of Parks"):
        fulfillmentText = park_list_scraping(URL_PARK_LIST)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get List Of Beaches"):
        fulfillmentText = beach_list_scraping(URL_BEACH_LIST)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get List Of Cities"):
        fulfillmentText = city_list_scraping(URL_CITY_LIST)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get List Of Monuments"):
        fulfillmentText = monument_list_scraping(URL_MONUMENT_LIST)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get List Of Churches"):
        fulfillmentText = church_list_scraping(URL_CHURCH_LIST)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get Info About City"):
        city = req.get("queryResult").get("parameters").get("geo-city")
        fulfillmentText = pass_specific_info_about_something(city)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get Info About Monument"):
        monument = req.get("queryResult").get("parameters").get("place-attraction")
        fulfillmentText = pass_specific_info_about_something(monument)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get Info About Park"):
        park = req.get("queryResult").get("parameters").get("place-attraction")
        fulfillmentText = pass_specific_info_about_something(park)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get Info About Church"):
        church = req.get("queryResult").get("parameters").get("place-attraction")
        fulfillmentText = pass_specific_info_about_something(church)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get Info About Beach"):
        city = req.get("queryResult").get("parameters").get("geo-city")
        beach = req.get("queryResult").get("parameters").get("place-attraction")
        if city:
            fulfillmentText = "Non ho dati sufficienti a proposito della spiaggia ma eccone alcuni su " + str(city) + ":\n"
            fulfillmentText += pass_specific_info_about_something(city)
        elif beach:
            fulfillmentText = pass_specific_info_about_something(beach)
        print(str(fulfillmentText))
    if (req.get("queryResult").get("intent").get("displayName") == "Get Info About Castle"):
        city = req.get("queryResult").get("parameters").get("geo-city")
        castle = req.get("queryResult").get("parameters").get("place-attraction")
        if city:
            fulfillmentText = "Non ho abbastanza informazioni riguardanti il castello ma eccone alcune su " + str(city) + ":\n"
            fulfillmentText += pass_specific_info_about_something(city)
        elif castle:
            fulfillmentText = pass_specific_info_about_something(castle)
        print(str(fulfillmentText))
    return {
        'fulfillmentText': fulfillmentText
    }

if __name__ == "__main__":
    app.debug = True
    app.run()