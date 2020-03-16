import GetMixedLyrics
import NLP_Processor

artist='The Rolling stones'

list =GetMixedLyrics.get_all_lyrics_from_an_artist(artist)

NLP_Processor.count_lyrics_word_frequency(list)

