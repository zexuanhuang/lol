import matplotlib.pyplot as plt
import datetime
import numpy as np
import json

def by_hour(matches):
	wins = {i:0 for i in range(24)}
	loses = {i:0 for i in range(24)}
	rates = []
	hours = [i for i in range(24)]

	for _, body in matches.items():
		time = datetime.datetime.fromtimestamp(body['time'])
		if body['result'] == 'Won':
			wins[time.hour] += 1
		else:
			loses[time.hour] += 1

	for hour in hours:
		if wins[hour] == 0 and loses[hour] == 0:
			rate = 0
		else:
			rate = wins[hour] / (wins[hour] + loses[hour])
		rates.append(rate)

	npa = np.array(rates)
	rates_marked = np.ma.masked_where( npa < 0.5, npa)

	fig, ax = plt.subplots()
	ax.bar(hours, rates_marked)

	for h in hours:
		hi ="***" if rates[h] > 0.5 else ''
		print(f'hour:{h} win rate:{rates[h]} {hi}')

	plt.axhline(y=0.5)

	plt.show()

def by_date(matches):
    wins = {i:0 for i in range(7)}
    loses = {i:0 for i in range(7)}
    rates = []
    dates = [i for i in range(7)]

    for _, body in matches.items():
        date = datetime.datetime.fromtimestamp(body['time']).weekday()
        if body['result'] == 'Won':
            wins[date] += 1
        else:
            loses[date] += 1

    for date in dates:
        if wins[date] == 0 and loses[hour] == 0:
            rate = 0
        else:
            rate = wins[date] / (wins[date]+loses[date])
        rates.append(rate)

    npa = np.array(rates)
    rates_marked = np.ma.masked_where(npa < 0.5, npa)
    fig, ax = plt.subplots()
    ax.bar(dates, rates_marked)

    plt.axhline(y=0.5)
    plt.show()

def main():
	match_file = './matches.json'
	with open(match_file, 'r') as f:
		matches = json.load(f)
	# x, y = [], []
	# for id, body in matches.items():
	# 	x.append(datetime.datetime.fromtimestamp(body['time']))
	# 	y.append(1 if body['result'] == 'Won' else -1)

	# plt.plot(x, y)
	# plt.show()

	by_hour(matches)
	by_date(matches)

if __name__ == '__main__':
	main()
