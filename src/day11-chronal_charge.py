from santas_little_helpers import day, get_data, timed
import math

today = day(2018, 11)

def measure_grid_power(grid, grid_size=3):
  square_parts = 300-grid_size
  for y in range(square_parts):
    for x in range(square_parts):
      yield square_power_level(grid, x, y, grid_size)

def square_power_level(grid, x, y, grid_size):
  total = 0
  for yp in range(grid_size):
    for xp in range(grid_size):
      total += grid[yp+y][xp+x]
  return total, (x+1, y+1, grid_size)

def cell_power_level(x, y, serial_number):
  raw = str(((x+10)*y+serial_number)*(x+10))
  power = 0 if len(raw) < 3 else int(raw[-3])
  return power - 5

def variable_grid_size(grid):
  power_levels = []
  for i in range(1, 300):
    new_reading = max(measure_grid_power(grid, grid_size=i))
    power_levels += [new_reading]
    if new_reading < max(power_levels):
      return fmt(max(power_levels), include_grid_size = True)

def fmt(reading, include_grid_size = False):
  _, (x, y, grid_size) = reading
  result = f'{x},{y}'
  if include_grid_size:
    result += f',{grid_size}'
  return result

def main() -> None:
  serial_number = int(next(get_data(today)))
  grid = [[cell_power_level(x, y, serial_number) for x in range(1, 301)] for y in range(1, 301)]

  print(f'{today} star 1 = {fmt(max(measure_grid_power(grid)))}')
  print(f'{today} star 2 = {variable_grid_size(grid)}')

if __name__ == '__main__':
  timed(main)
