#https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html#directed-graphs
import json
import networkx as nx

#carico il file che contiene il json in memoria
with open('data.json') as data_file:
    map_dict = json.load(data_file);

#creo un grafo orientato (digraph) a  partire dalla mappa json
G = nx.DiGraph(name="Map")
directions=['north','south', 'east', 'west']
for room in map_dict['rooms']:
    _id=room['id']
    G.add_node(_id,
               name=room['name'],
               objects=room['objects'])

    for dir in directions:
        if room.has_key(dir):
            _to=room[dir]
            G.add_edge(_id, _to, dir=dir)

print G.graph
print G.nodes(data=True)
print G.edges()
print "---------------------------"
#seguo tutti i percorsi raggiungibili dal nodo X

# eseguo una BFS sul grafo inserendo in una lista tutti gli edge
start_room_id=4
print list(nx.bfs_edges(G, start_room_id))

#
# stampo per ogni nodo dell'edge nella lista di cui sopra le info
#
print "ID Room Object collected"
print "---------------------------"

for (_from, _to) in list(nx.bfs_edges(G, start_room_id)):
    print _from, " ", G.node[_from]['name'], " ", G.node[_from]['objects']
    print _to, " ", G.node[_to]['name'], " ", G.node[_to]['objects']