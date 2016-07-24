from classes.MTI.free_mti import FreeMTI
from classes.MeSH.mesh_reader import parse_mesh
from xml.etree import cElementTree as elemtree


class QueryExpander():

    def __init__(self, parameters):
        self._parameters = parameters
        self.free_mti = FreeMTI()

        # turn this off for now
        # self._mesh = [x for x in parse_mesh(parameters.mesh_path)]

    def expand_query_from_topic_file(self, file_path, nth_topic):
        xml_data = elemtree.parse(file_path)
        node = xml_data.findall("//topic[@number='{}']".format(nth_topic))[0]

        return self.expand_query_from_string(node.find("./summary").text)

    def expand_query_from_string(self, query):
        return self.free_mti.query(query)