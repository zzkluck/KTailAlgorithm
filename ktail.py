from dataclasses import dataclass
from typing import Tuple, List, Dict, Iterable
from collections import defaultdict
from pyvis.network import Network

Element = str
Tail = Tuple[Element]


@dataclass
class State:
    id: int
    ktails: Dict[Tail, int]
    trans: Dict[Element, 'State']

    def edge_strength(self):
        res = defaultdict(int)
        for ktail, strength in self.ktails.items():
            res[ktail[0]] += strength
        return res

    def node_strength(self):
        return sum(v for _, v in self.ktails.items())

    def __repr__(self):
        es = self.edge_strength()
        trans_info = [(activate, next_node.id, es[activate]) for activate, next_node in self.trans.items()]
        return f"State(id={self.id}, ktail={self.ktails}, trans={trans_info}"


def generate_linear_automaton(seq: Iterable[Element], k: int = 5, start_index=0):
    seq = list(seq)
    states: List[State] = []
    for i, ele in enumerate(seq):
        ktail = seq[i:i + k]
        ktail = tuple(ktail + ['$'] * (k - len(ktail)))
        states.append(State(start_index + len(states), {ktail: 1}, {}))
        if i != 0: states[-2].trans[seq[i - 1]] = states[-1]
    states.append(State(start_index + len(states), {tuple(['$'] * k): 1}, {}))
    states[-2].trans[seq[-1]] = states[-1]
    return states


def init_automaton(seq: Iterable[Element], k: int = 5):
    linear = generate_linear_automaton(seq, k, start_index=1)
    end_state = State(0, {tuple(['<END>']): 1}, {})
    linear[-1].trans['$'] = end_state
    return [end_state, *linear]


def merge_state(i0: int, i1: int, fsa: List[State]) -> State:
    assert fsa[i0].id == i0 and fsa[i1].id == i1
    if i0 > i1: i0, i1 = i1, i0
    s0, s1 = fsa[i0], fsa[i1]
    s1.id = s0.id
    k0, k1 = s0.trans.keys(), s1.trans.keys()
    for activate in k1 - k0:
        s0.trans[activate] = s1.trans[activate]

    for activate in k0 & k1:
        if s0.trans[activate] != s1.trans[activate]:
            m0, m1 = s0.trans[activate].id, s1.trans[activate].id
            while fsa[m0].id != m0: m0 = fsa[m0].id
            while fsa[m1].id != m1: m1 = fsa[m1].id
            merge_state(m0, m1, fsa)

    for ktail, strength in s1.ktails.items():
        if ktail in s0.ktails:
            s0.ktails[ktail] += strength
        else:
            s0.ktails[ktail] = strength
    return s0


def merge_epoch(fsa: List[State]):
    mem: Dict[Tail, int] = {}
    for i, state in enumerate(fsa):
        if i != state.id: continue
        for activate, next_state in state.trans.items():
            state.trans[activate] = fsa[next_state.id]
        for ktail in state.ktails:
            if ktail not in mem:
                mem[ktail] = i
            else:
                merge_state(mem[ktail], i, fsa)
                return False
    return True


def simplify_automaton(fsa: List[State]):
    while not merge_epoch(fsa): pass
    fsa = [state for i, state in enumerate(fsa) if i == state.id]
    for i, state in enumerate(fsa):
        state.id = i
    return fsa


def draw_automaton(fsa: List[State]):
    # 创建一个空的有向图
    G = Network(directed=True)
    # 添加节点
    for state in fsa:
        G.add_node(f"S{state.id}", shape='circle', font={'size': 20, 'face': 'Arial'})

    # 添加边
    for state in fsa:
        edge_strength = state.edge_strength()
        self_loop = []
        self_loop_strength = 0
        for activate, next_state in state.trans.items():
            if next_state is state:
                self_loop.append(activate)
                self_loop_strength += edge_strength[activate]
            else:
                G.add_edge(f"S{state.id}", f"S{next_state.id}")
        if len(self_loop) != 0:
            G.add_edge(f"S{state.id}", f"S{state.id}")

    G.force_atlas_2based()
    G.show('graph.html', notebook=False)