import GetMixedLyrics
import pprint

artist='The Beatles'
#song="Yellow SubMarine"
#GetMixedLyrics.find_similarity()


list = GetMixedLyrics.get_all_lyrics_from_an_artist(artist)
print(list)

'''
a="Hey Jude, don't make it bad\r\nTake a sad song and make it better\r\nRemember to let her into your heart\r\nThen you can start to make it better\r\n\r\nHey Jude, don't be afraid\r\nYou were made to go out and get her\r\nThe minute you let her under your skin\r\nThen you begin to make it better\r\n\r\nAnd anytime you feel the pain\r\nHey Jude, refrain\r\nDon't carry the world upon your shoulders\r\nFor well you know that it's a fool\r\nWho plays it cool\r\nBy making his world a little colder\r\nNa-na-na, na, na\r\nNa-na-na, na\r\n\r\nHey Jude, don't let me down\r\nYou have found her, now go and get her \r\nRemember to let her into your heart \r\nThen you can start to make it better\r\n\r\nSo let it out and let it in\r\nHey Jude, begin\r\nYou're waiting for someone to perform with\r\nAnd don't you know that it's just you\r\nHey Jude, you'll do\r\nThe movement you need is on your shoulder\r\nNa-na-na, na, na\r\nNa-na-na, na, yeah\r\n\r\nHey Jude, don't make it bad\r\nTake a sad song and make it better\r\nRemember to let her under your skin\r\nThen you'll begin to make it better\r\nBetter better better better better, ah!\r\n\r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude \r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude \r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude \r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude \r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude \r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude \r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude \r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude \r\nNa, na, na, na-na-na na \r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude\r\nNa, na, na, na-na-na na\r\nNa-na-na na, hey Jude"
print(type(a))
a=''.join(a)
a=a.replace('\r', '')
a=a.replace('\n',' ')
b="In the town where I was born\r\nLived a man who sailed to sea\r\nAnd he told us of his life\r\nIn the land of submarines\r\nSo we sailed up to the sun\r\nTill we found a sea of green\r\nAnd we lived beneath the waves\r\nIn our yellow submarine\r\n\r\nWe all live in a yellow submarine\r\nYellow submarine, yellow submarine\r\nWe all live in a yellow submarine\r\nYellow submarine, yellow submarine\r\n\r\nAnd our friends are all aboard\r\nMany more of them live next door\r\nAnd the band begins to play\r\n\r\nWe all live in a yellow submarine\r\nYellow submarine, yellow submarine\r\nWe all live in a yellow submarine\r\nYellow submarine, yellow submarine\r\n\r\n(Full speed ahead Mr. Boatswain, full speed ahead\r\nFull speed ahead it is, Sergeant\r\nCut the cable, drop the cable\r\nAye, Sir, aye\r\nCaptain, captain)\r\n\r\nAs we live a life of ease\r\nEvery one of us has all we need\r\nSky of blue and sea of green\r\nIn our yellow submarine\r\n\r\nWe all live in a yellow submarine\r\nYellow submarine, yellow submarine\r\nWe all live in a yellow submarine\r\nYellow submarine, yellow submarine\r\nWe all live in a yellow submarine\r\nYellow submarine, yellow submarine"
b=''.join(b)
b=b.replace('\r', '')
b=b.replace('\n', ' ')

sim= GetMixedLyrics.calculate_similarity(a,b)
print(sim)
'''