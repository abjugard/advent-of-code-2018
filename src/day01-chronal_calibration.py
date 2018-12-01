from santas_little_helpers import day, get_data, timed

today = day(2018, 1)

def find_first_repetition(numbers: [int]) -> int:
  current = 0
  seen = set([current])
  while True:
    for n in numbers:
      current += n
      if current in seen:
        return current
      seen.add(current)

def main() -> None:
  numbers = list(get_data(today, [('func', int)]))

  print(f'{today} star 1 = {sum(numbers)}')
  print(f'{today} star 2 = {find_first_repetition(numbers)}')

if __name__ == '__main__':
  timed(main)
