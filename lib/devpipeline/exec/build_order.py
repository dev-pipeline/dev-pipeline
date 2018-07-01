#!/usr/bin/python3
"""This modules generates a build ordered list of targets."""

import re
import sys

import devpipeline.config.config
import devpipeline.common
import devpipeline.resolve


def _dotify(string):
    """This function swaps '-' for '_'."""
    return re.sub("-", lambda m: "_", string)


def _print_graph(targets, components):
    # pylint: disable=protected-access
    rev_deps = devpipeline.resolve._build_dep_data(targets, components)[1]

    print("digraph dependencies {")
    for pkg, deps in rev_deps.items():
        stripped_pkg = _dotify(pkg)
        print("\t{}".format(stripped_pkg))
        for dep in deps:
            print("\t{} -> {}".format(_dotify(dep), stripped_pkg))
    print("}")

def _print_dot(targets, components):
    print("Warning: dot option is deprecated.  Use graph instead.",
          file=sys.stderr)
    _print_graph(targets, components)


def _print_layers(targets, components):
    layer = 0

    def _add_layer(resolved_dependencies):
        nonlocal layer

        print("\tsubgraph cluster_{} {{".format(layer))
        print("\t\tlabel=\"Layer {}\"".format(layer))
        for component in resolved_dependencies:
            stripped_name = _dotify(component)
            component_dependencies = components[component].get("depends")
            if component_dependencies:
                for dep in devpipeline.config.config.split_list(
                        component_dependencies):
                    print("\t\t{} -> {}".format(stripped_name, _dotify(dep)))
            print("\t\t{}".format(stripped_name))
        print("\t}")
        layer += 1

    print("digraph layers {")
    devpipeline.resolve.process_dependencies(targets, components, _add_layer)
    print("}")


def _print_list(targets, components):
    build_order = devpipeline.resolve.order_dependencies(targets, components)
    print(build_order)


_ORDER_OUTPUTS = {
    "dot": _print_dot,
    "graph": _print_graph,
    "layer": _print_layers,
    "list": _print_list,
}


class BuildOrderer(devpipeline.common.TargetTool):

    """This class outputs an ordered list of the packages to satisfy dependencies."""

    def __init__(self):
        super().__init__(executors=False,
                         prog="dev-pipeline build-order",
                         description="Determinte all dependencies of a set of "
                                     "targets and the order they should be "
                                     "built in.")
        self.add_argument("--method",
                          help="The method used to display build order.  Valid"
                               " options are list (an order to resolve "
                               "specified targets), dot (a dot graph), and "
                               "layer (a dot graph that groups components "
                               "into layers based on their dependencies)..",
                          default="list")
        self.helper_fn = None

    def setup(self, arguments):
        self.helper_fn = _ORDER_OUTPUTS.get(arguments.method)
        if not self.helper_fn:
            raise Exception("Invalid method: {}".format(arguments.method))

    def process(self):
        self.helper_fn(self.targets, self.components)


def main(args=None):
    # pylint: disable=missing-docstring
    build_orderer = BuildOrderer()
    devpipeline.common.execute_tool(build_orderer, args)


if __name__ == '__main__':
    main()
