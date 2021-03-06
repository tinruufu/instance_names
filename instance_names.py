from mastodon import Mastodon
from pythonwhois import get_whois
from pythonwhois.shared import WhoisException
import json, random, threading, os

min_delay = 600
max_delay = 1800

#get tlds from text file with all generic tlds
tlds = []
with open("tlds.txt", 'r') as f:
	tlds = f.read().split('\n')

#get words, courtesy of darius kazemi's corpora project https://github.com/dariusk/corpora
words = []
for file in os.listdir('./corpus'):
	if file.endswith(".json"):
		print("loading " + file)
		with open(os.path.join("./corpus", file), 'r') as f:
			words.append(json.loads(f.read())["words"])

#get login info from secrets.json
secrets = {}
with open('secrets.json', 'r') as f:
	secrets = json.loads(f.read())

mastodon = Mastodon(client_id=secrets["id"], client_secret=secrets["secret"], access_token=secrets["access_token"], api_base_url="https://cybre.space")


def get_available_domain():
	for attempt in range(10):
		tld = random.choice(tlds).lower()
		word = random.choice(random.choice(words)).lower()
		name = "{}{}".format(word, tld)

		try:
			whois = get_whois(name)
		except WhoisException:
			continue

		if not whois.get('id'):
			return name
	else:
		raise RuntimeError('tried too many times')


def make_post():
	name = get_available_domain()

	print("posting {}".format(name))

	mastodon.status_post(name, visibility="unlisted")
	threading.Timer(random.randint(min_delay, max_delay), make_post).start()


make_post()
