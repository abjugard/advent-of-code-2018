from santas_little_helpers import day, get_data, timed

today = day(2018, 12)

def garden_generator(state, rules):
  offset = 3
  state = '.' * offset + state + '.' * 2
  generation = 0
  while True:
    generation += 1
    new_state = state
    for i in range(2, len(state)-2):
      to_consider = state[i-2:i+3]
      if to_consider in rules:
        new_state = new_state[:i] + rules[to_consider] + new_state[i+1:]
    if generation == 20:
      yield pot_count(-offset, new_state)
    if new_state.strip('.') == state.strip('.'):
      yield pot_count(50000000000 - (generation-1) - offset, state)
      break
    state = new_state
    if '#' in state[-3:]:
      state = state + '.' * 2
    if '#' in state[:4]:
      state = '.' * 3 + state
      offset += 3

def pot_count(offset, state):
  return sum(offset+index for index, pot in enumerate(state) if pot == '#')

def main() -> None:
  data = list(get_data(today))
  initial_state, _, *rules = data
  initial_state = initial_state[15:]
  rules = {rule[:5]: rule[-1] for rule in rules}

  it = garden_generator(initial_state, rules)
  print(f'{today} star 1 = {next(it)}')
  print(f'{today} star 2 = {next(it)}')

if __name__ == '__main__':
  timed(main)
