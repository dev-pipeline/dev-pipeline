#!/usr/bin/python3

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

    def setup(self, arguments):
        if arguments.build_dir:
            self.build_dir = arguments.build_dir
        else:
            if arguments.context:
                self.build_dir = "{}-{}".format(
                    arguments.build_dir_basename, arguments.context)
            else:
                self.build_dir = arguments.build_dir_basename
        self.context = arguments.context
        self.config = arguments.config

    def process(self):
        devpipeline.config.write_cache(
            devpipeline.config.ConfigFinder(self.config),
            devpipeline.config.ContextConfig(self.context),
            self.build_dir)


configure = Configure()
devpipeline.common.execute_tool(configure)
