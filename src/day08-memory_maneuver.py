from santas_little_helpers import day, get_data, timed
from itertools import islice

today = day(2018, 8)

def parse_child(data):
  child_count, meta_count = next(data), next(data)
  if child_count == 0:
    return [sum(islice(data, meta_count))] * 2

  meta_total = meta_val = 0
  child_metas = []
  for _ in range(child_count):
    child_sum, child_meta = parse_child(data)
    meta_total += child_sum
    child_metas += [child_meta]

  for metadata in islice(data, meta_count):
    meta_total += metadata
    meta_val += child_metas[metadata - 1] \
      if metadata > 0 and metadata <= child_count else 0
  return meta_total, meta_val

def main() -> None:
  data = iter(next(get_data(today, [('split', ' '), ('map', int)])))
  star1, star2 = parse_child(data)

  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')

if __name__ == '__main__':
  timed(main)
