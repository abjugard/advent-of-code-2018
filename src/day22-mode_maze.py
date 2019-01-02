from santas_little_helpers import day, get_data, timed
from collections import namedtuple
from itertools import product
from networkx import Graph
from networkx import dijkstra_path_length

erosion = {}
cavern = []
depth, target = None, None

class Point(namedtuple('Point', ['x', 'y'])):
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
  def __le__(self, other):
    return self.x <= other.x and self.y <= other.y

  @property
  def    up(self): return self + Point(0, -1)
  @property
  def  down(self): return self + Point(0, 1)
  @property
  def  left(self): return self + Point(-1, 0)
  @property
  def right(self): return self + Point(1, 0)

  @property
  def neighbours(self):
    return [self.up, self.down, self.left, self.right]
  @property
  def erosion(self):
    return erosion[self]

ENTRANCE = Point(0, 0)
UP, DOWN, LEFT, RIGHT = ENTRANCE.neighbours

today = day(2018, 22)

def geologic_index(p, target):
  if p in [ENTRANCE, target]:
    return 0
  elif p.x == 0:
    return p.y * 48271
  elif p.y == 0:
    return p.x * 16807
  else:
    return p.left.erosion * p.up.erosion

def equipment(erosion_level):
  erosion_level %= 3
  if erosion_level == 0:
    return {1, 2}
  return {0, erosion_level}

def calculate_erosion():
  for p in cavern:
    erosion[p] = (geologic_index(p, target) + depth) % 20183

def rescue():
  cave_graph = Graph()
  for p in cavern:
    e1, e2 = equipment(erosion[p])
    cave_graph.add_edge((p, e1), (p, e2), weight=7)
    for pd in p.neighbours:
      if pd not in erosion:
        continue
      tools = equipment(erosion[p]) \
            & equipment(erosion[pd])
      for tool in tools:
        cave_graph.add_edge((p, tool), (pd, tool), weight=1)
  return dijkstra_path_length(cave_graph, (ENTRANCE, 2), (target, 2))

def main() -> None:
  global depth, target
  it = get_data(today, [('split', ' '), ('func', lambda l: l[1].strip())])
  depth = int(next(it))
  target = Point(*map(int, next(it).split(',')))
  cavern.extend(Point(x, y) for x, y in product(range(target.x + 50), range(target.y + 50)))

  calculate_erosion()
  print(f'{today} star 1 = {sum([erosion[p] % 3 for p in erosion if p <= target])}')
  print(f'{today} star 2 = {rescue()}')

if __name__ == '__main__':
  timed(main)
