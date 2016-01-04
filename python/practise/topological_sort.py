def topological_sort(edge_list):
    edge_set = set([tuple(i) for i in edge_list])

    node_list = []

    node_from, node_to = zip(*edge_set)

    source_list = list(set(node_from) - set(node_to))

    while source_list:
        node = source_list.pop(0)
        node_list.append(node)

        from_selection = [e for e in edge_set if e[0] == node]
        for edge in from_selection:
            node_2 = edge[1]
            edge_set.discard(edge)

            edge_new_list = [e for e in edge_set if e[1] == node_2]
            if not edge_new_list:
                source_list.append(node_2)

    if edge_set:
        print 'graph has cycles'

    else:
        for i in node_list:
            print i

u = [
    ['a', 'b'], # a -> b, etc.
    ['a', 'c'],
    ['b', 'e'],
    ['c', 'd'],
    ['b', 'd'],
    ['e', 'f'],
    ['c', 'f'],
]

topological_sort(u)