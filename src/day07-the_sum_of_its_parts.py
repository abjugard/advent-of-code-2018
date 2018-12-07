from santas_little_helpers import day, get_data, timed, alphabet
from collections import defaultdict

today = day(2018, 7)

alphas = alphabet.upper()

def singlesledded(steps):
  completed = ''
  while len(completed) < len(steps):
    completed += possible_steps(steps, completed)[0]
  return completed

def multisledded(steps, workers = 5):
  available_at = defaultdict(list)
  in_progress = set()
  time_index = -1
  completed = []
  while len(completed) < len(steps):
    time_index += 1
    if time_index in available_at:
      now_available = available_at[time_index]
      workers += len(now_available)
      completed += sorted(now_available)
    if workers == 0:
      continue
    for step in possible_steps(steps, completed, in_progress):
      if workers > 0:
        in_progress.add(step)
        available_at[time_index + 61 + alphas.index(step)] += [step]
        workers -= 1
  return time_index

def possible_steps(steps, completed, in_progress = None):
  secondary = completed if in_progress is None else in_progress
  return sorted([step for step, required in steps.items()
                      if all([s in completed for s in required])
                      and step not in secondary])

def main() -> None:
  instructions = get_data(today, [('func', lambda l: (l[5], l[-13]))])

  steps = defaultdict(list)
  for required, before in sorted(instructions):
    steps[before] += [required]
    steps[required] += []

  print(f'{today} star 1 = {singlesledded(steps)}')
  print(f'{today} star 2 = {multisledded(steps)}')

if __name__ == '__main__':
  timed(main)
