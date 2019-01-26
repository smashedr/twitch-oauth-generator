#!/usr/bin/env bash

PORT="9000"
PROT="http"

set -e

function trap_exit() { [[ "$?" = "0" ]] && exit 0 || exit 1 ; }
trap trap_exit EXIT SIGHUP SIGINT SIGTERM

host_array=(${DJANGO_ALLOWED})
[[ "${host_array[0]}" = "*" ]] && host_array[0]='localhost'
curl -ksL "${PROT}://localhost:${PORT}" -H "Host: ${host_array[0]}" >/dev/null 2>&1
[[ "$?" != "0" ]] && exit 1

exit 0
