import re
import urllib.request
from bs4 import BeautifulSoup
from pprint import pprint

def remove_html_tags(text):
    """Remove html tags from a string"""
    """So the idea is to build a regular expression which can find all the characters “< >” in the first incidence in a text, 
    and after that using sub function replace all the text between those symbols with an empty string."""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_songs_from_artist_songlyrics(artist):
    artist = artist.lower()
    # remove all except alphanumeric characters from artist and song_title
    #artist = re.sub('[^A-Za-z0-9]+', "", artist)
    if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist.replace(" ","-").strip()
    url = "https://www.lyrics.com/artist.php?name="+artist+"&o=1"

    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        #listOfSongs=soup.findAll("div"),{"class":"tdata-ext"}
        #listOfSongs=soup.find('td', attrs={'class':'tdata'})
        table = soup.find('table', attrs={'class': 'tdata'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        listOfSongs=[]
        listOfUrls=[]
        for row in rows:
            cols = row.find_all('td')
            urls = row.find_all('a')
            url=(str(urls[0])).split('"')[1] # ricavo link per ogni canzone
            cols=[ele.text.strip() for ele in cols]
            #urls= [ele.text.strip() for ele in urls]
            url="https://www.lyrics.com/"+url
            songAndLink=[cols[0],url]
            #listOfSongs.append(cols[0])
            listOfSongs.append(songAndLink)
        pprint(listOfSongs) ##########################LISTONE CON NOMI E LINK.
        #print(listOfUrls)
        #print(cleanAndUniqueUrlList)


        ###################DA QUI, TAGLIARE I LINK NELLA PARTE FINALE PER TOGLIERE I DOPPIONI.
        ################### POI FARE FUNZIONE PER OTTENERE IL TESTO DA CIASCUNA API.



        # lyrics lies between up_partition and down_partition
        #up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        #down_partition = '<!-- MxM banner -->'
        #lyrics = lyrics.split(up_partition)[1]
        #lyrics = lyrics.split(down_partition)[0]
        #lyrics=remove_html_tags(lyrics)
        cListOfSongs=[]
        for element in listOfSongs:
            element=element.lower().strip()
            element=re.sub(r'\[.*?\]',"", element) #RIMUOVO PARENTESI [
            element=re.sub(r'\(.*?\)', "", element) #RIMUOVO PARENTESI (
            cListOfSongs.append(element.strip())
        cleanAndUniqueSongsList=list(dict.fromkeys(cListOfSongs))
        return cleanAndUniqueSongsList #Lista di titoli unici
    except Exception as e:
        return "Exception occurred \n" + str(e)


def get_lyrics_(artist, song_title):
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