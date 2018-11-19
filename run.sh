#!/bin/bash
#

if [ ! -d pyenv ]; then

	python3 -m venv pyenv

fi

source pyenv/bin/activate

python3 -m pip install -r requirements.txt

python3 dydns.py --configuration config.ini
