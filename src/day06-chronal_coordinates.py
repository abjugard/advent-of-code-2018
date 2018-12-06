from santas_little_helpers import day, get_data, timed
from collections import defaultdict
from itertools import product

today = day(2018, 6)

safe_space = set()

def assess_coordinates(coordinates):
  x_max = max(x for x, _ in coordinates)-1
  x_min = min(x for x, _ in coordinates)+1
  y_max = max(y for _, y in coordinates)-1
  y_min = min(y for _, y in coordinates)+1
  infinite_coordinates = set()
  isolation_zones = defaultdict(int)
  for x, y in product(range(x_min-1, x_max+1), range(y_min-1, y_max+1)):
    closest = closest_nodes(coordinates, x, y)
    if x in [x_min, x_max] or y in [y_min, y_max]:
      infinite_coordinates.update(closest)
    if len(closest) == 1:
      isolation_zones[closest[0]] += 1
  return max(area for coordinate, area
                  in isolation_zones.items()
                  if coordinate not in infinite_coordinates)

def closest_nodes(coords, x, y):
  closest_distance = 1000
  distances = {}
  d_sum = 0
  for xp, yp in coords:
    d = abs(x-xp) + abs(y-yp)
    d_sum += d
    if d <= closest_distance:
      closest_distance = d
      distances[(xp, yp)] = d
  if d_sum < 10000:
    safe_space.add((x, y))
  return [coord for coord, d
                in distances.items()
                if d is closest_distance]

def main() -> None:
  coords = list(get_data(today, [('split', ', '), ('map', int)]))

  print(f'{today} star 1 = {assess_coordinates(coords)}')
  print(f'{today} star 2 = {len(safe_space)}')

if __name__ == '__main__':
  timed(main)
