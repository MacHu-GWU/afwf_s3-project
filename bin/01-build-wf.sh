#!/bin/bash
#
# Build Alfred Workflow release from source code.
# Basically it creates:
#
# - ${dir_workflow}/main.py
# - ${dir_workflow}/lib
# - ${dir_workflow}/workflow

dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
dir_project_root="$(dirname "${dir_here}")"

source "${dir_here}/settings.sh"

bin_pip="${dir_venv}/bin/pip"

rm "${dir_workflow}/main.py"
rm -r "${dir_workflow}/lib"
rm "${dir_project_root}/info.plist"

cp "${dir_project_root}/main.py" "${dir_workflow}/main.py"

# install afwf
${bin_pip} install "${dir_project_root}" --target="${dir_workflow}/lib"

cp "${dir_workflow}/info.plist" "${dir_project_root}/info.plist"
