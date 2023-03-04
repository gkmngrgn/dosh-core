#!/bin/bash

export PATH="$HOME/.local/bin:$HOME/bin:$PATH"

if command -v poetry &> /dev/null
then
    echo "poetry found in path."
else
    python -m pip install --user pipx
    python -m pipx install poetry
fi

poetry install --no-ansi --no-interaction
poetry self add 'poethepoet[poetry_plugin]' --no-ansi --no-interaction
poetry poe build

OS_NAME=$(python -c 'import platform; print(platform.system().lower())')
ARCH_TYPE=$(python -c 'import platform; print(platform.machine().lower())')
PY_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
DOSH_VERSION=$(poetry run dosh version)
DIR_NAME="dosh-${DOSH_VERSION}-${OS_NAME}-${ARCH_TYPE}"

echo "---"
echo "PYTHON VERSION: ${PY_VERSION}"
echo "DIRECTORY     : ${DIR_NAME}"
echo "---"

mkdir "${DIR_NAME}"
mv dosh.bin "${DIR_NAME}/dosh"
tar -czvf "${DIR_NAME}.tar.gz" "${DIR_NAME}/"*
