#!/usr/bin/python3

import devpipeline.scm.scm
import devpipeline.common


class Checkout(devpipeline.common.TargetTool):

    def __init__(self):
        super().__init__([
            devpipeline.scm.scm.scm_task
        ], description="Checkout repositories")


checkout = Checkout()
devpipeline.common.execute_tool(checkout)
