from classes.MTI.free_mti import FreeMTI
from classes.MeSH.mesh_reader import parse_mesh
from xml.etree import cElementTree as elemtree


class QueryExpander():

    def __init__(self, parameters):
        self._parameters = parameters
        self.free_mti = FreeMTI()

        self.mesh_xml = elemtree.parse(self._parameters.mesh_path)

    def expand_query_from_topic_file(self, file_path, nth_topic):
        xml_data = elemtree.parse(file_path)
        node = xml_data.findall(".//topic[@number='{}']".format(nth_topic))[0]

        return self.expand_query_from_string(node.find("./summary").text)

    def expand_query_from_string(self, query):
        mti_result = self.free_mti.query(query)
        result = {"0": set()}
        for label in mti_result:
            name = label["concept_name"]
            result["0"].add(name)

        if self._parameters.traverse_tree_up:
            for i in range(self._parameters.traverse_tree_up_limit):
                partial = set()
                for name in result[str(i)]:
                    for descriptor in self._find_parent_descriptors_by_name(name):
                        partial.add(descriptor)
                result[str(i + 1)] = partial

        return result

    def _find_descriptor_by_name(self, name):
        descriptor = self.mesh_xml.find("./DescriptorRecord/DescriptorName[String='{}']/..".format(name))
        if not descriptor:
            raise IndexError("No such descriptor name: {}".format(name))
        return descriptor

    def _find_descriptor_by_tree_number(self, tree_number):
        descriptor = self.mesh_xml.find("./DescriptorRecord/TreeNumberList[TreeNumber='{}']/..".format(tree_number))
        if not descriptor:
            raise IndexError("No such descriptor tree number: {}".format(tree_number))
        return descriptor

    def _find_parent_descriptors_by_name(self, name):
        descriptor = self._find_descriptor_by_name(name)
        result = []
        for tree_number_element in descriptor.findall("./TreeNumberList/TreeNumber"):
            tree_number = tree_number_element.text
            if "." in tree_number:
                parent_tree_number = tree_number.rsplit(".", 1)[0]
                result.append(self._find_descriptor_by_tree_number(parent_tree_number).find("./DescriptorName/String").text)

        return list(set(result))

