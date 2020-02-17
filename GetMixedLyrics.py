import re
import urllib.request
import requests
from bs4 import BeautifulSoup
import time
from pprint import pprint
# gestione proxy vedere qui --> https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
#o qui --> https://blog.scrapinghub.com/python-requests-proxy
# per user agent ---> https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
proxies = {
    "http":  'http://89.32.227.230:8080',
    "https":  'http://89.32.227.230:8080',
    "http":  'http://80.241.222.137:80',
    "https":  'http://80.241.222.137:80',
    "http": 'http://80.232.126.94:80',
    "https": 'http://80.232.126.94:80',
    "https": 'https://163.172.136.226:8811',
    "http": 'https://163.172.136.226:8811',
    "http":  'http://178.128.28.166:8080',
    "https":  'http://178.128.28.166:8080',
    #"http": 'http://209.50.52.162:9050',
    #"https": 'http://209.50.52.162:9050'
}
def remove_html_tags(text):
    """Remove html tags from a string"""
    """So the idea is to build a regular expression which can find all the characters “< >” in the first incidence in a text, 
    and after that using sub function replace all the text between those symbols with an empty string."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', str(text))

def get_songs_from_artist_lyrics(artist):
    artist = artist.lower()
    # remove all except alphanumeric characters from artist and song_title
    #artist = re.sub('[^A-Za-z0-9]+', "", artist)
    if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist.replace(" ","-").strip()
    url = "https://www.lyrics.com/artist.php?name="+artist+"&o=1"

    try:
        #content = urllib.request.urlopen(url).read()
        content = requests.get(url,proxies=proxies).text
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        #listOfSongs=soup.findAll("div"),{"class":"tdata-ext"}
        #listOfSongs=soup.find('td', attrs={'class':'tdata'})
        table = soup.find('table', attrs={'class': 'tdata'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        listOfSongs=[]
        finalList=[]
        finalNameList=[]
        finalUrlList=[]
        for row in rows:
            htmlRow = row.find_all('td')
            htmlRowUrl = row.find_all('a')
            name=[ele.text.strip() for ele in htmlRow][0]
            name = name.lower()
            name = re.sub(r'\[.*?\]', "", name)  # RIMUOVO PARENTESI [
            name = re.sub(r'\[.*?\]', "", name)  # RIMUOVO PARENTESI [
            name = re.sub(r'\[.*? ', "", name)  # RIMUOVO PARENTESI (
            name = name.split('[')[0] # RIMUOVO PARENTESI (
            name = name.split('(')[0] # RIMUOVO PARENTESI (
            name = name.strip()
            if name not in finalNameList:
                url=(str(htmlRowUrl[0])).split('"')[1] # ricavo link per ogni canzone
                url = "https://www.lyrics.com/"+url
                finalNameList.append(name)
                finalUrlList.append(url)
        finalList = [val for pair in zip(finalNameList, finalUrlList) for val in pair]
        return finalList
    except Exception as e:
        return "Exception occurred \n" + str(e)



        # lyrics lies between up_partition and down_partition
        #up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        #down_partition = '<!-- MxM banner -->'
        #lyrics = lyrics.split(up_partition)[1]
        #lyrics = lyrics.split(down_partition)[0]
        #lyrics=remove_html_tags(lyrics)
        #cListOfSongs=[]
        #Removing version such as [DVD],[STUDIO VERSION], [LIVE AT]


    '''
        for element in listOfSongs:
            element[0]=(element[0].lower())
            element[0]=re.sub(r'\[.*?\]', "", element[0]) #RIMUOVO PARENTESI [
            element[0]=re.sub(r'\(.*?\)', "", element[0]) #RIMUOVO PARENTESI (
            element[0]=element[0].strip()
        return listOfSongs #Lista di titoli unici
    '''

def get_all_lyrics_from_an_artist(artist):
    artist = artist.lower()
    all_songs= get_songs_from_artist_lyrics(artist)
    all_separated_songs=[list(x) for x in zip(all_songs[::2], all_songs[1::2])] # creo una lista di sottoliste [[nome,url]...]
    list_of_words=[]
    for item in all_separated_songs:
        url_lyric = (item[1])
        time.sleep(0.5)
        content = requests.get(url_lyric).text
        soup = BeautifulSoup(content, 'html.parser')
        # listOfSongs=soup.findAll("div"),{"class":"tdata-ext"}
        # listOfSongs=soup.find('td', attrs={'class':'tdata'})
        body_lyrics=soup.find('pre', attrs={'id': 'lyric-body-text'})
        cleaned_text=remove_html_tags(body_lyrics)
        print ("Sto scaricando il titolo di:" + item[0])
        list_of_words.append(cleaned_text) # Ecco qua il testo di una singola canzone
    return list_of_words # lista di tutte le parole. Problema, ci sono duplicati.



def get_lyric_by_artist(artist, song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "https: // www.metrolyrics.com /" + artist + "-"+"lyrics"+ ".html"

    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics=remove_html_tags(lyrics)
        return lyrics
    except Exception as e:
        return "Exception occurred \n" + str(e)