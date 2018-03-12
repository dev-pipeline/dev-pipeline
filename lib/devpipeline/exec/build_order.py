#!/usr/bin/python3
"""This modules generates a build ordered list of targets."""

import re

import devpipeline.common
import devpipeline.resolve


def _print_list(targets, components):
    build_order = devpipeline.resolve.order_dependencies(targets, components)
    print(build_order)


def _print_dot(targets, components):
    # pylint: disable=protected-access
    rev_deps = devpipeline.resolve._build_dep_data(targets, components)[1]

    def remove_hyphen(string):
        """This function swaps '-' for '_'."""
        return re.sub("-", lambda m: "_", string)

    print("digraph dependencies {")
    for pkg, deps in rev_deps.items():
        stripped_pkg = remove_hyphen(pkg)
        print("\t{}".format(stripped_pkg))
        for dep in deps:
            print("\t{} -> {}".format(remove_hyphen(dep), stripped_pkg))
    print("}")


_ORDER_OUTPUTS = {
    "list": _print_list,
    "dot": _print_dot
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
                               "specified targets) and dot (a dot graph).",
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
