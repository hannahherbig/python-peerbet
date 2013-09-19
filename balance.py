import peerbet

import argparse
import sys
from decimal import Decimal
from time import strftime, sleep

def color(n):
  return '\033[%dm%+.8f\033[m' % (32 if n >= 0 else 31, n)

parser = argparse.ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
args = parser.parse_args()

sys.stdout.write('\rlogging in')
sys.stdout.flush()

bot = peerbet.Peerbet(args.username, args.password)

balance = bot.balance()

while True:
  new = bot.balance()

  sys.stdout.write('\r%s | %.8f ' % (strftime('%H:%M:%S'), new))

  if new != balance:
    sys.stdout.write('| %s\n' % color(new - balance))
    balance = new

  sys.stdout.flush()

  sleep(10)
