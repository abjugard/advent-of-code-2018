from santas_little_helpers import day, get_data, timed

today = day(2018, 19)

pc_reg = 0
regs = []

# Meta
def _ip(a):
  global pc_reg
  pc_reg = a

# Math
def addr(a, b, c): regs[c] = regs[a] + regs[b]
def addi(a, b, c): regs[c] = regs[a] + b

def mulr(a, b, c): regs[c] = regs[a] * regs[b]
def muli(a, b, c): regs[c] = regs[a] * b

# Bit-operations
def banr(a, b, c): regs[c] = regs[a] & regs[b]
def bani(a, b, c): regs[c] = regs[a] & b

def borr(a, b, c): regs[c] = regs[a] | regs[b]
def bori(a, b, c): regs[c] = regs[a] | b

# Assignment
def setr(a, _, c): regs[c] = regs[a]
def seti(a, _, c): regs[c] = a

# Logical operations
def gtir(a, b, c): regs[c] = 1 if a       > regs[b] else 0
def gtri(a, b, c): regs[c] = 1 if regs[a] > b       else 0
def gtrr(a, b, c): regs[c] = 1 if regs[a] > regs[b] else 0

def eqir(a, b, c): regs[c] = 1 if a       == regs[b] else 0
def eqri(a, b, c): regs[c] = 1 if regs[a] == b       else 0
def eqrr(a, b, c): regs[c] = 1 if regs[a] == regs[b] else 0

cpu = {
  '_ip': _ip,
  'addr': addr, 'addi': addi,
  'mulr': mulr, 'muli': muli,
  'banr': banr, 'bani': bani,
  'borr': borr, 'bori': bori,
  'setr': setr, 'seti': seti,
  'gtir': gtir, 'gtri': gtri, 'gtrr': gtrr,
  'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr
}

def run(header, sum_of_factors, reg_0 = 0):
  global pc_reg, regs
  pc_reg = 0
  regs = [0] * 6
  regs[0] = reg_0

  instr, args = header
  instr(*args)

  while 0 <= regs[pc_reg] < len(sum_of_factors):
    instr, args = sum_of_factors[regs[pc_reg]]
    instr(*args)
    regs[pc_reg] += 1
    
    if regs[pc_reg] == 1:
      return sum([n for n in range(1, regs[1] + 1) if regs[1] % n == 0])
  return regs[0]

def main() -> None:
  header, *sum_of_factors = list(get_data(today, [('replace', ('#', '_')), ('asmbunny', cpu)]))

  print(f'{today} star 1 = {run(header, sum_of_factors)}')
  print(f'{today} star 2 = {run(header, sum_of_factors, 1)}')

if __name__ == '__main__':
  timed(main)
