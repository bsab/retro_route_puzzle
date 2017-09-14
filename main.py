#https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html#directed-graphs
import json
import logging
import networkx as nx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

directions = ['north', 'south', 'east', 'west']


class RetroRoutePuzzle():

    # Constructor
    def __init__(self, map_file_name):
        self.__map_file_name = map_file_name
        self.__map_graph = nx.DiGraph(name="Map")

        self.__load_map_from_file()

        self.__set_map_on_graph()

    def __load_map_from_file(self):
        #carico il file che contiene il json in memoria
        with open(self.__map_file_name) as data_file:
            self.__map_dict = json.load(data_file);

    def __set_map_on_graph(self):
        #creo un grafo orientato (digraph) a  partire dalla mappa json

        for room in self.__map_dict['rooms']:
            self.__map_graph.add_node(room['id'],
                                      name=room['name'],
                                      objects=room['objects'])

            for room_dir in directions:
                if room.has_key(room_dir):
                    next_room=room[room_dir]
                    self.__map_graph.add_edge(room['id'], next_room, dir=room_dir)

    def show_map_structure(self):
        print "---------------------------"
        print self.__map_graph.graph
        print self.__map_graph.nodes(data=True)
        print self.__map_graph.edges()
        print "---------------------------"

    def run_routing(self, start_room_id):
        #seguo tutti i percorsi raggiungibili dal nodo X

        # eseguo una BFS sul grafo inserendo in una lista tutti gli edge
        # stampo per ogni nodo dell'edge nella lista di cui sopra le info
        #
        print "ID Room Object collected"
        print "---------------------------"

        edge_routing = list(nx.bfs_edges(self.__map_graph, start_room_id))
        for (room_from, room_to) in edge_routing:
            print room_from, " ", self.__map_graph.node[room_from]['name'], " ", self.__map_graph.node[room_from]['objects']
            print room_to, " ", self.__map_graph.node[room_to]['name'], " ", self.__map_graph.node[room_to]['objects']


if __name__ == "__main__":

    retro_route_puzzle = RetroRoutePuzzle('data.json')

    retro_route_puzzle.show_map_structure()

    start_room_id=4
    retro_route_puzzle.run_routing(start_room_id)

