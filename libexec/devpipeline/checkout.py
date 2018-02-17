#!/usr/bin/python3

import devpipeline.scm.scm
import devpipeline.common


checkout = devpipeline.common.TargetTool([
    devpipeline.scm.scm.scm_task
], description="Checkout repositories")
devpipeline.common.execute_tool(checkout)
