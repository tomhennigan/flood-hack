#!/usr/bin/env bash

if [ ! -d env ]; then
    virtualenv env
fi

. env/bin/activate

if [ ! -f env/installed -o requirements.txt -nt env/installed ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Unable to install requirements. "
        exit 1
    fi

    touch env/installed
fi

python src/main.py "$@"
