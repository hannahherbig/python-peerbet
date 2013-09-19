from peerbet import Peerbet

from argparse import ArgumentParser
from decimal import Decimal
from time import strftime
import sys

def log(line):
  sys.stdout.write('\r\033[K%s - %s' % (strftime('%H:%M:%S'), line))
  sys.stdout.flush()

def puts(line):
  sys.stdout.write('\r\033[K%s - %s\n' % (strftime('%H:%M:%S'), line))
  sys.stdout.flush()

parser = ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('price', type=Decimal)
parser.add_argument('tickets', type=int)
parser.add_argument('total', type=int)
parser.add_argument('-t', '--target', type=Decimal, default=Decimal('Infinity'))
parser.add_argument('-f', '--fair', dest='instant', action='store_false')
args = parser.parse_args()

puts('logging in')

bot = Peerbet(args.username, args.password)

price = args.price

balance = bot.balance()
n = 0

while price < balance < args.target:
	puts('%.8f' % balance)

	log('creating raffle')
	raffle = bot.create(args.total * 2 ** n, price, instant=args.instant)
	log('buying tickets')
	bot.buy(raffle, args.tickets * 2 ** n)
	log('waiting')

	waiting = True

	while waiting:
		r = bot.getraffle(raffle)
		sold = int(r['tickets_sold'])
		total = int(r['tickets_total'])

		if r['status'] == 'waiting':
			log('waiting for block')
		elif r['status'] == 'win':
		  puts('won')
		  n = 0
		  waiting = False
		elif r['status'] == 'lose':
		  puts('lost')
		  n += 1
		  waiting = False
		elif r['status'] == 'finished':
			puts('for some reason this bet is "finished" and not "win" or "lose"')
			puts("i'll just exit since that's probably what you meant")
			sys.exit(1)
		else:
			log('%d/%d = %.2f%%' % (sold, total, 100.0 * sold / total))

	balance = bot.balance()
