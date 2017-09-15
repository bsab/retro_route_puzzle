#https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html#directed-graphs
import json
import logging
import networkx as nx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

directions = ['north', 'south', 'east', 'west']


class RetroRoutePuzzle():
    """La notazione cardinale delle direzioni non ha valore indica esclusivamente che esiste
    una porta (ad esempio chiamata Nord) che permette di andare dalla stanza X alla stanza Y
    (ma non viceversa se non diversamente specificato). Questo significa che:
        Se la stanza X ha porte vero Y W e Z
        E Z ha porte esclusivamente verso Y e W
        Da X potrai andare in Z ma da Z non puoi tornare in X

    L'algoritmo del percorso deve permettere la collezione degli oggetti.
    """

    def __init__(self, map_file_name):
        """Constructor"""
        self.__map_file_name = map_file_name
        self.__map_graph = self.__load_map_from_file()

    def __load_map_from_file(self):
        """ Load map from file"""
        map_graph = None
        try:
            # carico il file che contiene la mappa json in un dizionario ...
            with open(self.__map_file_name) as data_file:
                map_dict = json.load(data_file);

            # .. e da questo definisco il DiGraph
            map_graph = self.__set_map_on_graph(map_dict)
        except Exception as e:
            logger.error('Cannot load map from file', exc_info=False)

        return map_graph

    def __set_map_on_graph(self, map_dict):
        """ creo un grafo orientato (digraph) a  partire dalla mappa json"""

        map_graph = None
        try:
            map_graph = nx.DiGraph(name="Map")

            for room in map_dict['rooms']:
                # aggiungo i nodi al grafo
                map_graph.add_node(room['id'],
                                   name=room['name'],
                                   objects=room['objects'])

                # leggendo le direzioni, aggiungo li archi fra un nodo e l'altro
                for room_dir in directions:
                    if room.has_key(room_dir):
                        next_room=room[room_dir]
                        map_graph.add_edge(room['id'], next_room, dir=room_dir)
        except Exception as e:
            logger.error('Cannot setup map on graph', exc_info=False)
            map_graph = None

        return map_graph

    def show_map_structure(self):
        print "---------------------------"
        if self.__map_graph:
            print "MAP GRAPH:", self.__map_graph.graph
            print "MAP NODES:", self.__map_graph.nodes(data=True)
            print "MAP EDGES:", self.__map_graph.edges()
        else:
            print "MAP GRAPH IS NONE"
        print "---------------------------"

    def __get_row(self, room_id):
        room_name = self.__map_graph.node[room_id]['name']
        room_object=None
        if len(self.__map_graph.node[room_id]['objects'])>0:
            room_object = self.__map_graph.node[room_id]['objects'][0]['name']

        return room_name, room_object

    def run_routing(self, start_room_id, objects_to_collect):

        if not self.__map_graph:
            logger.error('Cannot run algorithm map on graph. The graph is None', exc_info=False)
            return False
        try:
            #seguo tutti i percorsi raggiungibili dal nodo X

            # eseguo una BFS sul grafo inserendo in una lista tutti gli edge
            # stampo per ogni nodo dell'edge nella lista di cui sopra le info
            #
            print "ID Room Object collected"
            print "---------------------------"

            edge_routing = list(nx.bfs_edges(self.__map_graph, start_room_id))
            print "edge_routing--->", edge_routing
            for (room_from, room_to) in edge_routing:
                #room from
                room_name, room_object = self.__get_row(room_from)
                print room_from, " ", room_name, " ", room_object
                if room_object:
                    #print 'popping ', room_object, '...'
                    objects_to_collect.pop(objects_to_collect.index(room_object))
                    if not objects_to_collect:
                        break;

                #room to
                room_name, room_object = self.__get_row(room_to)
                print room_to, " ", room_name, " ", room_object
                if room_object:
                    #print 'popping ', room_object, '...'
                    objects_to_collect.pop(objects_to_collect.index(room_object))
                    if not objects_to_collect:
                        break;

            print "AFTER ID Room Object collected"
            print objects_to_collect
            print "---------------------------"

        except Exception as e:
            logger.error('Cannot run algorithm map on graph', exc_info=False)
            return False

if __name__ == "__main__":

    # definisco la struttura dati
    map_file_name='data.json'
    retro_route_puzzle = RetroRoutePuzzle(map_file_name)

    # stampo la struttura dati
    retro_route_puzzle.show_map_structure()

    # eseguo l'algoritmo
    start_room_id=4
    objects_to_collect=['Knife', 'Potted Plant', 'Pillow']
    #print objects_to_collect

    retro_route_puzzle.run_routing(start_room_id, objects_to_collect)

