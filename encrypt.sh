#!/bin/sh

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

# get the encryption key as D8 string
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

# maybe get a nonce as a D8 string
nonce="$(mktemp)"
cat >${nonce} <<EOL

----
# To avoid using any digital random number generator,
# roll a D8 sixty-four (64) times and enter each number above
# the ---- in this file.  Or, you can leave this file empty and
# a random nonce will be generated for you using the NaCL random
# number generator.
EOL
${VISUAL:-${EDITOR:-vi}} ${nonce}

# get the message
msg="$(mktemp)"
cat >${msg} <<EOL

----
# Please enter your message above the ---- in this file.
EOL
${VISUAL:-${EDITOR:-vi}} ${msg}

# find a good file name to store the encrypted data in
i=0
f=$(printf "msg.%0*d" 4 ${i})
while [ -e ${f} ]; do
  i=$((i+1))
  f=$(printf "msg.%0*d" 4 ${i})
done

env python ./encrypt.py ${key} ${number} ${nonce} ${msg} > ${f}

rm ${key}
rm ${number}
rm ${nonce}
rm ${msg}
