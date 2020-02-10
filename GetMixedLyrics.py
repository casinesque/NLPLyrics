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

def get_songs_from_artist_lyrics(artist):
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