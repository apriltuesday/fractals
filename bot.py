#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import tweepy


# twitter auth
# consumer_key = os.environ['CONSUMER_KEY']
# consumer_secret = os.environ['CONSUMER_SECRET']
# access_token = os.environ['ACCESS_TOKEN']
# access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)


BOT_NAME = 'FractalBot'


class FractalBot(tweepy.StreamListener):

	def random_post(self):
		try:
			#api.update_with_media(output_file, message)
			print 'done!'
		except Exception as e:
			print 'couldn\'t create status :', e


def main():
	bot = FractalBot()
	print 'up and running!'

	# post randomly every 4 hours
	while True:
		bot.random_post()
		time.sleep(14400)


if __name__ == '__main__':
	main()
