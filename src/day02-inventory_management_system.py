from santas_little_helpers import day, get_data, timed
from collections import defaultdict
from itertools import combinations

today = day(2018, 2)

def checksum(wordlist):
  repetitions = defaultdict(int)
  for word in wordlist:
    counts = get_counts(word)
    if 2 in counts:
      repetitions[2] += 1
    if 3 in counts:
      repetitions[3] += 1
  return repetitions[2] * repetitions[3]

def get_counts(word):
  charcount = defaultdict(int)
  for c in word:
    charcount[c] += 1
  return charcount.values()

def most_common_word(data):
  for w1, w2 in combinations(data, 2):
    if differs_by_one(w1, w2):
      return ''.join([c for c, w in zip(w1, w2) if c == w])

def differs_by_one(word1, word2):
  count = 0
  for c1, c2 in zip(word1, word2):
    if c1 != c2:
      count += 1
    if count > 1:
      return False
  return count == 1

def main() -> None:
  data = list(get_data(today))

  print(f'{today} star 1 = {checksum(data)}')
  print(f'{today} star 2 = {most_common_word(data)}')

if __name__ == '__main__':
  timed(main)
