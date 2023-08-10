import csv
from ktail import init_automaton, simplify_automaton, draw_automaton


with open('./example_sequence/seq.csv', 'r') as f:
    reader = csv.DictReader(f)
    seq = []
    for li, line in enumerate(reader):
        if li == 0 or line['Host'] == 'main': continue
        seq.extend([s for s in line['Sequence'].split()])
        if li > 40: break

automaton = init_automaton(seq, k=5)
automaton = simplify_automaton(automaton)
draw_automaton(automaton)