#!/usr/bin/python3

import devpipeline.build.build
import devpipeline.scm.scm
import devpipeline.common


def main(args=None):
    builder = devpipeline.common.TargetTool([
        devpipeline.scm.scm.scm_task,
        devpipeline.build.build.build_task
    ])
    devpipeline.common.execute_tool(builder, args)


if __name__ == '__main__':
    main()
