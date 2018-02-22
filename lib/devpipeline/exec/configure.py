#!/usr/bin/python3

import devpipeline.common
import devpipeline.config


class Configure(devpipeline.common.GenericTool):

    def __init__(self):
        super().__init__(description="Configure a project")
        self.add_argument("--config", help="Build configuration file",
                          default="build.config")
        self.add_argument("--profile",
                          help="Build-specific profiles to use.  If more than "
                               "one profile is required, separate their names "
                               "with commas.")
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
            if arguments.profile:
                self.build_dir = "{}-{}".format(
                    arguments.build_dir_basename, arguments.profile)
            else:
                self.build_dir = arguments.build_dir_basename
        self.profile = arguments.profile
        self.config = arguments.config

    def process(self):
        devpipeline.config.write_cache(
            devpipeline.config.ConfigFinder(self.config),
            devpipeline.config.ProfileConfig(self.profile),
            self.build_dir)


if __name__ == '__main__':
    configure = Configure()
    devpipeline.common.execute_tool(configure)
