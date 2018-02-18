#!/usr/bin/python3

import re

import devpipeline.common
import devpipeline.resolve


class BuildOrderer(devpipeline.common.TargetTool):

    def __init__(self):
        super().__init__(description="Determinte all dependencies of a set of"
                                     " targets and the order they should be "
                                     "built in.")
        self.add_argument("--dot",
                          help="Generate a dot graph showing dependencies.",
                          action="store_true")

    def setup(self, arguments):
        self.dot = arguments.dot

    def process(self):
        if not self.dot:
            build_order = devpipeline.resolve.order_dependencies(
                self.targets, self.components)
            print(build_order)
        else:
            rev_deps = devpipeline.resolve._build_dep_data(self.targets,
                                                           self.components)[1]
            def remove_hyphen(s):
                return re.sub("-", lambda m: "_", s)

            print("digraph dependencies {{")
            for p, deps in rev_deps.items():
                stripped_p = remove_hyphen(p)
                print("\t{}".format(stripped_p))
                for d in deps:
                    print("\t{} -> {}".format(remove_hyphen(d), stripped_p))
            print("}}")


build_orderer = BuildOrderer()
devpipeline.common.execute_tool(build_orderer)
