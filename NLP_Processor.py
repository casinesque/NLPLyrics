import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
import WordCloud_Processor

lemmatizer = WordNetLemmatizer()

#IN ORDER TO IMPROVE THE LEMMITAZATION WE DEFINE A DICT FOR POS TAGGING.
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    #tag = nltk.pos_tag([word])[0][1][0].upper()
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN) #return the tag or NOUN if key doesn't exists.



def count_lyrics_word_frequency(list,N):
    tokens=[]
    for item in list:
        tokens.append(word_tokenize(item.lower())) #tokenization
    for token in tokens: #list of list iteration
        for segment in token: # token in each list iteration
            # pulizia stopwords
            if segment in stopwords.words('english') or segment in string.punctuation:
                token.remove(segment)                 # removing that word from the token list of a single song
    lemma_tokens = []
    for list in tokens:  #Additional list with lemmatized tokens
        for word in list:
            lemma_tokens.append(lemmatizer.lemmatize(word, get_wordnet_pos(word)))
    punct= "[!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]:"
    freq = nltk.FreqDist()
    for word in lemma_tokens: #manually creates the dict, we only considering strings longer than 4 chars.
        if len(word) >= 4 and word not in punct:
            freq[word] +=1
    print(freq.keys()) #print the map of words and relative frequency
    for key in freq:
        print(key, ': ', freq[key])
    freq.plot(50, cumulative=False) #plot the first 50 most common words