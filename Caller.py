import GetMixedLyrics
import NLP_Processor

artist='The Beatles'
#song="Yellow SubMarine"
#GetMixedLyrics.find_similarity()


list =GetMixedLyrics.get_all_lyrics_from_an_artist(artist)

NLP_Processor.count_lyrics_word_frequency(list)

