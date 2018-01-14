#!/bin/python3
from time import sleep
import random
import collections
import string
import subprocess
import sys

tabs = {'ta': 2, 'tb': 3}
vars_ = None
vars_tabs = None

consts = {str(x): x for x in [0, 2, 4, 8, 16, 1, 3]}


Value = collections.namedtuple('Value', 'const, key')
ID = collections.namedtuple('ID', 'key')
def gen_value():
    r = random.randint(0,1)
    if r == 0: # vars/tabs
        return Value(const=False, key=random.choice(list(vars_tabs.keys())))
    elif r == 1: # consts
        return Value(const=True, key=random.choice(list(consts.keys())))

def execute_operation(t, operation, a, b):

    av = consts[a.key] if a.const else vars_tabs[a.key]
    bv = consts[b.key] if b.const else vars_tabs[b.key]
    r = 0

    if operation == '+':
        r = av + bv

    elif operation == '-':
        r = max(0, av - bv)

    elif operation == '/':
        r = (av // bv) if bv != 0 else 0

    elif operation == '%':
        r = (av % bv) if bv != 0 else 0

    elif operation == '*':
        r = av * bv

    vars_tabs[t.key] = r


def gen_expression():
    target = ID(key=random.choice(list(vars_tabs.keys())))
    a = gen_value()
    b = gen_value()

    #  operations = '%/*-+'
    operations = '%*-+'
    operation = random.choice(operations)
    func = lambda : execute_operation(target, operation, a, b)
    instructions = ["{} := {} {} {};".format(target.key,\
                                        a.key, operation, b.key)]
    return instructions, func

def execute_condition(cmp_, a, b, body):
    def call_inner_fs():
        for _, f in body:
            f()

    av = consts[a.key] if a.const else vars_tabs[a.key]
    bv = consts[b.key] if b.const else vars_tabs[b.key]

    if cmp_ == '=' and av == bv:
        call_inner_fs()
    elif cmp_ == '<>' and av != bv:
        call_inner_fs()
    elif cmp_ == '>' and av > bv:
        call_inner_fs()
    elif cmp_ == '<' and av < bv:
        call_inner_fs()
    elif cmp_ == '>=' and av >= bv:
        call_inner_fs()
    elif cmp_ == '<=' and av <= bv:
        call_inner_fs()


def gen_if():
    comparison = random.choice(['=', '<>', '>=', '<=', '<', '>'])
    a = gen_value()
    b = gen_value()
    body = gen_commands(2)
    instructions = ["IF {} {} {} THEN".format(a.key, comparison, b.key)]
    for cmd, f in body:
        instructions.extend([' ' + c for c in cmd])
    instructions.extend(["ENDIF"])
    return instructions, lambda : execute_condition(comparison, a, b, body)

def gen_for():
    a = random.randint(0, 5)
    b = random.randint(a, 10)
    i = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
    body = gen_commands(3)
    instructions = ["FOR {} FROM {} TO {} DO".format(
                i, a, b)]
    for cmd, _ in body:
        instructions.extend([' ' + c for c in cmd])
    instructions.extend(["ENDFOR"])
    def func():
        for i in range(a, b + 1):
            for _, f in body:
                f()

    return instructions, func


def random_choice(gens):
    r = random.random()
    tmp = 0
    for gen, p in gens.items():
        tmp += p
        if tmp > r:
            return gen

def gen_commands(size=5):
    cmds = []
    gens = {
            gen_expression: 0.85,
            gen_if: .1,
            gen_for: .05,
            }
    for _ in range(size):
        cmds.append(random_choice(gens)())
    return cmds

def run():
    cmds = gen_commands()
    code = ['VAR']
    code += ['  ' + ' '.join(vars_.keys()) + ' ' + ' '.join(['{}[{}]'.format(t, size) for t, size in tabs.items()])]
    code += ['BEGIN']
    code += ['\n'.join("  {} := {};".format(k, v) for k, v in vars_tabs.items())]
    code += ['\n'.join(['  ' + v for package, _ in cmds for v in package])]
    code += ['\n'.join(['  WRITE {};'.format(k) for k in sorted(vars_.keys())])]
    code += ['END']
    for _, f in cmds:
        f()
    code += ['([{}])'.format(', '.join(
        [str(vars_tabs[v]) for v in sorted(vars_.keys())]
        ))]
    result = \
            [vars_tabs[v] for v in sorted(vars_.keys())]
    return '\n'.join(code), result

def test():
    global vars_tabs, vars_
    vars_tabs = {'{}[{}]'.format(k, i): random.randint(1,10)  for k, n in tabs.items() for i in range(n)}
    vars_ = {x: random.randint(3,15) for x in 'abcde'}
    vars_tabs.update(vars_)
    code, result = run()

    with open('/tmp/test.in', 'w+') as f:
        f.write(code)

    with open('/tmp/test.out', 'w+') as fout:
        subprocess.run(compi, input=code.encode(), stdout=fout)
    out_raw = subprocess.check_output([interpreter, '/tmp/test.out']).decode('UTF-8')
    out = [int(line.split('>')[1].strip())
            for line in out_raw.split('\n')
            if len(line.split('>')) > 1]
    general_result = True
    for i, line in enumerate(out):
            general_result &= (line == result[i])
    return general_result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("{} [compiler path] [interpreter path]".format(sys.argv[0]))
        exit(1)
    else:
        compi, interpreter = sys.argv[1], sys.argv[2]

    counter = 0
    while(test()):
        counter += 1
        if counter % 100 == 0:
            print(counter, ' tests done')
    print(counter)
