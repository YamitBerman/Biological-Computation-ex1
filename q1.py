import networkx as nx


def create_file(msg1):
    file = open('output.txt', "w")
    file.write('')     # overwrite any existing content
    file.close()
    file = open('output.txt', "a")
    file.write(msg1)
    file.close()


# this function checks if all the vertices are connected in the graph
def all_vertices_connected(graph, size):
    vertices = []
    for edge in graph.edges:
        if not edge[0] in vertices:
            vertices.append(edge[0])
        if not edge[1] in vertices:
            vertices.append(edge[1])
        if len(vertices) == size:
            return True
    return False


# this function gets a graph and each time removes an edge if and checks if its a valid sub graph
def delete_edge(graph, size, sub_graphs):
    test = graph.copy()
    for edge in graph.edges:
        test.remove_edge(edge[0], edge[1])
        if all_vertices_connected(test, size):
            if test not in sub_graphs:
                sub_graphs.append(test.copy())
            delete_edge(test, size, sub_graphs)
        test = graph.copy()


def build_graphs(size):
    sub_graphs = []
    graph = nx.DiGraph()
    graph.add_nodes_from([1, size])
    # create a complete directed graph with all edges possible
    for i in range(1, size+1):
        for j in range(1, size+1):
            if i == j:
                continue
            graph.add_edge(i, j)
    sub_graphs.append(graph)
    delete_edge(graph.copy(), size, sub_graphs)
    # now we have all sub graphs possible and we need to remove the isomorphic graphs
    count = len(sub_graphs)
    for i in range(len(sub_graphs)):
        if i == count:
            break
        j = i+1
        while j != count:
            if nx.is_isomorphic(sub_graphs[i], sub_graphs[j]):
                sub_graphs.remove(sub_graphs[j])
                j -= 1
                count -= 1
            j += 1
    txt = 'n='+str(size)+'\ncount='+str(len(sub_graphs))
    count = 1
    for graphs in sub_graphs:
        txt = txt+'\n'+'#'+str(count)
        for edge in graphs.edges:
            txt = txt + '\n' + str(edge[0]) + ' ' + str(edge[1])
        count += 1
    return txt


if __name__ == '__main__':
    print('Hello! this programs generates all connected sub-graphs of size of your choosing')
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
    if n == 0:
        msg = 'n=0\ncount=0'
    elif n == 1:
        msg = 'n=1\ncount=0'
    else:
        # generates all connected sub-graphs
        msg = build_graphs(n)
    create_file(msg)
    print(msg)
