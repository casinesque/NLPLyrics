import GetMixedLyrics
import pprint

artist='The Beatles'
#song="Yellow SubMarine"

list= GetMixedLyrics.get_songs_from_artist_songlyrics(artist)
print(list)