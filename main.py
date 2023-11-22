from bs4 import BeautifulSoup
import requests
import time

countPages=0
eventsOnPage=21
currentPage=0



html=requests.get("https://www.ostravainfo.cz/cz/akce/").text
soup=BeautifulSoup(html,'html.parser')

for page in soup.find_all(class_="list-pagination__item__in"):
    countPages+=1
countPages-=1

def getData(currentPage=0,countPages=countPages): 
    start_time=time.time()
    countLinks=1
    print('[INFO] I\'m collecting data. Please wait...')
    with open('whereToGo.txt','w',encoding='utf-8') as file:
        while currentPage<countPages:
            html=requests.get(f"https://www.ostravainfo.cz/cz/akce/?from={eventsOnPage*currentPage}").text
            soup=BeautifulSoup(html,'html.parser')
            for link in soup.find_all('a',class_="js-simulate-link-target"):
                html=requests.get(link.get('href')).text
                soup=BeautifulSoup(html,'html.parser')
                divName=soup.find('div',class_='akce-detail')
                name=divName.find('h2').string
                divPrices=soup.find_all('div',class_='odsadit')
                date=soup.find('ul', class_='akce-info').find('li').text
                if len(divPrices)==3:
                    p=divPrices[0].find_all('p')
                    if len(p)+1>=3:
                        price=p[1]
                        print(f'{name} : {price.text} | {date}')
                        file.write(f'{countLinks}) {name} || {price.text} || {date} || {link.get('href')}\n')
                    else:
                        print(f'{name} : Free | {date}')
                        file.write(f'{countLinks}) {name} || Free || {date} || {link.get('href')}\n')
                else:
                    print(f'{name} : Free | {date}')
                    file.write(f'{countLinks}) {name} || Free || {date} || {link.get('href')}\n')
                countLinks+=1

            currentPage+=1
            file.write('\n\n')
            print("\n\n")
    end_time=time.time()
    execution_time = end_time - start_time
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    print(f'[INFO] The file was successfully created and the data was successfully written.\nAds processed: {countLinks-1} for {minutes} minutes {seconds} seconds.')

getData()
