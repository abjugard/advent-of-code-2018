from santas_little_helpers import day, get_data, timed
from datetime import datetime
from collections import defaultdict
import re

today = day(2018, 4)
r = re.compile(r'\[[\d\-: ]*(?P<minute>\d{2})\] (?P<event>Guard #(?P<guardid>\d+)|w|f)')
guardid = ''

def find_lazy_guard(log_entries):
  times = []
  minutes_sleeping = {}
  active_guard = log_entries[0][1]
  for guardid, event, minute in log_entries:
    if guardid != active_guard:
      if active_guard not in minutes_sleeping:
        minutes_sleeping[active_guard] = defaultdict(int)
      handle_guard_times(times, minutes_sleeping[active_guard])
      active_guard = guardid
      times = []
    times += [(event, minute)]

  highest = None, 0
  for guard, minutes in minutes_sleeping.items():
    total = sum(minutes.values())
    if total > highest[1]:
      highest = guard, total

  most_slept = None, 0
  for minute, count in minutes_sleeping[highest[0]].items():
    if count > most_slept[1]:
      most_slept = minute, count
  return highest[0] * most_slept[0], minutes_sleeping

def handle_guard_times(times, minutes_sleeping):
  current_sleep_start = None
  for event, minute in times:
    if event == 'f':
      current_sleep_start = minute
    if event == 'w':
      for m in range(current_sleep_start, minute):
        minutes_sleeping[m] += 1

def find_consistently_lazy_guard(minutes_sleeping):
  most_slept = None, None, 0
  for guard, minutes in minutes_sleeping.items():
    for minute, count in minutes.items():
      if count > most_slept[2]:
        most_slept = guard, minute, count
  return most_slept[0] * most_slept[1]

def fmt(entry):
  global guardid
  m = r.match(entry)
  event = m.group('event')
  if m.group('guardid') is not None:
    guardid = m.group('guardid')
  return int(guardid), event, int(m.group('minute'))

def main() -> None:
  log_entries = [fmt(entry) for entry in sorted(list(get_data(today)))]

  star1, minutes_sleeping = find_lazy_guard(log_entries)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {find_consistently_lazy_guard(minutes_sleeping)}')

if __name__ == '__main__':
  timed(main)
