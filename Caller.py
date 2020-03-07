import GetMixedLyrics
import pprint

artist='The Beatles'
#song="Yellow SubMarine"
#GetMixedLyrics.find_similarity()

#sim= GetMixedLyrics.calculate_similarity()

#list= GetMixedLyrics.get_songs_from_artist_lyrics(artist)
list = GetMixedLyrics.get_all_lyrics_from_an_artist(artist)
print(list)
print(list[0])
print(list[1])
sim= GetMixedLyrics.calculate_similarity(list[0],list[1])
print(sim)