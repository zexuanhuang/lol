import matplotlib.pyplot as plt
import datetime
import numpy as np
import json
import argparse

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
	npu = np.array(units)
	bad = npa <= 0.5
	good = npa > 0.5

	fig, ax = plt.subplots()
	ax.bar(npu[bad], npa[bad], color='gray')
	ax.bar(npu[good], npa[good], color='red')

	for i, u in enumerate(units):
		uu = "***" if rates[u] > 0.5 else ''
		value = "{:.2%}".format(rates[u])

		print(f'{unit}:{u} win rate:{value} wins:{wins[u]} loses:{loses[u]} {uu}')

		if rates[u] > 0:
			ax.text(u-0.4, rates[u]+0.01, value, fontsize=8, va='center')
			ax.text(u-0.3, rates[u]-0.02, f'wins:{wins[u]}', fontsize=8, va='center')
			ax.text(u-0.3, rates[u]-0.04, f'loses:{loses[u]}', fontsize=8, va='center')
	plt.axhline(y=0.5)

	plt.show()


def main():
	p = argparse.ArgumentParser()
	p.add_argument('unit', choices=['hour', 'date'])
	result = p.parse_args()
	match_file = './matches.json'
	with open(match_file, 'r') as f:
		matches = json.load(f)

	by_unit(matches, result.unit)


if __name__ == '__main__':
	main()
