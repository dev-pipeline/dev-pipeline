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


def _do_dot(targets, components, layer_fn):
    def _handle_layer_dependencies(resolved_dependencies, attributes):
        for component in resolved_dependencies:
            stripped_name = _dotify(component)
            component_dependencies = components[component].get("depends")
            if component_dependencies:
                for dep in devpipeline.config.config.split_list(
                        component_dependencies):
                    print("{} -> {} {}".format(stripped_name,
                                               _dotify(dep), attributes))
            print("{} {}".format(stripped_name, attributes))

    print("digraph dependencies {")
    try:
        devpipeline.resolve.process_dependencies(
            targets, components, lambda rd: layer_fn(
                rd, lambda rd: _handle_layer_dependencies(
                    rd, "")))
    except devpipeline.resolve.CircularDependencyException as cde:
        layer_fn(
            cde._components,
            lambda rd: _handle_layer_dependencies(
                rd, "[color=\"red\"]"))
    print("}")


def _print_graph(targets, components):
    # pylint: disable=protected-access
    _do_dot(targets, components, lambda rd, dep_fn: dep_fn(rd))


def _print_dot(targets, components):
    print("Warning: dot option is deprecated.  Use graph instead.",
          file=sys.stderr)
    _print_graph(targets, components)


def _print_layers(targets, components):
    layer = 0

    def _add_layer(resolved_dependencies, dep_fn):
        nonlocal layer

        print("subgraph cluster_{} {{".format(layer))
        print("label=\"Layer {}\"".format(layer))
        dep_fn(resolved_dependencies)
        print("}")
        layer += 1

    _do_dot(targets, components, _add_layer)


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
