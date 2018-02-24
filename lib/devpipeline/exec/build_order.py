#!/usr/bin/python3

import re

import devpipeline.common
import devpipeline.resolve


def _print_list(targets, components):
    build_order = devpipeline.resolve.order_dependencies(targets, components)
    print(build_order)


def _print_dot(targets, components):
    rev_deps = devpipeline.resolve._build_dep_data(targets, components)[1]

    def remove_hyphen(s):
        return re.sub("-", lambda m: "_", s)

    print("digraph dependencies {{")
    for p, deps in rev_deps.items():
        stripped_p = remove_hyphen(p)
        print("\t{}".format(stripped_p))
        for d in deps:
            print("\t{} -> {}".format(remove_hyphen(d), stripped_p))
    print("}}")


_order_outputs = {
    "list": _print_list,
    "dot": _print_dot
}


class BuildOrderer(devpipeline.common.TargetTool):

    def __init__(self):
        super().__init__(prog="dev-pipeline build-order",
                         description="Determinte all dependencies of a set of "
                                     "targets and the order they should be "
                                     "built in.")
        self.add_argument("--method",
                          help="The method used to display build order.  Valid"
                               " options are list (an order to resolve "
                               "specified targets) and dot (a dot graph).",
                          default="list")

    def setup(self, arguments):
        self.fn = _order_outputs.get(arguments.method)
        if not self.fn:
            raise Exception("Invalid method: {}".format(arguments.method))

    def process(self):
        self.fn(self.targets, self.components)


def main(args=None):
    build_orderer = BuildOrderer()
    devpipeline.common.execute_tool(build_orderer, args)


if __name__ == '__main__':
    main()
