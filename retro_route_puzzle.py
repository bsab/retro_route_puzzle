#https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html#directed-graphs
import json
import logging
import networkx as nx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

directions = ['north', 'south', 'east', 'west']


class RetroRoutePuzzle():
    """A program that will output a valid route one could follow to collect all specified items within a map.
    The map is a json description of set of rooms with allowed path and contained object.
    It starts with an input of:
        json reppresentation of map
        starting room
        list of object to collect.
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
        """ creo un grafo orientato (digraph) a  partire dalla mappa json.
        La notazione cardinale delle direzioni non ha valore indica esclusivamente che esiste
        una porta (ad esempio chiamata Nord) che permette di andare dalla stanza X alla stanza Y
        (ma non viceversa se non diversamente specificato). Questo significa che:
         - Se la stanza X ha porte vero Y W e Z
         - E Z ha porte esclusivamente verso Y e W
         - Da X potrai andare in Z ma da Z non puoi tornare in X"""

        map_graph = None
        try:
            map_graph = nx.DiGraph(name="Map")

            for room in map_dict['rooms']:
                # aggiungo i nodi al grafo ...
                map_graph.add_node(room['id'],
                                   name=room['name'],
                                   objects=room['objects'])

                # e leggendo le direzioni, aggiungo li archi fra un nodo e l'altro
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

    def __collect_room_object(self, room_id):
        """controllo che nel nodo (ovvero la room) siano presenti oggetti
        da collezionare, in caso positivo elimino l'oggetto dalla lista
        objects_to_collect"""

        room_object = None
        if len(self.__map_graph.node[room_id]['objects'])>0:
            room_object = self.__map_graph.node[room_id]['objects'][0]['name']
            if room_object in objects_to_collect:
                print '*****popping ', room_object, '...'
                objects_to_collect.pop(objects_to_collect.index(room_object))

        return room_object

    def navigate_and_collect(self, start_room_id, objects_to_collect):
        """
        Seguo tutti i percorsi raggiungibili dal nodo X (start_room_id).
        Edge classification during
        Eseguo un Breadth-first search sul directed graph partendo dal nodo X
        e da questo classifico tutti gli edge ottenuti in una lista.
        A questo punto, stampo per ogni nodo dell'edge presente nella lista
        le info del nodo.
        """

        if start_room_id<=0:
            logger.error('Cannot run algorithm on map. The start room ID is not valid', exc_info=False)
            return False
        elif not self.__map_graph:
            logger.error('Cannot run algorithm on map. The map is None', exc_info=False)
            return False
        elif not objects_to_collect:
            logger.error('Cannot run algorithm on map. No objects to collects', exc_info=False)
            return False

        try:
            print "ID Room Object collected"
            print "---------------------------"

            edge_routing = list(nx.bfs_edges(self.__map_graph, start_room_id))
            #print "edge_routing--->", edge_routing
            for (room_from, room_to) in edge_routing:

                room_name = self.__map_graph.node[room_from]['name']
                room_object = self.__collect_room_object(room_from)
                print room_from, " ", room_name, " ", room_object
                if not objects_to_collect:
                    break;

                room_name = self.__map_graph.node[room_to]['name']
                room_object = self.__collect_room_object(room_to)
                print room_to, " ", room_name, " ", room_object
                if not objects_to_collect:
                    break;

            print "---------------------------"

        except Exception as e:
            logger.error('Cannot run algorithm map on graph', exc_info=True)
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

    retro_route_puzzle.navigate_and_collect(start_room_id, objects_to_collect)

    print "Room Object remain to collect:"
    print objects_to_collect


