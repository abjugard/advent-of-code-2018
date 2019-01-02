from santas_little_helpers import day, get_data, timed
from collections import defaultdict, namedtuple
from itertools import product
import re, sys

sys.setrecursionlimit(5000)

class Point(namedtuple('Point', ['x', 'y'])):
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
  def __lt__(self, other):
    return self.y < other.y

  @property
  def left(self):
    return self + Point(-1, 0)
  @property
  def down(self):
    return self + Point(0, 1)
  @property
  def right(self):
    return self + Point(1, 0)

base = Point(0, 0)
LEFT, DOWN, RIGHT = base.left, base.down, base.right

today = day(2018, 17)

rl = re.compile(r'([xy])=(\d+)')
rr = re.compile(r'([xy])=(\d+)..(\d+)')

settled, flowing = set(), set()
ymax, ymin = 0, 0
clay = defaultdict(bool)

def flow(current, direction = DOWN):
  if current in flowing:
    return True
  flowing.add(current)

  if not clay[current.down]:
    if current.down not in flowing and 1 <= current.down.y <= ymax:
      flow(current.down)
    if current.down not in settled:
      return False

  right_filled = clay[current.right] or flow(current.right, RIGHT)
  left_filled = clay[current.left] or flow(current.left, LEFT)

  if direction == DOWN and right_filled and left_filled:
    settle_flowing(current.right, RIGHT)
    settle_flowing(current.left, LEFT)
    settled.add(current)

  return direction == RIGHT and right_filled \
      or direction == LEFT  and left_filled

def settle_flowing(position, direction):
  while position in flowing:
    settled.add(position)
    position += direction

def parse(line):
  l, r = line.split(', ')
  ml, mr = rl.match(l), rr.match(r)
  al = [int(ml.group(2))]
  ar = [p for p in range(int(mr.group(2)), int(mr.group(3)) + 1)]
  ys = al if ml.group(1) == 'y' else ar
  xs = al if ml.group(1) == 'x' else ar
  ps = list(product(xs, ys))
  return [Point(x, y) for x, y in ps]

def main() -> None:
  global ymax, ymin
  inp = list(get_data(today, [('func', parse)]))
  for p in [p for ps in inp for p in ps]:
    clay[p] = True

  ymax = max(clay).y
  ymin = min(clay).y

  flow(Point(500, 0))

  print(f'{today} star 1 = {len([p for p in settled | flowing if ymin <= p.y <= ymax])}')
  print(f'{today} star 2 = {len([p for p in settled if ymin <= p.y <= ymax])}')

if __name__ == '__main__':
  timed(main)
