from classes.MeSH.mesh_reader import parse_mesh


class QueryExpander():

    def __init__(self, parameters):
        self._parameters = parameters
        self._mesh = [x for x in parse_mesh(parameters.mesh_path)]

    def expand_query_from_topic_file(self, file_path):
        pass

    def expand_query_from_string(self, query):
        pass