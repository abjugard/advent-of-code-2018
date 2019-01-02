from santas_little_helpers import day, get_data, timed
from collections import deque

today = day(2018, 15)

class Player(object):
  def __init__(self, y, x, team, elf_ap = 3):
    self.y = y
    self.x = x
    self.team = team
    self.hp = 200
    self.ap = elf_ap if team == 'E' else 3
    self.enemy_team = 'G' if self.team == 'E' else 'E'

  def __lt__(self, other):
    return self.position < other.position

  def attack(self, other):
    other.hp -= self.ap

  def _get_alive(self):
    return self.hp > 0

  def _get_position(self):
    return self.y, self.x

  def _set_position(self, pos):
    self.y, self.x = pos

  position = property(_get_position, _set_position)
  alive = property(_get_alive)

class Elf(Player):
  def __init__(self, y, x, ap = 3):
    Player.__init__(self, y, x, 'E', ap)

class Goblin(Player):
  def __init__(self, y, x):
    Player.__init__(self, y, x, 'G')

def find_target(player, enemies):
  targets = [enemy for pos in positions_around(player.position)
                   for enemy in enemies if enemy.position == pos and enemy.hp > 0]
  if len(targets) < 1:
    return None
  return min(targets, key = lambda player: player.hp)

def positions_around(pos, obstacles = {}, target = None):
  y, x = pos
  around = [(y-1, x), (y, x-1), (y, x+1), (y+1, x)]
  return [p for p in around if p not in obstacles or obstacles[p] == target]

def next_step(orig_pos, target, obstacles):
  previous = {new_pos: orig_pos for new_pos in positions_around(orig_pos, obstacles, target)}
  distance = {new_pos: 1 for new_pos in previous.keys()}
  to_visit = deque(previous.keys())
  closest = None
  while len(to_visit) > 0:
    current_pos = to_visit.popleft()
    if obstacles.get(current_pos) == target:
      closest = current_pos
      break
    for new_pos in positions_around(current_pos, obstacles, target):
      if new_pos not in previous:
        previous[new_pos] = current_pos
        distance[new_pos] = distance[current_pos] + 1
        to_visit.append(new_pos)
  if closest is None:
    return None, None
  current_pos = closest
  while previous.get(current_pos) != orig_pos:
    current_pos = previous[current_pos]
  return current_pos, distance[closest]

def move(player, obstacles):
  target = player.enemy_team
  new_pos, distance = next_step(player.position, target, obstacles)
  if new_pos is not None and distance >= 2:
    del obstacles[player.position]
    player.position = new_pos
    obstacles[new_pos] = player.team

def execute_round(goblins, elves, obstacles):
  for player in sorted(goblins + elves):
    if not player.alive:
      continue
    move(player, obstacles)
    enemy = find_target(player, goblins if player.team == 'E' else elves)
    if enemy:
      player.attack(enemy)
      if not enemy.alive:
        del obstacles[enemy.position]
  goblins = [goblin for goblin in goblins if goblin.alive]
  elves = [elf for elf in elves if elf.alive]
  return goblins, elves, obstacles

def game_loop(goblins, elves, obstacles):
  iterations = 0
  while len(goblins) > 0 and len(elves) > 0:
    goblins, elves, obstacles = execute_round(goblins, elves, obstacles)
    iterations += 1
  return (iterations - 1) * sum(player.hp for player in goblins + elves), elves

def setup_game(cavern, elf_ap = 3):
  goblins = []
  elves = []
  obstacles = {}
  for y in range(len(cavern)):
    for x in range(len(cavern[y])):
      symbol = cavern[y][x]
      if symbol is 'G':
        goblins += [Goblin(y, x)]
      if symbol is 'E':
        elves += [Elf(y, x, elf_ap)]
      if symbol in 'GE#':
        obstacles[(y, x)] = symbol
  return goblins, elves, obstacles

def game_runner(cavern):
  elf_ap = 3
  while True:
    goblins, elves, obstacles = setup_game(cavern, elf_ap)
    elf_count = len(elves)
    score, elves = game_loop(goblins, elves, obstacles)
    if elf_ap == 3:
      yield score
    if len(elves) == elf_count:
      yield score
    elf_ap += 1

def main() -> None:
  it = game_runner(list(get_data(today)))

  print(f'{today} star 1 = {next(it)}')
  print(f'{today} star 2 = {next(it)}')

if __name__ == '__main__':
  timed(main)
