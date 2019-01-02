from santas_little_helpers import day, get_data, timed
from collections import deque

today = day(2018, 21)

def optimised_activation_system(r2_value):
  seen = set()
  last_r2 = None

  r2 = 0
  while True:
    r4 = r2 | 65536
    r2 = r2_value

    while True:
      r2 += r4 & 255
      r2 &= 16777215
      r2 *= 65899
      r2 &= 16777215
      if 256 > r4:
        if r2 in seen:
          yield last_r2
          return
        seen.add(r2)
        last_r2 = r2
        yield r2
        break
      else:
        r4 //= 256

def main() -> None:
  r2_value = int(list(get_data(today))[8].split()[1])

  it = optimised_activation_system(r2_value)
  print(f'{today} star 1 = {next(it)}')
  print(f'{today} star 2 = {deque(it, maxlen = 1).pop()}')

if __name__ == '__main__':
  timed(main)
