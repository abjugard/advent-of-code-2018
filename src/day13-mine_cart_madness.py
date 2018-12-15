from santas_little_helpers import day, get_data, timed
from collections import deque
from itertools import product

today = day(2018, 13)

_turns = {
   'left': { '>': '^', '^': '<', '<': 'v', 'v': '>' },
  'right': { '>': 'v', 'v': '<', '<': '^', '^': '>' }
}

_bends = {
   '/': { '>': '^', '^': '>', '<': 'v', 'v': '<' },
  '\\': { '>': 'v', 'v': '>', '^': '<', '<': '^' }
}

class Cart(object):
  def __init__(self, y, x, direction, next_turn = 'left', track = None):
    self.y = y
    self.x = x
    self.direction = direction
    self.next_turn = next_turn
    self.track = track

  def copy(self):
    return Cart(self.y, self.x, self.direction, self.next_turn, self.track)

  def set_track(self, track):
    self.track = track

  def travel(self):
    if self.direction == '>':
      self.x += 1
    elif self.direction == '^':
      self.y -= 1
    elif self.direction == '<':
      self.x -= 1
    elif self.direction == 'v':
      self.y += 1
    track_part = self.track[self.y][self.x]
    if track_part in _bends:
      self.direction = _bends[track_part][self.direction]
    elif track_part == '+':
      self._turn()

  def __str__(self):
    return f'{self.x},{self.y}'

  def __lt__(self, other):
    return self.position < other.position

  def _get_position(self):
    return self.y, self.x
  
  def _turn(self):
    if self.next_turn == 'straight':
      self.next_turn = 'right'
    else:
      self.direction = _turns[self.next_turn][self.direction]
      self.next_turn = 'left' if self.next_turn == 'right' else 'straight'

  position = property(_get_position)

def simulate(carts):
  while len(carts) > 1:
    to_del = []
    carts = sorted(carts)
    for i, cart in enumerate(carts):
      if i in to_del:
        continue
      updated = cart.copy()
      updated.travel()
      for j, other in enumerate(carts):
        if (j not in to_del) and other.position == updated.position:
          to_del += [i, j]
      carts[i] = updated
    for i in sorted(to_del, reverse=True):
      yield carts[i]
      del carts[i]
  yield carts[0]

def setup_carts(track):
  carts = []
  for x, y in product(range(len(track)), range(len(track[0]))):
    symbol = track[y][x]
    if symbol in '>^<v':
      carts += [Cart(y, x, symbol, 'left')]
      if symbol in '<>':
        track[y] = track[y][:x] + '-' + track[y][x+1:]
      if symbol in '^v':
        track[y] = track[y][:x] + '|' + track[y][x+1:]
  for cart in carts:
    cart.set_track(track)
  return carts

def main() -> None:
  track = list(get_data(today))
  carts = setup_carts(track)

  it = simulate(carts)
  print(f'{today} star 1 = {next(it)}')
  print(f'{today} star 2 = {deque(it, maxlen = 1).pop()}')

if __name__ == '__main__':
  timed(main)
