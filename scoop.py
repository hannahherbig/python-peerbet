import peerbet

import traceback
import argparse
import sys
from decimal import Decimal
from time import strftime, sleep

def log(line):
  sys.stdout.write('\r\033[K%s - %s' % (strftime('%H:%M:%S'), line))
  sys.stdout.flush()

def puts(line):
  sys.stdout.write('\r\033[K%s - %s\n' % (strftime('%H:%M:%S'), line))
  sys.stdout.flush()

parser = argparse.ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('target', type=Decimal)
args = parser.parse_args()

log('logging in')

bot = peerbet.Peerbet(args.username, args.password)

balance = bot.balance()

while balance < args.target:
  log('%.8f' % balance)

  if balance > 0:
    raffles = []

    for r in bot.activeraffles():
      if not r['protected'] and r['instant'] == '1':
        sold = int(r['tickets_sold'])
        total = int(r['tickets_total'])
        left = total - sold
        price = Decimal(r['ticket_price']) * left

        raffles.append((r['raffle_id'], left, total, price, 'instant' if r['instant'] == '1' else 'provably fair'))

    raffles.sort(key=lambda t: t[3])

    for raffle, left, total, price, type in raffles:
      if left != total and float(left) / total >= 0.5 and price < balance:
        puts('%.8f - buying %d tickets for %.8f BTC - %s' % (balance, left,
          price, type))

        try:
          bot.buy(raffle, left)
        except:
          traceback.print_exc()
          sleep(10)

        break

  else:
    sleep(10)

  balance = bot.balance()
