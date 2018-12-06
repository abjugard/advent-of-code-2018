import json, re, time, importlib, sys
from bs4 import BeautifulSoup
from datetime import date, datetime
from pathlib import Path
from requests import request
from requests import codes as status_codes
from typing import Callable, Iterator

base_ops = [('replace', (r'\n', ''))]

aoc_root = Path('../')
aoc_data = aoc_root / 'data'

with (aoc_root / 'config.json').open('r') as f:
  config = json.load(f)

def day(year: int, theday: int) -> date:
  return date(year, 12, theday)

def format_line(line: str, ops: list):
  for op, args in ops:
    if op == 'asmbunny':
      line = asmbunny_setup(args, line)
    elif op == 'func':
      line = args(line)
    elif op == 'map':
      line = list(map(args, line))
    elif op == 'replace':
      line = re.sub(args[0], args[1], line)
    elif op == 'split':
      line = line.split(args)
  return line

def asmbunny_setup(instrs: {}, line: str) -> (Callable, tuple):
  instr, *raw = line.strip().split(' ')
  if instr not in instrs:
    exit(1)
  args = ()
  for arg in raw:
    try:
      arg = int(arg)
    except:
      pass
    args += arg,
  if len(args) == 1:
    args = args[0]
  return instrs[instr], args

def get_data(today: date = date.today(), ops: list = base_ops) -> Iterator:
  if not aoc_data.exists():
    aoc_data.mkdir()

  def save_daily_input(today: date) -> None:
    url = f'https://adventofcode.com/{today.year}/day/{today.day}/input'
    res = request('GET', url, cookies=config)
    if res.status_code != status_codes.ok:
      print(f'Day {today.day} not available yet')
      sys.exit(0)
    with file_path.open('wb') as f:
      for chunk in res.iter_content(chunk_size=128):
        f.write(chunk)
        print(chunk.decode('utf-8'), end='')
      print()

  file_path = aoc_data / f'day{today.day:02}.txt'
  if not file_path.exists():
    print(f'Data for day {today.day} not available, downloading!')
    save_daily_input(today)
  with file_path.open() as f:
    for line in f.readlines():
      yield format_line(line, ops)

def submit_answer(today: date, answer: str, level: int = 1) -> None:
  url = f'https://adventofcode.com/{today.year}/day/{today.day}/answer'
  payload = {
    'level': level,
    'answer': answer
  }
  res = request('POST', url, cookies=config, data=payload)
  soup = BeautifulSoup(res.content, 'html.parser')
  for content in soup.find_all('article'):
    print(content.text)

def time_fmt(delta: float) -> (float, str):
  if delta > 1e9:
    return 1e9, 'seconds'
  elif delta > 1e6:
    return 1e6, 'ms'
  elif delta > 1e3:
    return 1e3, 'µs'
  return 1, 'ns'

def timed(func: Callable) -> None:
  start = time.time_ns()
  func()
  delta = time.time_ns()-start
  multiplier, unit = time_fmt(delta)
  print(f'--- {delta/multiplier:.2f} {unit} ---')

def run_all():
  for file in sorted(Path('.').glob('day*-*.py')):
    print(f'Running \'{file.name}\':')
    day = importlib.import_module(file.name[:-3])
    timed(day.main)
    print()

if __name__ == '__main__':
  timed(run_all)
