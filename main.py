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
        """Carico il file json contentente la struttura della mappa in un dizionario"""
        try:
            with open(self.__map_file_name) as data_file:
                self.__map_dict = json.load(data_file);
        except Exception as e:
            logger.error('Cannot load map from file', exc_info=True)

    def __set_map_on_graph(self):
        """A partire dal dizionario appena creato, definisco uno grafo orientato (digraph)
        utilizzando le room come nodi e le cardinalita' per l'associazione fra nodi."""
        try:
            for room in self.__map_dict['rooms']:
                # aggiungo i nodi al grafo
                self.__map_graph.add_node(room['id'],
                                          name=room['name'],
                                          objects=room['objects'])

                # leggendo le direzioni, aggiungo li archi fra un nodo e l'altro
                for room_dir in directions:
                    if room.has_key(room_dir):
                        next_room=room[room_dir]
                        self.__map_graph.add_edge(room['id'], next_room, dir=room_dir)
        except Exception as e:
            logger.error('Cannot setup map on graph', exc_info=True)

    def show_map_structure(self):
        logger.debug("---------------------------")
        logger.debug(self.__map_graph.graph)
        logger.debug(self.__map_graph.nodes(data=True))
        logger.debug(self.__map_graph.edges())
        logger.debug("---------------------------")

    def __get_row(self, room_id):
        room_name = self.__map_graph.node[room_id]['name']
        room_object=None
        if len(self.__map_graph.node[room_id]['objects'])>0:
            room_object = self.__map_graph.node[room_id]['objects'][0]['name']

        return room_name, room_object

    def run_routing(self, start_room_id, objects_to_collect):
        """
        L'algoritmo termina quando ha esaminato tutti i nodei del grafo oppure
        quando ha collezionato tutti gli elementi richiesti.
        :param start_room_id:
        :param objects_to_collect:
        :return:
        """
        try:
            #seguo tutti i percorsi raggiungibili dal nodo X

            # eseguo una BFS sul grafo inserendo in una lista tutti gli edge
            # stampo per ogni nodo dell'edge nella lista di cui sopra le info
            #
            print "ID Room Object collected"
            print objects_to_collect
            print "---------------------------"

            edge_routing = list(nx.bfs_edges(self.__map_graph, start_room_id))
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
            logger.error('Cannot run algorithm map on graph', exc_info=True)

if __name__ == "__main__":

    # definisco la struttura dati
    map_file_name='data.json'
    retro_route_puzzle = RetroRoutePuzzle(map_file_name)

    # stampo la struttura dati
    retro_route_puzzle.show_map_structure()

    # eseguo l'algoritmo
    start_room_id=4
    objects_to_collect=['Knife', 'Potted Plant', 'Pillow']
    retro_route_puzzle.run_routing(start_room_id, objects_to_collect)

