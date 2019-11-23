#!/usr/bin/env bash

if [[ -s /galaxy/tools/exaremeTools/exareme_environment.py ]]; then
    rm -rf /galaxy/tools/exaremeTools/exareme_environment.py
fi

echo "EXAREME_IP = "\"${EXAREME_IP}\" >> /galaxy/tools/exaremeTools/exareme_environment.py
echo "EXAREME_PORT = "\"${EXAREME_PORT}\" >> /galaxy/tools/exaremeTools/exareme_environment.py
