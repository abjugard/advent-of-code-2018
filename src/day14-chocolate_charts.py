from santas_little_helpers import day, get_data, timed

today = day(2018, 14)

def part1(it, recipes):
  for _ in range(recipes + 10):
    recipe_scores = next(it)
  return ''.join(map(str, recipe_scores[recipes:recipes + 10]))

def part2(it, token):
  while True:
    recipe_scores = next(it)
    offset = token_found(token, recipe_scores)
    if offset >= 0:
      return len(recipe_scores) - len(token) - offset

def recipe_generator():
  recipe_scores = [3, 7]
  elf1, elf2 = 0, 1
  while True:
    new_val = map(int, str(recipe_scores[elf1] + recipe_scores[elf2]))
    recipe_scores += new_val
    yield recipe_scores
    elf1 = (elf1 + recipe_scores[elf1] + 1) % len(recipe_scores)
    elf2 = (elf2 + recipe_scores[elf2] + 1) % len(recipe_scores)

def token_found(token, recipe_scores):
  if recipe_scores[-len(token):] == token:
    return 0
  if recipe_scores[-len(token)-1:-1] == token:
    return 1
  return -1

def main() -> None:
  recipes = next(get_data(today))

  it = recipe_generator()
  print(f'{today} star 1 = {part1(it, int(recipes))}')
  print(f'{today} star 2 = {part2(it, list(map(int, recipes)))}')

if __name__ == '__main__':
  timed(main)
