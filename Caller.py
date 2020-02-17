import GetMixedLyrics
import pprint

artist='The Beatles'
#song="Yellow SubMarine"

#list= GetMixedLyrics.get_songs_from_artist_lyrics(artist)
list = GetMixedLyrics.get_all_lyrics_from_an_artist(artist)
print(list)