from santas_little_helpers import day, get_data, timed
from itertools import product
from operator import attrgetter as attr
import re

today = day(2018, 23)

r = re.compile(r'pos=<([-\d]*),([-\d]*),([-\d]*)>, r=([-\d]*)')

class Point(object):
  def __init__(self, x, y, z):
    self.x, self.y, self.z = x, y, z
  @property
  def displacement(self):
    return abs(self.x) + abs(self.y) + abs(self.z)
  def reaches(self, bots, box_diameter):
    return sum(bot.in_range(self, box_diameter) for bot in bots)

ORIGIN = Point(0, 0, 0)

class Nanobot(object):
  def __init__(self, line):
    self.x, self.y, self.z, self.r = map(int, r.match(line).groups())
  def in_range(self, other, box_diameter = 0):
    return self.manhattan(other) < self.r + box_diameter
  def manhattan(self, other):
    return abs(self.x-other.x) + abs(self.y-other.y) + abs(self.z-other.z)

def ranges(center, size):
  return range(center.x - size, center.x + size + 1, size), \
         range(center.y - size, center.y + size + 1, size), \
         range(center.z - size, center.z + size + 1, size)

def points_to_test(center, size):
  return [Point(*cs) for cs in product(*ranges(center, size))]

def find_optimal_position(bots):
  box_size = 1
  while box_size < max(bots, key=attr('x')).x - min(bots, key=attr('x')).x:
    box_size *= 2

  box_center = ORIGIN
  while box_size > 0:
    best, best_count = None, None
    for p in points_to_test(box_center, box_size):
      count = p.reaches(bots, box_size)
      if best is None \
         or count > best_count \
         or count == best_count and p.displacement < best.displacement:
        best, best_count = p, count
    box_center = best
    box_size //= 2
  return box_center.displacement

def main() -> None:
  bots = list(get_data(today, [('func', Nanobot)]))
  strongest = max(bots, key=attr('r'))
  print(f'{today} star 1 = {sum(strongest.in_range(bot) for bot in bots)}')
  print(f'{today} star 2 = {find_optimal_position(bots)}')

if __name__ == '__main__':
  timed(main)
