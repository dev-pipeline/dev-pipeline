#!/usr/bin/python3

import os
import os.path

import devpipeline.common
import devpipeline.config


class Configure(devpipeline.common.GenericTool):

    def __init__(self):
        super().__init__(description="Configure a project")
        self.add_argument("--config", help="Build configuration file",
                          default="build.config")
        self.add_argument("--context", help="Build-specific context to use")
        self.add_argument("--build-dir",
                          help="Directory to store configuration.  If "
                               "specified, --build-dir-basename will be "
                               "ignored.")
        self.add_argument("--build-dir-basename",
                          help="Basename for build directory configuration",
                          default="build")

    def setup(self, args):
        if args.build_dir:
            self.build_dir = args.build_dir
        else:
            if args.context:
                self.build_dir = "{}-{}".format(
                    args.build_dir_basename, args.context)
            else:
                self.build_dir = args.build_dir_basename
        self.context = args.context
        self.config = args.config

    def process(self):
        devpipeline.config.write_cache(
            devpipeline.config.ConfigFinder(self.config),
            devpipeline.config.ContextConfig(self.context),
            self.build_dir)


configure = Configure()
devpipeline.common.execute_tool(configure)
