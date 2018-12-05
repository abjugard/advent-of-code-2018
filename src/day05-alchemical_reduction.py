from santas_little_helpers import day, get_data, timed

today = day(2018, 5)

alphabet = 'abcdefghijklmnopqrstuvwxyz'
pairs = [c + c.upper() for c in alphabet]
pairs += [c.upper() + c for c in alphabet]

def react(polymer):
  old_p = None
  while old_p != polymer:
    old_p = polymer
    for pair in pairs:
      polymer = polymer.replace(pair, '')
  return len(polymer), polymer

def shortest_polymer(polymer):
  return min([react(without(c, polymer))[0] for c in alphabet])

def without(c, polymer):
  return polymer.replace(c, '').replace(c.upper(), '')

def main() -> None:
  star1, first_run = react(next(get_data(today)))
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {shortest_polymer(first_run)}')

if __name__ == '__main__':
  timed(main)
