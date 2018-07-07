#!/usr/bin/python3

"""
The main module for devpipeline.  It provides the TOOLS variable, a map of all
available tools.
"""

import devpipeline_core.plugin

TOOLS = devpipeline_core.plugin.query_plugins('devpipeline.drivers')
