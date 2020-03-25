import re
import urllib.request
import requests
from bs4 import BeautifulSoup, SoupStrainer
import time
import editdistance
import spacy
import en_core_web_md
import lxml
from difflib import SequenceMatcher

# gestione proxy vedere qui --> https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
# o qui --> https://blog.scrapinghub.com/python-requests-proxy
# per user agent ---> https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
proxies = {
    # FUNZIONANTI
    "http": 'http://89.32.227.230:8080',
    "https": 'http://89.32.227.230:8080',
    # DA RIVEDERE
    "http": 'http://80.241.222.137:80',
    "https": 'http://80.241.222.137:80',
    # "http": 'http://80.232.126.94:80',
    # "https": 'http://80.232.126.94:80',
    # "https": 'https://163.172.136.226:8811',
    # "http": 'https://163.172.136.226:8811',
    # "http":  'http://178.128.28.166:8080',
    # "https":  'http://178.128.28.166:8080',
    # da rivedere ancora
    # "http": 'http://209.50.52.162:9050',
    # "https": 'http://209.50.52.162:9050'
}

MINIMUM_EDIT_DISTANCE_THRESHOLD = 1

MAX_SIMILARITY_TRESHOLD = 0.80

nlp = en_core_web_md.load()
'''
def remove_invalid_chars(input_string):
    invalidChars="&"
    if invalidChars in input_string:
        clean = re.compile('(& amp; | &)')
    return re.sub(clean, '', str(input_string))
'''
def remove_invalid_chars(input_string):
    invalidChars="&"
    input_string = input_string.replace('&', "and")
    return input_string


def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:  # e.g. 'come and get it' and 'come together' were reduced to just 'come'. Not enough information. Commented.
        # if token.text in nlp.Defaults.stop_words:
        #    continue
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
    clean = re.compile('[,\.!\?-]')
    return re.sub(clean, '', str(text))


def removeSpaces(text):
    clean = re.compile('[^a-zA-Z]')
    return re.sub(clean, '', str(text))


def remove_duplicates_by_dict(words):
    mapNameUrl = {}
    unique = []
    mapNameUrl = dict(zip(words[::2], words[1::2]))
    unique = mapNameUrl.items()
    unique = [[i, j] for i, j in unique]  # Trasforming list of tuples in a list
    flattened_unique_list = []
    list_of_similar = []
    for sublist in unique:  # list flattening !
        for element in sublist:
            flattened_unique_list.append(element)
    for left, right in zip(flattened_unique_list[:-2], flattened_unique_list[2:]):
        #if calculate_similarity(left, right) > 0.95 or editdistance.eval(left,right) <= MINIMUM_EDIT_DISTANCE_THRESHOLD or removeSpaces(right) in removeSpaces(left) or removeSpaces(left) in removeSpaces(right):  # REMOVING ALL THE NOISE NAMES OR WITH NON STANDARD NAMES, OR REPLICATED NAMES
            if not left.startswith("https:"):
                if SequenceMatcher(None, left, right).ratio() > MAX_SIMILARITY_TRESHOLD:
                    longer = left if len(left) > len(right) else right
                    '''Empirically those on the right side are the more correct so i'm deleting the left values'''
                    list_of_similar.append(longer)
    for key in list(mapNameUrl.keys()):
        if key in list_of_similar:
            try:
                del mapNameUrl[key]
            except KeyError:
                print("Key  not found")

    cleanedList = mapNameUrl.items()
    unique = [[i, j] for i, j in cleanedList]  # returning the clean list
    return unique


def get_songs_from_artist_lyrics(artist):
    artist = artist.lower()
    # remove all except alphanumeric characters from artist
    artist = re.sub('[^a-zA-Z\d\s:]', "", artist)
    if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist.replace(" ", "-").strip()
    url = "https://www.lyrics.com/artist.php?name=" + artist + "&o=1"

    try:
        content = requests.get(url).text
        only_tdata_tags = SoupStrainer('table', {'class': 'tdata'})
        soup = BeautifulSoup(content, 'lxml',
                             parse_only=only_tdata_tags)  # BS + SoupStrainer allows to parse only the requested class. Improve speed and linearity.
        finalList = []
        finalNameList = []
        finalUrlList = []
        for row in soup.select('tbody tr'):
            htmlRow = row.find_all('td')
            htmlRowUrl = row.find_all('a')
            name = [ele.text.strip() for ele in htmlRow][0] #from each row, we get the song name.
            name = name.lower()
            name = re.sub(r'\[.*?\]', "", name)  # RIMUOVO PARENTESI [
            name = re.sub(r'\(.*?\)', "", name)  # RIMUOVO PARENTESI (
            name = re.sub(r'\{.*?\}', "", name)  # RIMUOVO PARENTESI (
            name = name.split('[')[0]  # RIMUOVO PARENTESI (
            name = name.split('(')[0]  # RIMUOVO PARENTESI (
            name = name.strip()
            name= name.replace("‘", '').replace("’", '').replace("'", '')
            name= name.replace('"', '').replace('/"',"")
            name= remove_invalid_chars(name)
            if name not in finalNameList:
                url = (str(htmlRowUrl[0])).split('"')[1]  # gathering url for each correct song
                url = "https://www.lyrics.com" + url
                finalNameList.append(leaveOnlyAlphabeticalChars(name))
                finalUrlList.append(url)
        finalList = [val for pair in zip(finalNameList, finalUrlList) for val in pair]
        all_separated_final_list = [list(x) for x in
                                    zip(finalList[::2], finalList[1::2])]  # Ho creato una lista di liste [[[]]
        #Now we have a whole list with some equals name. We call a method which works using dict in order to automatically remove duplicates
        finalList = remove_duplicates_by_dict(finalList)
        if finalList:
            return finalList
        else:
            raise Exception('No results for this artist. Please check your input and retry.')
    except Exception as e:
        return "Exception occurred \n" + str(e)


def get_all_lyrics_from_an_artist(artist):
    artist = artist.lower()
    all_songs = get_songs_from_artist_lyrics(artist)
    list_of_words = []
    #At this point i have a list with [[name,url][name,url]]. We simply gather each lyrics from each song simply parsing the url associated.
    for item in all_songs:
        url_lyric = (item[1])
        # time.sleep(0.5) OPTIONAL: If fastness is not a priority and we query lots of data. This slow down the request made to the lyrics.com
        content = requests.get(url_lyric).text
        only_pre_tag = SoupStrainer('pre', {
            'id': 'lyric-body-text'})  # Allows to parse just this css id instead of the whole webpage. 1.5x faster
        soup = BeautifulSoup(content, 'lxml', parse_only=only_pre_tag)
        noHtmlCleanedText = remove_html_tags(str(soup))  # removing all html tags
        cleaned_text = remove_parenthesis(noHtmlCleanedText)  # removing noises characters
        print("Downloading lyric of:" + remove_parenthesis(item[0]))
        list_of_words.append(cleaned_text.replace('\n', ' ').replace('\r', ''))
    return list_of_words  # Huge list with all the words in it.

