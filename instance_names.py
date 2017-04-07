from mastodon import Mastodon
import json, random, threading

delay = 3600

#get tlds from text file with all generic tlds
tlds = []
with open("tlds.txt", 'r') as f:
	tlds = f.read().split('\n')

#get words, courtesy of darius kazemi's corpora project https://github.com/dariusk/corpora
words = []
with open("common.json", 'r') as f:
	words += (json.loads(f.read())["commonWords"])

with open("strange.json", 'r') as f:
	words += (json.loads(f.read())["words"])

with open("nouns.json", 'r') as f:
	words += (json.loads(f.read())["nouns"])

#get login info from secrets.json
secrets = {}
with open('secrets.json', 'r') as f:
	secrets = json.loads(f.read())

mastodon = Mastodon(client_id=secrets["id"], client_secret=secrets["secret"], access_token=secrets["access_token"], api_base_url="https://cybre.space")

def make_post():
	tld = random.choice(tlds)
	word = random.choice(words)

	name = "{}{}".format(word, tld)
	
	print("posting {}".format(name))

	mastodon.status_post(name, visibility="unlisted")
	threading.Timer(delay, make_post).start()


make_post()