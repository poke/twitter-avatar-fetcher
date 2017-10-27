#! /usr/bin/env python3
from collections import Counter
from urllib.request import urlopen, Request
import argparse
import base64
import json
import os
import re
import shutil
import urllib.parse

reScreenName = re.compile('^[a-z0-9_]{1,15}$', re.I)
def validateScreenName (screenName):
	if reScreenName.match(screenName):
		return True

	print('Invalid screen name:', screenName.encode())
	return False

class TwitterAvatarFetcher:
	def __init__ (self, targetFolder):
		if not os.path.exists(targetFolder):
			os.makedirs(targetFolder)
		self.targetFolder = targetFolder

		with open('config.json') as f:
			config = json.load(f)
		self.key = base64.b64encode('{}:{}'.format(config['consumer_key'], config['consumer_secret']).encode()).decode()

	def retrieveBearerToken (self):
		req = Request('https://api.twitter.com/oauth2/token')
		req.method = 'POST'
		req.add_header('Authorization', 'Basic {}'.format(self.key))
		req.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=utf-8')
		req.data = b'grant_type=client_credentials'

		with urlopen(req) as resp:
			data = json.loads(resp.read().decode())

		self.bearerToken = data['access_token']

	def getUsers (self, users):
		req = Request('https://api.twitter.com/1.1/users/lookup.json')
		req.method = 'POST'
		req.data = urllib.parse.urlencode({ 'screen_name': ','.join(users) }).encode()
		req.add_header('Authorization', 'Bearer {}'.format(self.bearerToken))
		req.add_header('Content-type', 'application/x-www-form-urlencoded')

		with urlopen(req) as resp:
			return json.loads(resp.read().decode())

	def downloadAvatars (self, users):
		users = Counter(filter(validateScreenName, users))
		for user, count in users.items():
			if count > 1:
				print('Duplicated screen name: "{}" ({} times)'.format(user, count))

		users = list(users.keys())
		print('Downloading avatars for {} users'.format(len(users)))
		for i in range(0, len(users), 50):
			batch = set((u.lower() for u in users[i:i+50]))
			for user in self.getUsers(batch):
				screenName = user['screen_name']
				batch.remove(screenName.lower())
				url = user['profile_image_url'].replace('_normal', '')
				path = os.path.join(self.targetFolder, screenName + os.path.splitext(url)[1])
				try:
					with urlopen(url) as res, open(path, 'wb+') as f:
						shutil.copyfileobj(res, f)
				except Exception as e:
					print('Download failed for "{}"\n  '.format(screenName, e))

			if batch:
				print('Skipped by the Twitter API:', batch)

def main ():
	parser = argparse.ArgumentParser(description='Fetch user avatars from Twitter.')
	parser.add_argument('file', help='File with usernames')
	parser.add_argument('-t', '--target', default='output', help='target path')
	args = parser.parse_args()

	if not os.path.exists('config.json'):
		parser.error('You need to create a config.json file first. Check the README file for details.')

	dl = TwitterAvatarFetcher(args.target)
	dl.retrieveBearerToken()

	with open(args.file, encoding='utf-8') as f:
		users = list(line.strip() for line in f)
	dl.downloadAvatars(users)

if __name__ == '__main__':
	main()
