import networkx as nx
import matplotlib.pyplot as plt
import os


OUTPUT_DIR = 'img'
INF_WEIGHT = 1000000
CURRENT_NODE_COLOR = (0, 1, 0)
VISITED_NODE_COLOR = (1, 0, 0)
NOT_VISITED_NODE_COLOR = (0, 1, 1)
NEAREST_NEIGHBOR_COLOR = (1, 1, 0)


EDGE_COLOR_NOT_IN_WAY = (0, 0, 0)
EDGE_COLOR_IN_WAY = (1, 0, 0)


def draw_graph(Graph, n_graph, pos, node_colors, edge_labels, good_edges = set()):

    _, ax = plt.subplots()

    # Добавляем номера узлов и их значения в виде текста на графике
    for node, (x, y) in zip(Graph.nodes(), pos.values()):
        value = Graph.nodes[node]['value']
        from_where = Graph.nodes[node]['from_where']
        ax.text(x, y, f"{node}\n{value}\n{from_where}", fontsize = 12, ha='center', va='center')


    # Рисуем граф

    edge_color = [EDGE_COLOR_IN_WAY if (u, v) in good_edges else EDGE_COLOR_NOT_IN_WAY for (u, v) in Graph.edges()]

    nx.draw(Graph, pos, with_labels = False, node_color = list(node_colors.values()), edge_color = edge_color, node_size = 800, font_size = 15, font_color = 'black', font_weight = 'bold')
    nx.draw_networkx_edge_labels(Graph, graph_pos, edge_labels = edge_labels, font_color='red')
    
    plt.title(f"graph{n_graph}")
    plt.savefig(os.path.join(OUTPUT_DIR, f"graph{n_graph}.png"), format='png', bbox_inches='tight')  # Сохранение в формате PNG

    plt.close()

def create_graph(seed, start_node_values, edges_with_weights):
    # Создаем пустой граф
    Graph = nx.DiGraph()

    # Добавляем узлы
    Graph.add_nodes_from(start_node_values.keys())


    # Задаем позиции узлов для визуализации
    graph_pos = nx.spring_layout(Graph, seed = seed)

    node_colors = {node: (0, 1, 1) for node in Graph.nodes()}

    #записываем в атрибут ноды ее значение
    for node, value in start_node_values.items():
        Graph.nodes[node]['value'] = value
        Graph.nodes[node]['from_where'] = -1

    # Добавляем веса на ребрах 
    Graph.add_weighted_edges_from(edges_with_weights)
    edge_labels = {(u, v): d['weight'] for u, v, d in Graph.edges(data=True)}
    

    return (Graph, graph_pos, node_colors, edge_labels)


def reset_graph(Graph, start_node_values):
    for node, value in start_node_values.items():
        Graph.nodes[node]['value'] = value
        Graph.nodes[node]['from_where'] = -1
        node_colors[node] = NOT_VISITED_NODE_COLOR




#локальная функция, нужная только для set_weight_to_neighbors
def set_neighbor_weight(Graph, node, neighbor, edge_labels, visited_nodes):
    if (node_colors[neighbor] in visited_nodes):
        return 

    neighbor_current_weight = Graph.nodes[neighbor]['value'] 
    weight_from_current_node =  max(Graph.nodes[node]['value'], edge_labels[(node, neighbor)])

    if (weight_from_current_node < neighbor_current_weight):
        Graph.nodes[neighbor]['value'] = weight_from_current_node
        Graph.nodes[neighbor]['from_where'] = node

    #return min(weight_from_current_node, neighbor_current_weight)             


#релаксация путей до соседних вершин
def set_weight_to_neighbors(Graph, node, edge_labels, nearest_neighbors, visited_nodes):

    
    nearest_neighbors |= set(Graph.neighbors(node))
    neighbors = list(Graph.neighbors(node))

    if (len(neighbors) == 0):
        return 

    '''min_weight = get_neighbor_weight(Graph, node, neighbors[0], edge_labels)
    best_neighbor = neighbors[0]'''
    #node_colors[neighbors[0]] = NEAREST_NEIGHBOR_COLOR 

    for i in range(len(neighbors)):
        set_neighbor_weight(Graph, node, neighbors[i], edge_labels, visited_nodes)

        

        node_colors[neighbors[i]] = NEAREST_NEIGHBOR_COLOR
        '''if (weight < min_weight):
            min_weight = weight
            best_neighbor = neighbors[i]'''


    return nearest_neighbors

    #node_colors[best_neighbor] = CURRENT_NODE_COLOR

    

def go_to_next_node_with_min_weight(Graph, edge_labels, nearest_neighbors):

    min_weight = INF_WEIGHT


    for nearest_neighbor in nearest_neighbors:
        weight = Graph.nodes[nearest_neighbor]['value'] 
        if  weight < min_weight:
            min_weight = weight
            node_to_go = nearest_neighbor

    node_colors[node_to_go] = CURRENT_NODE_COLOR
    nearest_neighbors.discard(node_to_go)



    return node_to_go


def find_best_way(Graph, node_start, node_finish, edge_labels, n_graph = 0, create_img = True):


    #ребра на путях с минимальными весами
    good_edges = set()


    nearest_neighbors = set()
    Graph.nodes[node_start]['value'] = 0
    visited_nodes = set()
    node_colors[node_start] = CURRENT_NODE_COLOR

    current_node = node_start

    i = 0

    while(node_finish != current_node):

        if (create_img):
            draw_graph(Graph, n_graph, graph_pos, node_colors, edge_labels, good_edges)

        nearest_neighbors = set_weight_to_neighbors(Graph, current_node, edge_labels, nearest_neighbors, visited_nodes)


        if (create_img):
            n_graph += 1
            draw_graph(Graph, n_graph, graph_pos, node_colors, edge_labels, good_edges)

        node_colors[current_node] = VISITED_NODE_COLOR
        visited_nodes.add(current_node)

        current_node = go_to_next_node_with_min_weight(Graph, edge_labels, nearest_neighbors)

        if (current_node == -1):
            return INF_WEIGHT

        good_edges.add((Graph.nodes[current_node]['from_where'], current_node))

        if (create_img):
            n_graph += 1

        i += 1
        if (i >= 30):
            print("INF LOOP")
            break



    if (create_img):
        draw_graph(Graph, n_graph, graph_pos, node_colors, edge_labels, good_edges)    


    way_weight = Graph.nodes[node_finish]['value']

    reset_graph(Graph, start_node_values)

    n_graph += 1

    if (create_img):
        draw_graph(Graph, n_graph, graph_pos, node_colors, edge_labels, good_edges)  
    
    return way_weight

    

    draw_graph(Graph, n_graph, graph_pos, node_colors, edge_labels, good_edges)    


    reset_graph(Graph, start_node_values)

    n_graph += 1

    draw_graph(Graph, n_graph, graph_pos, node_colors, edge_labels, good_edges)  
    


if (__name__ == "__main__"):


    start_node_values = {i: INF_WEIGHT for i in range(9)}  # Значения для каждой вершины
    


    # Задаем фиксированные ребра и их веса
    edges_with_weights = [
        (0, 1, 1),
        (1, 2, 5),  # Ребро от V1 к V2 с весом 5
        (1, 3, 3),  # Ребро от V1 к V3 с весом 3
        (2, 4, 2),  # Ребро от V2 к V4 с весом 2
        (3, 5, 6),  # Ребро от V3 к V5 с весом 6
        (4, 6, 1),  # Ребро от V4 к V6 с весом 1
        (5, 7, 4),  # Ребро от V5 к V7 с весом 4
        (6, 8, 7),  # Ребро от V6 к V8 с весом 7
        (7, 8, 3)   # Ребро от V7 к V8 с весом 3
    ]


    Graph, graph_pos, node_colors, edge_labels = create_graph(99, start_node_values, edges_with_weights) 







        
    find_best_way(Graph, 1, 4, edge_labels, 0)
    find_best_way(Graph, 0, 8, edge_labels, 10)







