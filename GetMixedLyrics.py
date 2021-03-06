import re
import urllib.request
import requests
from bs4 import BeautifulSoup
import time
import editdistance
import spacy
import en_core_web_md
from pprint import pprint
# gestione proxy vedere qui --> https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
#o qui --> https://blog.scrapinghub.com/python-requests-proxy
# per user agent ---> https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
proxies = {
    #FUNZIONANTI
    "http":  'http://89.32.227.230:8080',
    "https": 'http://89.32.227.230:8080',
    #DA RIVEDERE
    "http":  'http://80.241.222.137:80',
    "https":  'http://80.241.222.137:80',
    #"http": 'http://80.232.126.94:80',
    #"https": 'http://80.232.126.94:80',
    #"https": 'https://163.172.136.226:8811',
    #"http": 'https://163.172.136.226:8811',
    #"http":  'http://178.128.28.166:8080',
    #"https":  'http://178.128.28.166:8080',
    # da rivedere ancora
    #"http": 'http://209.50.52.162:9050',
    #"https": 'http://209.50.52.162:9050'
}

MINIMUM_EDIT_DITANCE_TRESHOLD = 1

nlp = en_core_web_md.load()


def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)


def calculate_similarity(text1, text2):
    base = nlp(process_text(text1))
    compare = nlp(process_text(text2))
    return base.similarity(compare)




def remove_html_tags(text):
    """Remove html tags from a string"""
    """So the idea is to build a regular expression which can find all the characters “< >” in the first incidence in a text, 
    and after that using sub function replace all the text between those symbols with an empty string."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', str(text))


def remove_parenthesis(text):
    cleanedFromSquare = re.sub(r'\[.*?\]', "", text)  # RIMUOVO PARENTESI [
    cleandedFromRound = re.sub(r'\(.*?\)', "", cleanedFromSquare)  # RIMUOVO PARENTESI (
    return cleandedFromRound

def leaveOnlyAlphabeticalChars(text):
    #[^a-zA-Z]
    clean = re.compile('[^a-zA-Z]')
    return re.sub(clean,'',str(text))


''' # RIMUOVE I DUPLICATI -------------- UTILE DA TENERE.
def remove_duplicate(items):
    unique = []
    names=[]
    urls=[]
    for item in items:
        name=item[0]
        url=item[1]
        if name not in names:
            names.append(name)
            urls.append(url)
    unique = [val for pair in zip(names, urls) for val in pair]
    # RITORNO LA LISTA DI TUTTE LE CANZONI SINGOLE ! NO MORE DUPLICATES! DA QUIIIIIIIIIIIIIIIIIIIII
    return unique
'''
'''def calculate_minimum_edit_distance(words):
    mapOfSongs = {}
    for word in words[::2]:
        index=words.index(word)
        mapOfSongs[word]=words[index+1]
        #if editdistance.eval(words[index],word[index+2]) <= 2:
         # print("ciao")
     return mapOfSongs
'''
def remove_duplicates_by_dict(words):
    mapNameUrl = {}
    unique = []
    mapNameUrl = dict(zip(words[::2], words[1::2]))
    unique= mapNameUrl.items()
    unique=[[i,j] for i,j in unique] #trasformo lista di tuple in lista
    flattened_unique_list=[]
    list_of_similar=[]
    for sublist in unique: # list flattening !
        for element in sublist:
            flattened_unique_list.append(element)
            #CONTROLLO LA MED. SOLO CON TRESHOLD A 1 SONO SICURO DI NON TOGLIERE CANZONI BUONE.
    for left, right in zip(flattened_unique_list[:-2],flattened_unique_list[2:]):
        if editdistance.eval(left,right)<= MINIMUM_EDIT_DITANCE_TRESHOLD or left in right: # rimuovo tutte quelle sporche o che hanno nomi allungati della stessa canzone
                list_of_similar.append(right) # empiricamente i dx sono quelli piu corretti, quindi cancello quelli a sx.
    for key in list(mapNameUrl.keys()):
        if key in list_of_similar:
            try:
                del mapNameUrl[key]
            except KeyError:
                print("Key  not found")
    cleanedList=mapNameUrl.items()
    unique = [[i, j] for i, j in cleanedList] # ritorno la lista in uscita pulita !
    return unique


def get_songs_from_artist_lyrics(artist):
    artist = artist.lower()
    # remove all except alphanumeric characters from artist and song_title
    #artist = re.sub('[^A-Za-z0-9]+', "", artist)
    if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist.replace(" ","-").strip()
    url = "https://www.lyrics.com/artist.php?name="+artist+"&o=1"

    try:
        #content = requests.get(url,proxies=proxies).text
        #TODO: sistemare questi maledetti proxies. Per ora uso la versione senza.
        content = requests.get(url).text
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
            name = re.sub(r'\(.*?\)', "", name)  # RIMUOVO PARENTESI (
            name = name.split('[')[0] # RIMUOVO PARENTESI (
            name = name.split('(')[0] # RIMUOVO PARENTESI (
            name = name.strip()
            name = name.replace('and', '') #RIMUOVO PAROLE  NEI TITOLI PIU COMUNI
            if name not in finalNameList:
                url=(str(htmlRowUrl[0])).split('"')[1] # ricavo link per ogni canzone
                url = "https://www.lyrics.com/"+url
                finalNameList.append(leaveOnlyAlphabeticalChars(name))
                #ORA HO UNA LISTA COI NOMI UGUALI A CUI HO RIMOSSO COMPLETAMENTE LA PUNTEGGIATURA. UTILE PER CHIAMARCI UN DICT. SOPRA E RIMUOVERE DUPLICATI.
                finalUrlList.append(url)
        finalList = [val for pair in zip(finalNameList, finalUrlList) for val in pair]
        all_separated_final_list = [list(x) for x in zip(finalList[::2], finalList[1::2])]  # Ho creato una lista di liste [[[]]
        print(finalList)
        finalList = remove_duplicates_by_dict(finalList) #ECCO QUA CHE HO CREATO IL DIZIONARIO SENZA USARE LA FUNZIONE APPOSITA!
        print(finalList)
        return finalList

    except Exception as e:
        return "Exception occurred \n" + str(e)



def get_all_lyrics_from_an_artist(artist):
    artist = artist.lower()
    all_songs= get_songs_from_artist_lyrics(artist)
    #Lista dove ogni elemento è [nome canzone, url] -- CONTIENE DUPLICATI E SIMILTUDINI.
    #all_separated_songs=[list(x) for x in zip(all_songs[::2], all_songs[1::2])] # creo una lista di sottoliste [[nome,url]...]
    list_of_words=[]
    for item in all_songs:
        url_lyric = (item[1])
        time.sleep(0.5)
        content = requests.get(url_lyric).text
        soup = BeautifulSoup(content, 'html.parser')
        # listOfSongs=soup.findAll("div"),{"class":"tdata-ext"}
        # listOfSongs=soup.find('td', attrs={'class':'tdata'})
        body_lyrics=soup.find('pre', attrs={'id': 'lyric-body-text'})
        noHtmlCleanedText=remove_html_tags(body_lyrics) # rimuovo html dal content
        cleaned_text=remove_parenthesis(noHtmlCleanedText) # rimuovo parentesi dai testi
        print ("Sto scaricando il titolo di:" + remove_parenthesis(item[0]))
        list_of_words.append(cleaned_text) # Ecco qua il testo di una singola canzone
    return list_of_words # lista di tutte le parole. Problema, ci sono duplicati. # DA QUIIIIIIIIIII






























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