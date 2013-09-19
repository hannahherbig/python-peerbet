import peerbet

import argparse
import sys
from itertools import count
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
args = parser.parse_args()

bot = peerbet.Peerbet(args.username, args.password)

for p in count():
  print(bot.myraffles(p))