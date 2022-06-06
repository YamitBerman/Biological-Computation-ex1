import networkx as nx
from itertools import combinations


def create_file(msg1):
    file = open('output_2.txt', "w")
    file.write('')     # overwrite any existing content
    file.close()
    file = open('output_2.txt', "a")
    file.write(msg1)
    file.close()


# this function checks if all the vertices are connected in the graph
def all_vertices_connected(graph_n, size):
    vertices = []
    for i in graph_n.edges:
        if not i[0] in vertices:
            vertices.append(i[0])
        if not i[1] in vertices:
            vertices.append(i[1])
        if len(vertices) == size:
            return True
    return False


# this function gets a graph and each time removes an edge if and checks if its a valid sub graph
def delete_edge(graph_n, size, sub_graphs_n):
    test = graph_n.copy()
    for i in graph_n.edges:
        test.remove_edge(i[0], i[1])
        if all_vertices_connected(test, size):
            if test not in sub_graphs_n:
                sub_graphs_n.append(test.copy())
            delete_edge(test, size, sub_graphs_n)
        test = graph_n.copy()


def build_graphs(size, sub_graphs_n):
    graph_n = nx.DiGraph()
    graph_n.add_nodes_from([1, size])
    # create a complete directed graph with all edges possible
    for i in range(1, size+1):
        for j in range(1, size+1):
            if i == j:
                continue
            graph_n.add_edge(i, j)
    sub_graphs_n.append(graph_n)
    delete_edge(graph_n.copy(), size, sub_graphs_n)
    # now we have all sub graphs possible and we need to remove the isomorphic graphs
    count_ = len(sub_graphs_n)
    for i in range(len(sub_graphs_n)):
        if i == count_:
            break
        j = i+1
        while j != count_:
            if nx.is_isomorphic(sub_graphs_n[i], sub_graphs_n[j]):
                sub_graphs_n.remove(sub_graphs_n[j])
                j -= 1
                count_ -= 1
            j += 1


def find_sub_graphs_of_size_n(the_graph, size, sub_graphs_n, num_of_motif):
    test = the_graph.copy()
    # generate a combinations of n num of nodes
    node_list = list(combinations(range(1, len(test.nodes)+1), size))
    for nodes in node_list:
        nbunch = list(nodes)
        sub = test.subgraph(nbunch)
        # if graph is connected
        if all_vertices_connected(sub, size):
            count_ = 0
            for motif in sub_graphs_n:
                if nx.is_isomorphic(motif, sub):
                    num_of_motif[count_] += 1
                    break
                count_ += 1


if __name__ == '__main__':
    print('please enter a graph')
    input_ = '0'
    g = ''
    while input_ != '':
        input_ = input()
        if input_ != '':
            g = g + input_ + '\n'
    print('please enter the size of the sub-graphs')
    done = False
    n = ''
    # get a valid size from user
    while not done:
        n = input()
        if not n.isdigit():
            print('please enter a positive integer')
        else:
            n = int(n)
            if n < 0:
                print('please enter a positive integer')
            else:
                done = True
    edges = g.split("\n")
    graph = nx.DiGraph()
    for edge in edges:
        if edge == '':
            break
        graph.add_node(int(edge[0]))
        graph.add_node(int(edge[2]))
        graph.add_edge(int(edge[0]), int(edge[2]))
    sub_graphs = []
    build_graphs(n, sub_graphs)
    motif_count = [0] * len(sub_graphs)
    find_sub_graphs_of_size_n(graph, n, sub_graphs, motif_count)
    txt = 'n=' + str(n) + '\ncount=' + str(len(sub_graphs))
    count = 1
    for graphs in sub_graphs:
        txt = txt + '\n' + '#' + str(count)
        txt = txt + "\ncount=" + str(motif_count[count - 1])
        for e in graphs.edges:
            txt = txt + '\n' + str(e[0]) + ' ' + str(e[1])
        count += 1
    create_file(txt)
    print(txt)
