import matplotlib.pyplot as plt
import datetime
import numpy as np
import json


def by_unit(matches, unit):
	spans = {
		'hour': 24,
		'date': 7
	}
	span = spans[unit]
	wins = { i:0 for i in range(span)}
	loses = { i:0 for i in range(span)}
	rates = []
	units = [ i for i in range(span) ]

	def get_bin(time, unit):
		if unit == 'hour':
			return time.hour
		if unit == 'date':
			return time.weekday()
		raise Exception('f u')

	for _, body in matches.items():
		time = datetime.datetime.fromtimestamp(body['time'])
		if body['result'] == 'Won':
			wins[get_bin(time, unit)] += 1
		else:
			loses[get_bin(time, unit)] += 1

	for u in units:
		if wins[u] == 0 and loses[u] == 0:
			rate = 0
		else:
			rate = wins[u] / (wins[u]+loses[u])
		rates.append(rate)

	npa = np.array(rates)
	rates_marked = np.ma.masked_where(npa < 0.5, npa)

	fig, ax = plt.subplots()
	ax.bar(units, rates_marked)

	for u in units:
		uu = "***" if rates[u] > 0.5 else ''
		print(f'{unit}:{uu} win rate:{rates[u]} {uu}')

	plt.axhline(y=0.5)

	plt.show()


def main():
	match_file = './matches.json'
	with open(match_file, 'r') as f:
		matches = json.load(f)

	by_unit(matches, 'date')


if __name__ == '__main__':
	main()
