#!/usr/bin/python3

import devpipeline.scm.scm
import devpipeline.common


def main(args=None):
    checkout = devpipeline.common.TargetTool([
        devpipeline.scm.scm.scm_task
    ], prog="dev-pipeline checkout", description="Checkout repositories")
    devpipeline.common.execute_tool(checkout, args)


if __name__ == '__main__':
    main()
