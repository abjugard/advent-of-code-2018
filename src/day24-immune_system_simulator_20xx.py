from santas_little_helpers import day, get_data, timed
from operator import attrgetter as attr
import re

r = re.compile(r'(?P<units>\d*) units each with ' \
             + r'(?P<hp>\d*) hit points (?:\(' \
             + r'(?P<modifiers>[^\)]*)\) |)with an attack that does ' \
             + r'(?P<dmg>\d*) ' \
             + r'(?P<dmgtype>\w*) damage at initiative ' \
             + r'(?P<initiative>\d*)')

today = day(2018, 24)

active_team = None

teams = {
  'immune_system': [],
  'infection': []
}

original_input = []

def parse_modifiers(modifiers):
  if not modifiers:
    return [], []
  modifiers = sorted(modifiers.split('; '))
  if len(modifiers) < 2:
    if modifiers[0].startswith('w'):
      modifiers.insert(0, [])
    else:
      modifiers.append([])
  immunities, weaknesses = modifiers
  if immunities:
    immunities = immunities[10:].split(', ')
  if weaknesses:
    weaknesses = weaknesses[8:].split(', ')
  return immunities, weaknesses

class Squad(object):
  def __init__(self, m, team, boost):
    self.team = team
    self.units = int(m.group('units'))
    self.hp = int(m.group('hp'))
    self.immunities, self.weaknesses = parse_modifiers(m.group('modifiers'))
    self.dmg = int(m.group('dmg')) + (boost if team == 'immune_system' else 0)
    self.dmgtype = m.group('dmgtype')
    self.initiative = int(m.group('initiative'))

  def copy(self):
    return Squad(self.units, self.hp, self.immunities, self.weaknesses, self.dmg, self.dmgtype, self.initiative)

  def __repr__(self):
    return f'{self.team}: {self.units}u = {self.effective_power} ({self.dmgtype}) dmg, i={self.initiative}, hp={self.hp}, im:{self.immunities}, wk:{self.weaknesses}'
  def __lt__(self, other):
    return (self.effective_power, self.initiative) < (other.effective_power, other.initiative)

  def attack(self, other, simulate = False):
    if self.dmgtype in other.immunities:
      return 0
    dmg = self.effective_power
    if self.dmgtype in other.weaknesses:
      dmg *= 2
    if not simulate:
      other.take_damage(dmg)
    return dmg

  def take_damage(self, dmg):
    units_lost = dmg // self.hp
    if self.units > units_lost:
      self.units -= units_lost
    else:
      self.units = 0

  @property
  def effective_power(self):
    return self.units * self.dmg

def total_units():
  return sum(squad.units for team in teams for squad in teams[team])

def run():
  while len(teams['immune_system']) > 0 and len(teams['infection']) > 0:
    fights = {}
    unit_count = total_units()
    for team in teams:
      enemies = teams['immune_system'] if team == 'infection' else teams['infection']
      for attacker in sorted(teams[team], reverse=True):
        if attacker.units == 0:
          continue
        targets = sorted([(attacker.attack(enemy, simulate=True), enemy) for enemy in enemies if enemy not in fights.values() and enemy.units > 0], reverse=True)
        if len(targets) > 0 and targets[0][0] > 0:
          fights[attacker] = targets[0][1]
    for attacker in sorted(fights.keys(), key=attr('initiative'), reverse=True):
      if attacker.units > 0:
        attacker.attack(fights[attacker])
    for team in teams:
      to_del = []
      for i, squad in enumerate(teams[team]):
        if squad.units == 0:
          to_del += [i]
      for i in sorted(to_del, reverse=True):
        del teams[team][i]
    if total_units() == unit_count:
      break
  return len(teams['infection']) == 0

def parse(line, boost):
  global active_team
  if line.startswith('I'):
    active_team = 'immune_system' if line.startswith('Immune') else 'infection'
  elif line != '':
    m = r.match(line)
    teams[active_team].append(Squad(m, active_team, boost))

def reset(boost=0):
  for team in teams:
    teams[team].clear()
  for line in original_input:
    parse(line, boost)

def main() -> None:
  original_input.extend(list(get_data(today)))

  reset()
  infection_eliminated = run()
  print(f'{today} star 1 = {total_units()}')
  boost = 1
  while not infection_eliminated:
    reset(boost)
    infection_eliminated = run()
    boost += 1
  print(f'{today} star 2 = {total_units()}')

if __name__ == '__main__':
  timed(main)
