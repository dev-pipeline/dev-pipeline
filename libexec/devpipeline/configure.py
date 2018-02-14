#!/usr/bin/python3

import os
import os.path

import devpipeline.cachewriter
import devpipeline.common
import devpipeline.iniloader


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
                self.build_dir = "{}-{}".format(args.build_dir_basename, args.context)
            else:
                self.build_dir = args.build_dir_basename
        self.context = args.context
        self.config = args.config

    def process(self):
        config = devpipeline.iniloader.read_config(self.config)
        context_file = "{}/{}".format(os.path.expanduser("~"), ".dev-pipeline")
        if os.path.isfile(context_file):
            context_config = devpipeline.iniloader.read_config(context_file)
        else:
            context_config = None
        devpipeline.cachewriter.write_cache(config, context_config,
                                            self.build_dir, self.context)


configure = Configure()
devpipeline.common.execute_tool(configure)
