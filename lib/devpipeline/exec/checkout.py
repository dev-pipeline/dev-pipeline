#!/usr/bin/python3
"""This modules does the checkout of code from SCM."""

import devpipeline.scm.scm
import devpipeline.common


def main(args=None):
    # pylint: disable=missing-docstring
    checkout = devpipeline.common.TargetTool([
        devpipeline.scm.scm.scm_task
    ], prog="dev-pipeline checkout", description="Checkout repositories")
    devpipeline.common.execute_tool(checkout, args)


if __name__ == '__main__':
    main()
