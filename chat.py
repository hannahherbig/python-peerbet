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
args = parser.parse_args()

bot = Peerbet(args.username, args.password)

print(bot.chat())
print(bot.postchat('testing'))
