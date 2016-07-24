import argparse
import os
from classes.QueryExpander.query_expander import QueryExpander


def main():
    parser = argparse.ArgumentParser(description="MeSH query expansion example")

    parser.add_argument("--mesh-path", action="store", dest="mesh_path", default=".",
                        help="Path to MeSH files "
                             "(unused for now)")
    parser.add_argument("--traverse-tree-up", action="store_true", dest="traverse_tree_up", default=False,
                        help="Whether to traverse the MeSH ontology tree up if a match is found "
                             "(unused for now)")
    parser.add_argument("--traverse-tree-up-limit", action="store", dest="traverse_tree_up_limit", default=3,
                        help="How many levels of the ontology hierarchy tree nodes should be included "
                             "when a match is found "
                             "(unused for now)")

    parser.add_argument_group()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--query-file", action="store", dest="query_file", default=False,
                       help="Topic input file that will be expanded")
    group.add_argument("--query-string", action="store", dest="query_string", default=False,
                       help="Topic string that will be expanded")

    parser.add_argument("--nth-topic", action="store", dest="nth_topic", type=int,
                        help="Required for the --query-file option - which topic from the file should be considered")

    arguments = parser.parse_args()

    if not arguments.query_file and not arguments.query_string:
        parser.error("Either --query-file or --query-string has to be supplied")

    query_expander = QueryExpander(arguments)
    if arguments.query_file:
        if not arguments.nth_topic:
            parser.error("When --query-file is supplied, --nth-topic should be supplied, too")
        print(query_expander.expand_query_from_topic_file(arguments.query_file, arguments.nth_topic))
    else:
        print(query_expander.expand_query_from_string(arguments.query_string))

if __name__ == "__main__":
    main()