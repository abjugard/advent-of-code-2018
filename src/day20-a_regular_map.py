from santas_little_helpers import day, get_data, timed
from collections import namedtuple
from networkx import Graph
from networkx.algorithms import shortest_path_length

class Point(namedtuple('Point', ['x', 'y'])):
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
  def __lt__(self, other):
    return self.y < other.y

graph = Graph()

today = day(2018, 20)

direction = {
  'N': Point( 0, -1),
  'E': Point( 1,  0),
  'S': Point( 0,  1),
  'W': Point(-1,  0)
}

def build_map(path_regex):
  pos = starts = { Point(0, 0) }
  stack = []
  ends = set()

  for current in path_regex:
    if current in 'NESW':
      graph.add_edges_from((p, p + direction[current]) for p in pos)
      pos = { p + direction[current] for p in pos }
    elif current == '(':
      stack += [(starts, ends)]
      starts, ends = pos, set()
    elif current == '|':
      ends |= pos
      pos = starts
    elif current == ')':
      pos |= ends
      starts, ends = stack.pop()

def main() -> None:
  path_regex = next(get_data(today))[1:-1]
  build_map(path_regex)

  path_lengths = shortest_path_length(graph, Point(0, 0)).values()

  print(f'{today} star 1 = {max(path_lengths)}')
  print(f'{today} star 2 = {sum(1 for length in path_lengths if length >= 1000)}')

if __name__ == '__main__':
  timed(main)
