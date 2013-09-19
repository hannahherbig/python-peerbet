import peerbet

from requests.exceptions import RequestException

from argparse import ArgumentParser
from decimal import Decimal
from time import strftime, sleep
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
parser.add_argument('-t', '--target', type=Decimal, default=Decimal('Infinity'))
parser.add_argument('-s', '--stop', type=Decimal, default=Decimal(0))
args = parser.parse_args()

log('logging in')

bot = peerbet.Peerbet(args.username, args.password)

balance = bot.balance()

while args.stop < balance < args.target:
  log('%.8f' % balance)

  if balance > 0:
    try:
      raffles = []

      for r in bot.activeraffles():
        if not r['protected'] and r['instant'] == '1' and r['my_tickets_count'] == '0':
          sold = int(r['tickets_sold'])
          total = int(r['tickets_total'])
          left = total - sold
          price = Decimal(r['ticket_price']) * left

          raffles.append((r['raffle_id'], left, total, price, 'instant' if r['instant'] == '1' else 'provably fair'))

      raffles.sort(key=lambda t: t[3])

      for raffle, left, total, price, type in raffles:
        if left != total and float(left) / total >= 0.2 and price < balance:
          puts('%.8f - buying %d tickets for %.8f BTC - %s' % (balance, left,
            price, type))

          try:
            bot.buy(raffle, left)
          except peerbet.RequestException as e:
            puts(e)
            continue

          break

    except RequestException as e:
      puts(e)
      sleep(10)

  else:
    sleep(10)

  balance = bot.balance()
