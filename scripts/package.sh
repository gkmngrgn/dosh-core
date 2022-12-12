export PATH="$HOME/.local/bin:$HOME/bin:$PATH"

OS_NAME=$(python -c 'import platform; print(platform.system().lower())')
ARCH_TYPE=$(python -c 'import platform; print(platform.machine().lower())')
PY_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
POETRY_VERSION="1.2.2"
DIR_NAME="dosh-${OS_NAME}-${ARCH_TYPE}-py${PY_VERSION}"

echo "Operating System  : $OS_NAME"
echo "Architecture Type : $ARCH_TYPE"
echo "Python Version    : $PY_VERSION"
echo "Poetry Version    : $POETRY_VERSION"

python -m pip install --user pipx
python -m pipx install "poetry==$POETRY_VERSION"

poetry install
poetry run pyinstaller app.py --name=dosh --console --noconfirm

cd ./dist/
mv dosh $DIR_NAME
tar -czvf $DIR_NAME.tar.gz $DIR_NAME/*
