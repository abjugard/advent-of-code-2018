from santas_little_helpers import day, get_data, timed
from collections import defaultdict
from itertools import permutations, product
import re

today = day(2018, 3)
r = re.compile(r'#(?P<claimer>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)')

def map_all_claims(data):
  m = defaultdict(lambda: defaultdict(lambda: (0, [])))
  for claimer, coords, area in data:
    map_area(claimer, coords, area, m)
  return sum(1 for x in m.values() for y, _ in x.values() if y > 1), m

def map_area(claimer, root, area, m):
  x, y = root
  w, h = area
  for xp, yp in product(range(x, x+w), range(y, y+h)):
    count, claimers = m[xp][yp]
    m[xp][yp] = count + 1, claimers + [claimer]

def find_unique_claim(m, all_claimers):
  for claimers in [claimers for x in m.values() 
                            for n, claimers in x.values() if n > 1]:
    for claimer in [claimer for claimer in claimers 
                            if claimer in all_claimers]:
      all_claimers.remove(claimer)
  return all_claimers[0]

def fun(line):
  m = r.match(line)
  claimer = m['claimer']
  coords = int(m['x']), int(m['y'])
  area = int(m['w']), int(m['h'])
  return claimer, coords, area

def main() -> None:
  data = list(get_data(today, [('func', fun)]))

  star1, m = map_all_claims(data)
  print(f'{today} star 1 = {star1}')
  all_claimers = [claimer for claimer, _, _ in data]
  print(f'{today} star 2 = {find_unique_claim(m, all_claimers)}')

if __name__ == '__main__':
  timed(main)
