from santas_little_helpers import day, get_data, timed

today = day(2018, 8)

def parse_child(data):
  child_count, meta_count, *data = data

  meta_total = 0
  child_metas = []
  for _ in range(child_count):
    child_sum, child_meta, data = parse_child(data)
    meta_total += child_sum
    child_metas += [child_meta]

  metadata, data = data[:meta_count], data[meta_count:]
  meta_total += sum(metadata)
  meta_val = sum(metadata) if child_count is 0 else \
             sum(child_metas[i - 1] for i in metadata
                                    if i > 0 and i <= len(child_metas))
  return meta_total, meta_val, data

def main() -> None:
  data = next(get_data(today, [('split', ' '), ('map', int)]))
  star1, star2, _ = parse_child(data)

  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')

if __name__ == '__main__':
  timed(main)
