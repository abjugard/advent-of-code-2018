from santas_little_helpers import day, get_data, timed
from collections import namedtuple

today = day(2018, 25)

constellations = []

class Point(object):
  def __init__(self, line):
    self.x, self.y, self.z, self.t = line
  def distance(self, other):
    return abs(self.x-other.x) \
         + abs(self.y-other.y) \
         + abs(self.z-other.z) \
         + abs(self.t-other.t)
  def can_reach(self, other):
    return self.distance(other) <= 3

class Constellation(object):
  def __init__(self, p):
    self.points = {p}
  def __contains__(self, other):
    return any(self.near(p) for p in other.points)
  def __repr__(self):
    return str(len(self.points))
  def near(self, p):
    return any(p.can_reach(pt) for pt in self.points)
  def merge(self, other):
    self.points |= other.points
  def __add__(self, other):
    self.points.add(other)

def run(inp):
  for p in inp:
    found = False
    for constellation in constellations:
      if constellation.near(p):
        constellation += p
        found = True
        break
    if not found:
      constellations.append(Constellation(p))
  while True:
    to_del = []
    for i, c1 in enumerate(constellations):
      if i in to_del:
        continue
      for j, c2 in enumerate(constellations):
        if j == i:
          continue
        if (j not in to_del) and c1 in c2:
          c1.merge(c2)
          to_del.append(j)
    if len(to_del) == 0:
      return constellations
    for i in sorted(to_del, reverse=True):
      del constellations[i]

def main() -> None:
  inp = get_data(today, [('split', ','), ('map', int), ('func', Point)])

  print(f'{today} star 1 = {len(run(inp))}')

if __name__ == '__main__':
  timed(main)
