OS_NAME=$(python -c 'import platform; print(platform.machine().lower())')
ARCH_TYPE=$(python -c 'import platform; print(platform.processor().lower())')
PY_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
DIR_NAME="dosh-${OS_NAME}-${ARCH_TYPE}-py${PY_VERSION}"

pip install poetry
poetry install
poetry run poe build

cd ./dist/
mv dosh $DIR_NAME
tar -czvf $DIR_NAME.tar.gz $DIR_NAME/*
