from networkx import shortest_path, NetworkXNoPath
from pandas import read_pickle
from functools import cached_property
from itertools import combinations, product

class PalworldParentPathFinder:

    def __init__(self, *parents):
        self.parents = set(parents)
        self.path_finder = SingleParentBreeder(*self.parents) if len(self.parents) == 1 else MultiParentBreeder(*self.parents)
    
    def find_path(self, child):
        if len(self.parents) == 0:
            return []
        paths = self.path_finder.find_path(child)
        print('Sample path:')
        if paths:
            for gen in paths[0]:
                print(gen)
        return paths
    
    def all_possible_children(self):
        if len(self.parents) < 2: return self.parents
        all_gens = self.path_finder.all_generations()
        return all_gens[-1].parents

class PalworldParentCombo:
    
    breeding_matrix = read_pickle('data/breeding_matrix.pkl')

    def __init__(self, parent1, parent2):
        self.parents = frozenset((parent1, parent2))
        self.child = self.breeding_matrix.loc[parent1, parent2]
        self.score = 0
    
    def __repr__(self):
        if len(self.parents) > 1:
            return ' + '.join(self.parents) + f' = {self.child}'
        parent = list(self.parents)[0]
        return f'{parent} + {parent} = {self.child}'
    
    def __contains__(self, item):
        return item in self.parents
    
    def __hash__(self):
        return hash(self.parents)

    def __eq__(self, other):
        if isinstance(other, PalworldParentCombo):
            return self.parents == other.parents
        return super().__eq__(other)

    def __add__(self, other):
        child = PalworldParentCombo(self.child, other.child)
        child.parent_nodes = [self, other]
        if len(set(child.parent_nodes)) > 1:
            child.score = 1
        return child
    __radd__ = __add__

    @cached_property
    def parent_tree(self):
        if not hasattr(self, 'parent_nodes'):
            return [set()]
        parent1, parent2 = self.parent_nodes
        tree = [tree1 | tree2 for tree1, tree2 in zip(parent1.parent_tree, parent2.parent_tree)] + [set([self])]
        return tree
    
    def __iter__(self):
        path = [[node for node in nodes if len(node.parents) > 1] for nodes in self.parent_tree][1:]
        for node in path:
            yield node

    @cached_property
    def path_score(self):
        score = sum([sum(node.score for node in sets) for sets in self.parent_tree])
        return score

class PalworldFamilyGeneration:
    
    def __init__(self, parent_nodes, child_nodes, min_scores=None):
        if min_scores is None:
            min_scores = {list(node.parents)[0]: 0 for node in parent_nodes}
        self.parent_nodes = parent_nodes
        self.min_scores, self.child_nodes = self._trim_nodes(min_scores, child_nodes)
    
    @staticmethod
    def _trim_nodes(min_scores, nodes):
        nodes_dict = {}
        for node in nodes:
            child = node.child
            score = node.path_score
            if child not in min_scores:
                min_scores[child] = score
            min_score = min_scores[child]
            if score == min_score:
                if child in nodes_dict:
                    nodes_dict[child].append(node)
                else:
                    nodes_dict[child] = [node]
            elif score < min_score:
                min_scores[child] = score
                nodes_dict[child] = [node]
        nodes = list(set(sum(nodes_dict.values(), start=[])))
        return min_scores, nodes
    
    def __repr__(self):
        return f'Parents: {len(self.parents)}, Children: {len(self.children)}'
    
    @property
    def parents(self):
        return set(combo.child for combo in self.parent_nodes)
    
    @property
    def children(self):
        return set(combo.child for combo in self.child_nodes if combo.child not in self.parents)
    
    def next_parent_nodes(self):
        parent_nodes = [node + node for node in self.child_nodes]
        new_combo_children = set(combo.child for combo in self.child_nodes)
        parent_nodes += [node + node for node in self.parent_nodes if node.child not in new_combo_children]
        return parent_nodes
    
    def next_child_nodes(self):
        child_nodes = [parent1 + parent2 for parent1, parent2 in combinations(self.child_nodes, 2)]
        new_child_nodes = [node for node in self.child_nodes if node.child in self.children]
        child_nodes += [parent1 + parent2 for parent1, parent2 in product(new_child_nodes, self.parent_nodes)]
        child_nodes = [node for node in child_nodes if node.child not in node.parents]
        return child_nodes
    
    def next_gen(self):
        return PalworldFamilyGeneration(self.next_parent_nodes(), self.next_child_nodes(), self.min_scores.copy())
    
    def generate_all(self):
        next = self
        while next.children:
            yield next
            next = next.next_gen()
        yield next
    
    def generate_until(self, child):
        next = self
        while next.children and (child not in (next.parents | next.children)):
            yield next
            next = next.next_gen()
        yield next

class MultiParentBreeder:

    def __init__(self, *parents):
        self.parents = set(parents)

    def _make_gen0(self, parents):
        root_nodes = [PalworldParentCombo(parent, parent) for parent in parents]

        parent_nodes = [node + node for node in root_nodes]
        child_nodes = [parent1 + parent2 for parent1, parent2 in combinations(root_nodes, 2)]
        child_nodes = [node for node in child_nodes if node.child not in node.parents]

        gen0 = PalworldFamilyGeneration(parent_nodes, child_nodes)
        return gen0

    def all_generations(self):
        gen0 = self._make_gen0(self.parents)
        gens = [gen for gen in gen0.generate_all()]
        return gens

    def find_path(self, child):
        gen0 = self._make_gen0(self.parents)
        gens = [gen for gen in gen0.generate_until(child)]
        if child not in gens[-1].children:
            return [], gens
        
        paths = [node for node in gens[-1].child_nodes if node.child == child]
        print(f'Found {len(paths)} path(s) in {len(gens)} gen(s) with score {paths[0].path_score if len(paths) > 0 else None}')
        min_score_path = paths[0].path_score
        gen_diff = min_score_path - len(gens)
        found_new = False
        
        new_gens = []
        for i in range(gen_diff):
            new_gen = gens[-1].next_gen()
            if not new_gen.children:
                break
            new_gens.append(new_gen)
            sample_paths = [node for node in new_gen.child_nodes if node.child == child]
            if sample_paths:
                sample_score_path = sample_paths[0].path_score

                if sample_score_path == min_score_path:
                    paths += sample_paths
                    found_new = True
                elif sample_score_path < min_score_path:
                    paths = sample_paths
                    found_new = True
                
        if found_new:
            gens += new_gens
            print(f'Updated to {len(paths)} path(s) in {len(gens)} gen(s) with length {paths[0].path_score if len(paths) > 0 else None}')
        self.gens = gens
        return paths

class SingleParentBreeder:

    breeding_matrix = read_pickle('data/breeding_matrix.pkl')
    breeding_graph = read_pickle('data/breeding_graph.pkl')

    pals = breeding_matrix.index
    pal_combos = breeding_graph.nodes

    def __init__(self, *parents):
        self.parents = set(parents)
    
    def _get_combos(self, pal, exception=None):
        if exception:
            return [pal_combo for pal_combo in self.pal_combos if pal in pal_combo and exception not in pal_combo]
        return [pal_combo for pal_combo in self.pal_combos if pal in pal_combo]

    def _get_subgraph_excluding(self, pal):
        nodes = [pal_combo for pal_combo in self.pal_combos if pal not in pal_combo]
        nodes.append(PalworldParentCombo(pal, pal))
        return self.breeding_graph.subgraph(nodes)
    
    def _get_shortest_path(self, breeding_graph, source, target):
        try:
            return shortest_path(breeding_graph, source=source, target=target)
        except NetworkXNoPath:
            return []
    
    def _get_paths(self, parent, child):
        sources = self._get_combos(parent, exception=child)
        target = PalworldParentCombo(child, child)
        paths = [self._get_shortest_path(self._get_subgraph_excluding(child), source, target) for source in sources]
        return paths
    
    def find_path(self, child):
        paths = self._get_paths(*self.parents, child)
        path_lengths = [len(path) for path in paths if len(path) > 0]
        if len(path_lengths) == 0:
            print('Found 0 paths.')
            return []
        else:
            min_path_length = min(path_lengths)
        min_paths = [path[:-1] for path in paths if len(path) == min_path_length]
        print(f'Found {len(min_paths)} path(s) with length {min_path_length-1}')
        return min_paths

if __name__ == '__main__':
    import sys

    parents = sys.argv[1:-1]
    child = sys.argv[-1]
    path_finder = PalworldParentPathFinder(*parents)
    paths = path_finder.find_path(child)