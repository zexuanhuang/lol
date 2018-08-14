import requests
import json
import datetime
import os.path
import sys
import time

class lol:
	def __init__(self):
		self.match_api_url = 'https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/'
		self.match_by_id_api_url = 'https://na1.api.riotgames.com/lol/match/v3/matches/'
		self.account_id = 239023994
		self.api_token = 'RGAPI-0ac15603-3cc5-4749-9d36-63fbea1f02fc'
		self.champion_url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions'
		self.champions_dict = None
		self.headers = {
			'X-Riot-Token': self.api_token
		}

		self.matches_parsed = None

	def get_today(self):
		return datetime.datetime.today()

	def to_msec(self, dt):
		return int(dt.timestamp()*1000)

	def get_champions(self):
		champion_file = './champions.json'

		if os.path.isfile(champion_file):
			print('champions static file exists...loading')
			with open(champion_file, 'r') as f:
				self.champions_dict = json.load(f)
			print(f'loaded {len(self.champions_dict)} champions')
			return

		r = requests.get(self.champion_url, headers=self.headers)
		champions = r.json()['data']

		self.champions_dict = { c['id']:c['name'] for _,c in champions.items() }

		with open(champion_file, 'w') as f:
			json.dump(self.champions_dict, f)
			print(f'download {len(self.champions_dict)} champions to {champion_file}')

	def get_match_data(self, beginTime, endTime):
		def get_match_by_id(gameId):
			def helper():
				return requests.get(self.match_by_id_api_url + str(gameId), headers=self.headers)

			r = helper()
			while r.status_code != requests.codes.ok:
				print(r.json())
				print('sleep 60 sec...')
				time.sleep(60)
				r = helper()
			r = r.json()
			win_team_id = None
			if r['teams'][0]['win'] == 'Win':
				win_team_id = r['teams'][0]['teamId']
			else:
				win_team_id = r['teams'][1]['teamId']
			my_participant_id = None
			my_team_id = None
			for p in r['participantIdentities']:
				if p['player']['accountId'] == self.account_id:
					my_participant_id = p['participantId']
					break

			for p in r['participants']:
				if p['participantId'] == my_participant_id:
					my_team_id = p['teamId']
					break

			if my_team_id == win_team_id:
				return True
			return False

		params = {
			'beginTime': self.to_msec(beginTime),
			'endTime': self.to_msec(endTime)
		}

		response = requests.get(self.match_api_url+str(self.account_id), params=params, headers=self.headers)

		r = response.json()
		matches = r['matches']

		for match in matches:
			gameId = match['gameId']
			if gameId in self.matches_parsed:
				continue

			m = {
				'lane': match['lane'],
				'time': match['timestamp']//1000,
				'champion': match['champion'],
				'result': 'Won' if get_match_by_id(gameId) else 'Lost'
			}
			print(f"downloaded 1 match, {m['result']} at {m['time']}")
			self.matches_parsed[gameId] = m

	def process(self, span=30):
		self.get_champions()

		start_date = self.get_today()
		span_dtd = datetime.timedelta(days=span)
		end_date = start_date - span_dtd
		one_day = datetime.timedelta(days=1)

		matches_file = './matches.json'

		if os.path.isfile(matches_file):
			with open(matches_file, 'r') as f:
				print('previous data exists...loading')
				self.matches_parsed = json.load(f)
				print('loaded ')
		else:
			self.matches_parsed = {}

		while start_date > end_date:
			beginTime = start_date-one_day*5
			self.get_match_data(beginTime, start_date)
			start_date -= one_day*5

		with open(matches_file, 'w') as f:
			json.dump(self.matches_parsed, f)
			print(f'downloaded {len(self.matches_parsed)} matches,\nfrom: {self.get_today()} \nto: {end_date}')

def main():
	l = lol()
	l.process()


if __name__ == '__main__':
	main()
