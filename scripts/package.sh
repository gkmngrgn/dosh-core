#!/bin/bash

export PATH="$HOME/.local/bin:$HOME/bin:$PATH"

python -m pip install --user pipx
python -m pipx install poetry

poetry install --no-ansi --no-interaction
poetry run pyinstaller app.py --name=dosh --console --noconfirm --copy-metadata=dosh

OS_NAME=$(python -c 'import platform; print(platform.system().lower())')
ARCH_TYPE=$(python -c 'import platform; print(platform.machine().lower())')
PY_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
DOSH_VERSION=$(poetry run dosh version)
DIR_NAME="dosh-${DOSH_VERSION}-${OS_NAME}-${ARCH_TYPE}"

echo "---"
echo "PYTHON VERSION: ${PY_VERSION}"
echo "DIRECTORY     : ${DIR_NAME}"
echo "---"

cd ./dist/ || exit
mv dosh "${DIR_NAME}"
tar -czvf "${DIR_NAME}.tar.gz" "${DIR_NAME}/"*
