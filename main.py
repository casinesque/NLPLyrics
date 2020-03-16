import GetMixedLyrics
import NLP_Processor

def main():
    #Please type the artist you are looking for without any dash or symbols char. E.g. "The rolling stones", "The beatles"
    artist='The R?olling stone£s'
    listOfLyrics= GetMixedLyrics.get_all_lyrics_from_an_artist(artist)
    NLP_Processor.count_lyrics_word_frequency(listOfLyrics)


if __name__ == "__main__":
    main()