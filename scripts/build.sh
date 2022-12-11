export PATH="$HOME/.local/bin:$HOME/bin:$PATH"

OS_NAME=$(python -c 'import platform; print(platform.system().lower())')
ARCH_TYPE=$(python -c 'import platform; print(platform.machine().lower())')
PY_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
DIR_NAME="dosh-${OS_NAME}-${ARCH_TYPE}-py${PY_VERSION}"

if ! command -v poetry &> /dev/null
then
    pip install poetry
fi

poetry install --with=dev
poetry run pyinstaller app.py --name=dosh --console --noconfirm

cd ./dist/
mv dosh $DIR_NAME
tar -czvf $DIR_NAME.tar.gz $DIR_NAME/*
