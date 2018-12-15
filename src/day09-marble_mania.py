from santas_little_helpers import day, get_data, timed
from collections import defaultdict

today = day(2018, 9)

class Marble:
  def __init__(self, value):
    self.value = value
    self.prev = self
    self.next = self

  def neighbours(self):
    return self.prev, self.next

  def new_neighbours(self):
    return self.next, self.next.next

  def play(self, value):
    if value % 23 > 0:
      current = Marble(value)
      current.prev, current.next = self.new_neighbours()
      current.prev.next = current.next.prev = current
      return current, 0
    else:
      current = self
      for _ in range(7):
        current = current.prev
      current.next.prev, current.prev.next = current.neighbours()
      return current.next, value + current.value

def play_marble(players, final_marble):
  scores = defaultdict(int)
  value = player = 0
  current = Marble(value)
  while value <= final_marble:
    value += 1
    current, points_gained = current.play(value)
    scores[player] += points_gained
    player = (player + 1) % players
  return max(scores.values())

def main() -> None:
  data = next(get_data(today, [('split', ' ')]))
  players, final_marble = int(data[0]), int(data[-2])

  print(f'{today} star 1 = {play_marble(players, final_marble)}')
  print(f'{today} star 2 = {play_marble(players, final_marble * 100)}')

if __name__ == '__main__':
  timed(main)
