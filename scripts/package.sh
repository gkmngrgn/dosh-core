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

export POETRY_HOME=~/poetry
python -m pip install virtualenv
python -m venv $POETRY_HOME

$POETRY_HOME/bin/pip install "poetry==$POETRY_VERSION"
$POETRY_HOME/bin/poetry install --with=dev
$POETRY_HOME/bin/poetry run pyinstaller app.py --name=dosh --console --noconfirm

cd ./dist/
mv dosh $DIR_NAME
tar -czvf $DIR_NAME.tar.gz $DIR_NAME/*
