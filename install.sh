#!/bin/sh

BASENAME=/usr/bin/basename
CAT=/bin/cat
CUT=/usr/bin/cut
DIRNAME=/usr/bin/dirname
ECHO=/bin/echo
INSTALL=/usr/bin/install

prefix=/usr/local

do_help() {
	${CAT} <<EOF
${0} - Install dev-pipeline tools

${0} [--prefix=/path/to/install]

OPTIONS
  -h, --help        Display this help message

  --prefix=<prefix> Install the tools to <prefix>.  This will override DESTDIR
                    if both are set.  Defaults to ${prefix}.

ENVIRONMENT
  DESTDIR
    The prefix for installation.  This can be overriden using the "--prefix"
    option.
EOF
}

basedir=$(${DIRNAME} "${0}")

install_file() {
	file="${1}"
	dest="${2}"
	mode="${3}"

	${INSTALL} -m ${mode} "${file}" "${prefix}/${dest}"
}

install_exec() {
	dest=$(${BASENAME} "${1}" | ${CUT} -d . -f 1)
	install_file "${1}" "${2}/${dest}" "0755"
}

install_share() {
	dest=$(${BASENAME} "${1}")
	install_file "${1}" "${2}/${dest}" "0644"
}

install_directory() {
	${INSTALL} -m 0755 -d "${prefix}/${1}"
}

install_helper() {
	runner="${1}"
	path="${2}"
	install_directory "${path}"

	shift 2
	for f in ${@}; do
		"${runner}" "${basedir}/${f}" "${path}"
	done
}

# Check for environmental overrides
if [ -n "${DESTDIR}" ]; then
	prefix=${DESTDIR}
fi

for arg in ${@}; do
	case "${arg}" in
	"--help")
		do_help
		exit ${?}
		;;

	"-h")
		do_help
		exit ${?}
		;;

	"--prefix="*)
		prefix=$(${ECHO} ${arg} | ${CUT} -d = -f 2)
		;;
	esac
done

${ECHO} "Instaling to \"${prefix}\""

binFiles=" \
	bin/dev-pipeline.sh \
"
libexecFiles=" \
	libexec/devpipeline/bootstrap.py \
	libexec/devpipeline/build.py \
	libexec/devpipeline/build-order.py \
	libexec/devpipeline/checkout.py \
	libexec/devpipeline/configure.py \
"
libFiles=" \
	lib/devpipeline/__init__.py \
	lib/devpipeline/common.py \
	lib/devpipeline/config.py \
	lib/devpipeline/resolve.py \
"

libBuildFiles=" \
	lib/devpipeline/build/__init__.py \
	lib/devpipeline/build/build.py \
	lib/devpipeline/build/cmake.py \
"

libScmFiles=" \
	lib/devpipeline/scm/__init__.py \
	lib/devpipeline/scm/git.py \
	lib/devpipeline/scm/scm.py \
"

# tools
install_helper install_exec "bin" ${binFiles}
install_helper install_share "lib/devpipeline/" ${libFiles}
install_helper install_share "lib/devpipeline/build" ${libBuildFiles}
install_helper install_share "lib/devpipeline/scm" ${libScmFiles}
install_helper install_exec "libexec/devpipeline" ${libexecFiles}
