"""
Implementation of the randomized graph contraction algorithm
used to find the minimal cut of a simple, unidirected graph.
The minimal cut is a way to cut a graph in two components,
where the number of edges that crosses from one component
to the other is minimized
"""
import math
import random
import copy

''' Read a text file containing a graph as a sequence of rows of numbers
where the first number of each row is a vertex, and the others
are the vertices connected to it.
Returns a list of all the edges in the graph as tuples with 2 vertices
and an unique identifier: (v1, v2, u_id), where v1 < v2.
'''
def create_edges_list(file_name):
    unique_id = 0
    edges = []
    edges_added = set()
    with open(file_name) as f:
        for line in f:
            if line == '\n':
                continue
            trimmed_line = line.strip()
            array_line = [int(n) for n in trimmed_line.split()]
            v1 = array_line[0]
            for v2 in array_line[1:]:
                pair = (v1, v2) if v1<v2 else (v2,v1)
                if pair in edges_added:
                    continue
                else:
                    edges_added.add(pair)
                edges.append((pair[0], pair[1], unique_id))
                unique_id += 1
    return edges

'''
Return the number of unique vertices
in a edges list
'''
def count_vertices(edges_list):
    vertex_set = set()
    for edge in edges_list:
        vertex_set.add(edge[0])
        vertex_set.add(edge[1])
    return len(vertex_set)

'''
Choose a random edge from the edge list
and merge the 2 vertices that are connected
by it.
'''
def merge_random_edge(edges_list):
    v1, v2, _ = random.choice(edges_list)
    v1, v2 = (v1, v2) if v1 < v2 else (v2, v1)
    for i in range(len(edges_list)):
        curr_edge = edges_list[i]
        # Mark edges connecting v1 to v2 (future self-loops) for removal
        # by defining its identifier as '-1'
        if (curr_edge[0], curr_edge[1]) == (v1, v2):
            edges_list[i] = (v1, v2, -1)
            continue
        # Transform edges connected to v2 ((v2, v3) or (v3, v2)) to be connected to v1,
        # by changing v2 to v1, always keeping v1 < v2
        if curr_edge[0] == v2:
            v3 = edges_list[i][1]
            u_id = edges_list[i][2]
            if v1 < v3:
                edges_list[i] = (v1, v3, u_id)
            else:
                edges_list[i] = (v3, v1, u_id)
        elif curr_edge[1] == v2:
            v3 = edges_list[i][0]
            u_id = edges_list[i][2]
            if v1 < v3:
                edges_list[i] = (v1, v3, u_id)
            else:
                edges_list[i] = (v3, v1, u_id)

    # Remove the edges marked for removal
    # by not copying them to a new list (O(n))
    edges_list = [edge for edge in edges_list if edge[2] != -1]
    return edges_list

'''
Receives a list of edges of a graph
and returns the edges connecting the
2 vertices that remain after the many
collapses
'''
def min_cut(original_edges_list, vertices_remaining):
    # To avoid rereading the file in the next calls to min_cut
    # to recreate the original edges_list,
    # don't modify it, but instead modify it copy
    edges_list = copy.deepcopy(original_edges_list)
    while vertices_remaining > 2:
        edges_list = merge_random_edge(edges_list)
        vertices_remaining -= 1

    # retrieve the original edges, from the edges that remained
    ids = set([edge[2] for edge in edges_list])
    final_edges = [edge for edge in original_edges_list if edge[2] in ids]
    return final_edges


# Reads the text file representing the graph
# and create the edges list
file_name = 'graph.txt'
original_edges_list = create_edges_list(file_name)

# Stores the minimal cut
# found until now
smaller_num_edges_min_cut = float('inf')
edges_of_min_cut = []

# To have a good probability of finding the correct minimal cut
# usually the algorithm is repeated n * (n-1) * log(n) times
number_of_vertices = count_vertices(original_edges_list)
number_of_runs = int(number_of_vertices * (number_of_vertices - 1) * math.log(number_of_vertices, 2))

# Runs the randomized algorithm many times
for k in range(1, number_of_vertices + 1):
    random.seed()
    edges_of_curr_min_cut = min_cut(original_edges_list, number_of_vertices)
    num_edges_of_curr_min_cut = len(edges_of_curr_min_cut)
    if num_edges_of_curr_min_cut < smaller_num_edges_min_cut:
        smaller_num_edges_min_cut = num_edges_of_curr_min_cut
        edges_of_min_cut = edges_of_curr_min_cut
    print()
    print(f'Minimal cut found until the ({k} of {number_of_runs}) iteration:', smaller_num_edges_min_cut)
print()
print(f'After {number_of_runs} iterations, the best estimation')
print(f'of the number of edges in the minimal cut is: {smaller_num_edges_min_cut}.')
print(f'The edges of the minimal cut are: {[(e[0], e[1]) for e in edges_of_min_cut]}')
