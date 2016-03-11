#!/bin/sh

if [ "$#" -lt 1 ] || [ ! -e ${1} ]; then
  echo "usage: ${0} <encrypted file>"
  exit 1
fi

# check for prerequisites
command -v mktemp >/dev/null 2>&1 || \
  { echo >&2 "I require the mktemp command for creating temp files.  Aborting."; exit 1; }
command -v cat >/dev/null 2>&1 || \
  { echo >&2 "I require the cat command for creating temp files.  Aborting."; exit 1; }
command -v python >/dev/null 2>&1 || \
  { echo >&2 "I require python to run.  Aborting."; exit 1; }
command -v ${VISUAL:-${EDITOR:-vi}} >/dev/null 2>&1 || \
  { echo >&2 "I require a text editor of some sort to run.  Aborting."; exit 1; }
env python -c "import nacl" >/dev/null 2>&1 || \
  { echo >&2 "I require the pynacl python module to run. Aborting."; exit 1; }

# get the encryption key as a D8 string
key="$(mktemp)"
cat >${key} <<EOL

----
# Please enter your D8 key above the ---- in this file.
EOL
${VISUAL:-${EDITOR:-vi}} ${key}

# get the key # for verification
number="$(mktemp)"
cat >${number} <<EOL

----
# Please enter the key # above the ---- in this file.
EOL
${VISUAL:-${EDITOR:-vi}} ${number}

env python ./decrypt.py ${key} ${number} ${1}

rm ${key}
rm ${number}
