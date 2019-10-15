#!/usr/bin/env bash

if [[ -s /galaxyDir/galaxy/tools/exaremeTools/exareme_environment.py ]]; then
    rm -rf /galaxyDir/galaxy/tools/exaremeTools/exareme_environment.py
fi

echo "EXAREME_IP = "\"${EXAREME_IP}\" >> /galaxyDir/galaxy/tools/exaremeTools/exareme_environment.py
echo "EXAREME_PORT = "\"${EXAREME_PORT}\" >> /galaxyDir/galaxy/tools/exaremeTools/exareme_environment.py
