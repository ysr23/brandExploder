import sys
import requests
from bs4 import BeautifulSoup
baseURL = 'https://nitro.api.bbci.co.uk/nitro/api/'
pid = str(sys.argv[1]) # No fallbacks, no error handling 
keyFile = open('keys.txt', 'r')
apiKey = str(keyFile.readline().split(':')[1].rstrip()) # No fallbacks, no error handling 
print(apiKey)

def explodeSeries(seriesPid): # explode series into episodes
    seriesUrl = baseURL + 'programmes/?api_key='+ apiKey +'&children_of=' + seriesPid + '&page_size=300'
    res = requests.get(seriesUrl)
    soup = BeautifulSoup(res.content, "lxml")
    results = soup.findAll('results')
    episodes = soup.findAll('episode')
    print(str(len(episodes)) + ' Episodes found')
    for episode in episodes:
        if episode.release_date:
            rd = str(episode.release_date.text)
        else:
            rd = 'N/A'
        if episode.title:
            title = str(episode.title.text)
        else:
            title = 'NO TITLE'
        print(episode.pid.text + ' - ' + title + ' - ' + rd)

def explodeBrand(pid): #explode brand into series
    nitro_url = baseURL + 'programmes/?api_key='+ apiKey +'&children_of=' + pid +'&entity_type=series&page_size=300'
    print(nitro_url)
    res = requests.get(nitro_url)
    soup = BeautifulSoup(res.content, "lxml")
    results = soup.findAll('results')
    seriess = soup.findAll('series')
    print(str(len(seriess)) + ' Series found')
    print(res)
    for series in seriess:
        if series.series_of.has_attr('position'):
            pos = str(series.series_of['position'])
        else:
            pos = 'N/A'
            
        print('-----------------------------')
        print(series.pid.text + ' - ' + series.title.text + ' - Position: ' + pos)
        print('-----------------------------')
        explodeSeries(series.pid.text)
explodeBrand(pid)
    
#explodeSeries('p00gw8y4')
