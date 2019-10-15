#!/usr/bin/env bash

if [[ -s /mnt/c/Users/Thanasis/Desktop/Madgik/galaxy/Docker_Build_Scripts/exareme_environment.py ]]; then
    rm -rf /mnt/c/Users/Thanasis/Desktop/Madgik/galaxy/Docker_Build_Scripts/exareme_environment.py
fi

echo "EXAREME_IP = "\"${EXAREME_IP}\" >> /mnt/c/Users/Thanasis/Desktop/Madgik/galaxy/Docker_Build_Scripts/exareme_environment.py
echo "EXAREME_PORT = "\"${EXAREME_PORT}\" >> /mnt/c/Users/Thanasis/Desktop/Madgik/galaxy/Docker_Build_Scripts/exareme_environment.py
