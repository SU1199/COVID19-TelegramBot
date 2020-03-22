import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import requests
from bs4 import BeautifulSoup

update_id = None
countries = 'China\nItaly\nUSA\nSpain\nGermany\nIran\nFrance\nS. Korea\nSwitzerland\nUK\nNetherlands\nAustria\nBelgium\nNorway\nSweden\nCanada\nDenmark\nAustralia\nPortugal\nMalaysia\nBrazil\nJapan\nCzechia\nTurkey\nIsrael\nIreland\nDiamond Princess\nLuxembourg\nPakistan\nThailand\nChile\nPoland\nEcuador\nGreece\nFinland\nQatar\nIceland\nIndonesia\nSingapore\nSaudi Arabia\nSlovenia\nPhilippines\nRomania\nIndia\nPeru\nBahrain\nRussia\nEstonia\nEgypt\nHong Kong\nMexico\nPanama\nSouth Africa\nLebanon\nArgentina\nIraq\nColombia\nCroatia\nArmenia\nSerbia\nSlovakia\nKuwait\nBulgaria\nSan Marino\nTaiwan\nUAE\nAlgeria\nUruguay\nHungary\nLatvia\nCosta Rica\nDominican Republic\nLithuania\nJordan\nMorocco\nVietnam\nBosnia and Herzegovina\nFaeroe Islands\nAndorra\nNorth Macedonia\nCyprus\nBrunei \nMoldova\nSri Lanka\nAlbania\nBelarus\nMalta\nVenezuela\nNew Zealand\nBurkina Faso\nTunisia\nGuadeloupe\nSenegal\nGeorgia\nKazakhstan\nAzerbaijan\nCambodia\nPalestine\nOman\nTrinidad and Tobago\nUkraine\nRéunion\nUzbekistan\nCameroon\nMartinique\nLiechtenstein\nChannel Islands\nHonduras\nBangladesh\nAfghanistan\nDRC\nParaguay\nNigeria\nCuba\nGhana\nPuerto Rico\nJamaica\nMacao\nBolivia\nGuyana\nMonaco\nFrench Guiana\nGuatemala\nRwanda\nMontenegro\nTogo\nFrench Polynesia\nGuam\nMauritius\nBarbados\nIvory Coast\nKyrgyzstan\nMaldives\nMayotte\nGibraltar\nMongolia\nEthiopia\nAruba\nKenya\nSeychelles\nEquatorial Guinea\nTanzania\nU.S. Virgin Islands\nGabon\nSaint Martin\nSuriname\nBahamas\nNew Caledonia\nEswatini\nCayman Islands\nCuraçao\nCabo Verde\nCAR\nCongo\nEl Salvador\nLiberia\nMadagascar\nNamibia\nSt. Barth\nZimbabwe\nSudan\nAngola\nBenin\nBermuda\nBhutan\nFiji\nGreenland\nGuinea\nHaiti\nIsle of Man\nMauritania\nNicaragua\nSaint Lucia\nZambia\nNepal\nAntigua and Barbuda\nChad\nDjibouti\nEritrea\nGambia\nVatican City\nMontserrat\nNiger\nPapua New Guinea\nSt. Vincent Grenadines\nSint Maarten\nSomalia\nTimor-Leste\nUganda'
instructions = "Enter 'info' to get summary of the world.\nEnter 'country <country name>' for Country-Wise Info.\nEnter 'list' to get list of available countries."
def main():
    global update_id
    bot = telegram.Bot('TOKEN')

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1


def echo(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:
            if update.message.text.lower() == "info":
                update.message.reply_text(info())
            elif update.message.text.lower().split(" ",1)[0] == "country":
                update.message.reply_text(data(update.message.text.split(" ",1)[1]))
            elif update.message.text.lower() == "list":
                update.message.reply_text(countries)
            else:
                update.message.reply_text(instructions)

def data(country):
    i = 0
    page = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table')
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        if i > 0:
            if td[0].text.lower() == country.lower():
                return td[0].text.strip() + " has " + td[1].text.strip() + ' total cases, ' + td[2].text.strip() + ' new cases, ' + td[3].text.strip() + ' total deaths, ' + td[4].text.strip() + ' new death(s), ' + td[5].text.strip() + ' total recoverd, ' + td[6].text.strip() + ' active cases, ' + td[7].text.strip() + ' serious critical cases.'
        elif i >= len(table_rows)+1:
            return "Invalid Country"
        i =i+1

def info():
    page = requests.get("https://www.worldometers.info/coronavirus/coronavirus-cases/")
    soup = BeautifulSoup(page.content, 'html.parser')
    i = soup.find_all('p')[0].get_text()
    return i


if __name__ == '__main__':
    main()
