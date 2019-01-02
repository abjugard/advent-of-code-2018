from santas_little_helpers import day, get_data, timed

today = day(2018, 18)

OPEN_GROUND = '.'
TREE = '|'
LUMBERYARD = '#'
TARGET = 1e9

def forest_generator(grid):
  maps = { str(grid): 0 }
  minute = 1
  while minute <= TARGET:
    grid = iterate_grid(grid)
    if str(grid) in maps:
      loop_size = minute - maps[str(grid)]
      multiplier = (TARGET - minute) // loop_size
      minute += loop_size * multiplier
    if minute == 10:
      yield value(grid)
    if minute == TARGET:
      yield value(grid)
    maps[str(grid)] = minute
    minute += 1

def value(grid):
  full = ''.join(grid)
  return full.count(TREE) * full.count(LUMBERYARD)

def iterate_grid(grid):
  grid_size = len(grid)
  return [''.join([iterate_cell(y, x, grid) for x in range(grid_size)]) \
                                            for y in range(grid_size)]

def iterate_cell(y, x, grid):
  trees, lumberyards = counts(y, x, grid)
  cell = grid[y][x]
  if cell == OPEN_GROUND and trees >= 3:
    cell = TREE
  elif cell == TREE and lumberyards >= 3:
    cell = LUMBERYARD
  elif cell == LUMBERYARD and (lumberyards < 1 or trees < 1):
    cell = OPEN_GROUND
  return cell

def counts(y, x, grid):
  ns = neighbours(y, x, grid)
  return ns.count(TREE), ns.count(LUMBERYARD)

def neighbours(y, x, grid):
  return [grid[y][x] for y, x in adjacent(y, x) \
                     if  0 <= y < len(grid) \
                     and 0 <= x < len(grid[0])]

def adjacent(y, x):
  return [(y-1, x-1), (y-1, x), (y-1, x+1), \
          (y,   x-1),           (y,   x+1), \
          (y+1, x-1), (y+1, x), (y+1, x+1)]
 
def main() -> None:
  initial_grid = list(get_data(today))

  it = forest_generator(initial_grid)
  print(f'{today} star 1 = {next(it)}')
  print(f'{today} star 2 = {next(it)}')

if __name__ == '__main__':
  timed(main)
