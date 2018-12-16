from santas_little_helpers import day, get_data, timed

today = day(2018, 16)

regs = []

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
  'addr': addr, 'addi': addi,
  'mulr': mulr, 'muli': muli,
  'banr': banr, 'bani': bani,
  'borr': borr, 'bori': bori,
  'setr': setr, 'seti': seti,
  'gtir': gtir, 'gtri': gtri, 'gtrr': gtrr,
  'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr
}

def execute(program, instrs):
  global regs
  regs = [0] * 4
  for instr, args in program:
    instrs[instr](*args)
  return regs[0]

def compile_program(source_code, opcode_table):
  return [(opcode_table[opcode], args) for opcode, *args in source_code]

def test_instructions(pre, args, post, instrs):
  global regs
  matches = set()
  for instr in instrs:
    regs = pre[::]
    instrs[instr](*args)
    if post == regs:
      matches.add(instr)
  return matches

def reverse_engineer(test_data, cpu):
  mappings = { i: set(cpu.keys()) for i in range(16) }
  count = 0
  for pre, op, post in test_data:
    opcode, *args = op
    possible_instructions = test_instructions(pre, args, post, cpu)
    if len(possible_instructions) >= 3:
      count += 1
    mappings[opcode] &= possible_instructions

  first = lambda inp: next(iter(inp))
  while any([len(mappings[opcode]) > 1 for opcode in mappings]):
    certain = set(first(ins) for ins in mappings.values() if len(ins) == 1)
    for opcode in mappings:
      if len(mappings[opcode]) == 1:
        continue
      mappings[opcode] -= certain

  return count, {op: instrs.pop() for op, instrs in mappings.items()}

def parse_input(inp):
  pre, op, post = [], [], []
  for line in inp:
    if line.startswith('Before'):
      pre += [ eval(line[8:]) ]
    elif line.startswith('After'):
      post += [ eval(line[8:]) ]
    elif len(line) > 3:
      op += [ tuple(map(int, line.split(' '))) ]
  return [(pre[i], op[i], post[i]) for i in range(len(pre))], op[len(pre):]

def main() -> None:
  test_data, source_code = parse_input(list(get_data(today)))

  star1, opcode_table = reverse_engineer(test_data, cpu)
  program = compile_program(source_code, opcode_table)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {execute(program, cpu)}')

if __name__ == '__main__':
  timed(main)
