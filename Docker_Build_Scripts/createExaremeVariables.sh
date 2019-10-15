#!/usr/bin/env bash

if [[ -s /srv/executor/tools/exaremeTools/exareme_environment.py ]]; then
    rm -rf /srv/executor/tools/exaremeTools/exareme_environment.py
fi

echo "EXAREME_IP = "\"${EXAREME_IP}\" >> /srv/executor/tools/exaremeTools/exareme_environment.py
echo "EXAREME_PORT = "\"${EXAREME_PORT}\" >> /srv/executor/tools/exaremeTools/exareme_environment.py
