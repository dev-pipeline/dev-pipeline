#!/usr/bin/python3

import devpipeline.common
import devpipeline.git
import devpipeline.resolve

_scm_lookup = {
    "git": devpipeline.git.make_git
}


def make_scm(component):
    scm = component._values.get("scm")
    if scm:
        scm_fn = _scm_lookup.get(scm)
        if scm_fn:
            return scm_fn(component)
        else:
            raise Exception(
                "Unknown scm '{}' for {}".format(scm, component._name))
    else:
        raise Exception("{} does not specify scm".format(component._name))


class Checkout(devpipeline.common.Tool):

    def __init__(self):
        super().__init__(description="Checkout repositories")

    def process(self):
        build_order = devpipeline.resolve.order_dependencies(
            self.targets, self.components)
        for target in build_order:
            scm = make_scm(self.components._components[target])
            scm.checkout(target)
            scm.update(target)


checkout = Checkout()
devpipeline.common.execute_tool(checkout)
