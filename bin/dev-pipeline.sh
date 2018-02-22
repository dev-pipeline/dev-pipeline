#!/bin/sh

CAT=/bin/cat
CUT=/usr/bin/cut
BASENAME=/usr/bin/basename
DIRNAME=/usr/bin/dirname
ECHO=/bin/echo
LS=/bin/ls
PWD=/bin/pwd
PYTHON=/usr/bin/python3

dir=$(${DIRNAME} "${0}")
first=$(${ECHO} ${dir} | ${CUT} -b 1)
if [ "${first}" != "/" ]; then
	dir="$(${PWD})/${dir}"
fi
toolsDir="${dir}/../libexec/devpipeline"

do_help() {
	local=$(${BASENAME} ${0})
	${CAT} <<EOF
${local} - Front-end to dev-pipeline tools.

${local} <tool> [tool options]

OPTIONS
  -h, --help  Display this help message

  --list      List the available tools
EOF
}

do_list() {
	echo "coming soon :)"
}


if [ ${#} -gt 0 ]; then
	case "${1}" in
	"--help")
		do_help
		exit ${?}
		;;

	"-h")
		do_help
		exit ${?}
		;;

	"--list")
		do_list
		exit ${?}
		;;
	esac
	tool="${1}"
	shift
	export PYTHONPATH="${dir}/../lib:${PYTHONPATH}"
	${PYTHON} -m "devpipeline.exec.${tool}" ${@}
else
	do_help
fi
