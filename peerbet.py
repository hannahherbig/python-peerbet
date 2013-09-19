import requests

import time
import decimal

BASE_URI = 'https://peerbet.org/api.php'

RATE_LIMITS = {
  'login': 5,
  'signup': 5,
  'getuserinfo': 0,
  'getdepositaddress': 0,
  'getactiveraffles': 1,
  'getraffleinfo': 1, 
  'getmyrafflecount': 0,
  'getmyraffles': 5,
  'createraffle': 1,
  'buytickets': 1,
  'refund': 1,
  'authorize': 5,
  'transfer': 1,
  'gettransferlist': 1,
  'getchatmessages': 1,
  'postchatmessage': 1
}

class RequestException(Exception):
  pass

last_request = float('-inf')

def request(method, **params):
  global last_request

  diff = last_request + RATE_LIMITS[method] - time.time()

  if diff > 0:
    time.sleep(diff)

  params['method'] = method

  try:
    data = requests.post(BASE_URI, data=params).json()

    if 'error' not in data:
      return data
    else:
      raise RequestException(data['error'])

  finally:
    last_request = time.time()

def login(username, password):
  r = request('login', username=username, password=password)

  if r['success']:
    return r
  else:
    raise RequestException('success is %r' % r['success'])

def signup(username, email, password):
  r = request('signup', username=username, email=email, password=password)

  if r['success']:
    return r
  else:
    raise RequestException('success is %r' % r['success'])

def activeraffles():
  return request('getactiveraffles')

def getraffle(raffle):
  return request('getraffleinfo', raffle=raffle)

class Peerbet(object):
  def __init__(self, username, password):
    r = login(username, password)

    self.username = r['username']
    self.key = r['key']

  def request(self, method, **params):
    return request(method, key=self.key, **params)

  def balance(self):
    return decimal.Decimal(self.request('getuserinfo')['balance'])

  def stats(self):
    return self.request('getuserinfo', stats='1')

  def deposit(self):
    return self.request('getdepositaddress')['address']

  def activeraffles(self):
    return self.request('getactiveraffles')

  def getraffle(self, raffle):
    return self.request('getraffleinfo', raffle=raffle)

  def rafflecount(self):
    return int(self.request('getmyrafflecount')['count'])

  def myraffles(self, page=0):
    return self.request('getmyraffles', page=page)

  def create(self, tickets, price, instant=True, password=None, expire=None):
    params = {
      'tickets': tickets,
      'price': str(price),
      'instant': 1 if instant else 0
    }

    if password:
      params['password'] = password

    if expire:
      params['expire'] = expire

    return self.request('createraffle', **params)['raffle_id']

  def buy(self, raffle, tickets=1):
    r = self.request('buytickets', raffle=raffle, tickets=tickets)

    if r['success']:
      return r
    else:
      raise RequestException('success is %r' % r['success'])

  def refund(self, raffle):
    r = self.request('refund', raffle=raffle)

    if r['success']:
      return r
    else:
      raise RequestException('success is %r' % r['success'])

  def authorize(self, raffle, password):
    r = self.request('authorize', raffle=raffle, password=password)

    if r['success']:
      return r
    else:
      raise RequestException('success is %r' % r['success'])

  def transfer(self, recipient, amount):
    r = self.request('transfer', recipient=recipient, amount=amount)

    if r['success']:
      return r
    else:
      raise RequestException('success is %r' % r['success'])

  # this is where i got bored and just wanted to win some coins. there's more
  # stuff in the API. feel free to submit a pull request.
