import GetMixedLyrics
import pprint

artist='The Beatles'
#song="Yellow SubMarine"
#GetMixedLyrics.find_similarity()


list = GetMixedLyrics.get_all_lyrics_from_an_artist(artist)
print(list)


'''
a="i want you"
a=''.join(a)
a=a.replace('\r', '')
a=a.replace('\n',' ')
b="i want to tell you"
b=''.join(b)
b=b.replace('\r', '')
b=b.replace('\n', ' ')

sim= GetMixedLyrics.calculate_similarity(a,b)
print(sim)
'''


#sgt pepper's lonely hearts club band
#sgt pepper's lonely hearts club band minidocumentary
#nothin' shakin'
#nothin shaking
#kansas city