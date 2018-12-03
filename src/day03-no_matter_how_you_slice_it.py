from santas_little_helpers import day, get_data, timed
from collections import defaultdict
from itertools import permutations

today = day(2018, 3)

def map_all_claims(data):
  m = {}
  for claimer, (x, y), area in data:
    map_area(m, (x, y), area, claimer)
  count = 0
  for x in m.values():
    for y, _ in x.values():
      if y > 1:
        count += 1
  return count, m

def map_area(m, root, area, claimer):
  x, y = root
  xd, yd = area
  for xp in range(x, x+xd):
    if xp not in m:
      m[xp] = defaultdict(lambda: (0, []))
    for yp in range(y, y+yd):
      count, claimers = m[xp][yp]
      m[xp][yp] = count + 1, claimers + [claimer]

def find_unique_claim(m, all_claimers):
  for x in m.values():
    for count, claimers in x.values():
      if count > 1:
        for claimer in claimers:
          if claimer in all_claimers:
            all_claimers.remove(claimer)
  return all_claimers[0]


def fun(line):
  claimer, line = line.split(' @ ')
  claimer = claimer[1:]
  coords, area = line.split(': ')
  coords = coords.split(',')
  area = area.strip().split('x')
  return claimer, (int(coords[0]), int(coords[1])), (int(area[0]), int(area[1]))

def main() -> None:
  data = list(get_data(today, [('func', fun)]))

  star1, m = map_all_claims(data)
  print(f'{today} star 1 = {star1}')
  all_claimers = [claimer for claimer, _, _ in data]
  print(f'{today} star 2 = {find_unique_claim(m, all_claimers)}')

if __name__ == '__main__':
  timed(main)
