#!/bin/sh

CAT=/bin/cat
CUT=/usr/bin/cut
BASENAME=/usr/bin/basename
DIRNAME=/usr/bin/dirname
ECHO=/bin/echo
LS=/bin/ls
PWD=/bin/pwd

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
	for tool in $(${LS} "${toolsDir}"); do
		if [ -x "${toolsDir}/${tool}" ]; then
			${ECHO} "${tool}"
		fi
	done
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
	tool="${toolsDir}/${1}"
	if [ -x "${tool}" ]; then
		shift
		export PYTHONPATH="${dir}/../lib:${PYTHONPATH}"
		${tool} ${@}
	else
		${ECHO} "\"${1}\" - Unknown command" >&2
		exit 1
	fi
else
	do_help
fi
