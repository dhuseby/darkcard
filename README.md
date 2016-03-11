# Dark Card v1.0

This repo contains everything you need to print and laser cut a "dark card".
A dark card is a simple way to bootstrap an encrypted communication channel
between two people by using some dice rolls to generate a key and some simple
scripts to encrypt and decrypt a message using the key.

## Use

The first thing to do is to generate a key.  Take your eight-sided die (D8) and
roll it 86 times, writing down each number as you go.  Next, write down the key
number.  You can number keys sequentially, or you can roll your D8 four times
to generate a random number.  They key number isn't used in encryption, but it
is used for convenience to the receiver of the encrypted message.  They key
number is human readable in the encrypted file and allows the receiver to
quickly find which key to use to try to decrypt the message.  Be warned though,
that part of the encrypted file isn't covered by the authenticity guaranteed
by the encryption, so it can be modified in transit.  It's just for convenience,
so if it is modified, the encrypted message can still be decrypted and read.

After generating a key and giving it a number, write the same key and number on
a second card and give the card to the person you wish to communicate with.  The
security of your communication channel rests on both of you keeping the key a
secret.  So handle that card with care.

To send an encrypted message, you must first clone this repo to a computer with
a reasonably POSIX compliant terminal, a text editor, python, and the pynacl
python module.  Then, just run the ./encrypt.sh shell script.  It will open your
default text editor to get the key from you.  Just type in the key as it appears
on your card, left to right, top to bottom.  Save the file and quit the text
editor.  It will then ask you for the key number using the same procedure.

The next thing it does is ask you for a "nonce".  A "nonce" is a Number used
only ONCE.  If you are super paranoid, you can now roll your D8 and additional
sixty-four (64) times and enter them into the file.  You can also choose not to
generate a nonce and instead leave the file empty.  In that case, the software
will use the NaCl library random number generator to generate a nonce for you.

In the last step, the script will ask you for the message you wish to send.  I
would take this opportunity to either generate a bunch more symmetric keys with
my D8 and send those.  Or export a public key and paste it in here.  The idea
is that you will use this secure bootstrap method to solve the initial trust
problem.  By generating a key, in person, using dice, you can establish some
level of trust with the other person.  Then use the key to send a single message
to bootstrap more convenient and secure forms of communicating.

I like to use these to create the ability for me to bootstrap secure
communications with friends in the future in the event of a SHTF scenario.  I
generate keys, give them to friends, and tell them, if you ever receive an
encrypted message that has a "key #" first line, use this method to decrypt it.

## Notes on Key Generation

To generate a key, you must use a D8.  They are commonly found in role playing
dice sets that you can purchase online or from your local gaming/comics store.
Why a D8?  D8's give us octal numbers which fit into 3 bits.  To generate a
32-byte (256-bit) key, we need to roll the D8 eighty-six (86) times.  I know
that seems like a lot but I had to ballance the availability of dice with the
ease of use.  

If we wanted 4 bits each roll, we'd need a 16-sided die.  5 bits, 32-sided.  6
bits, 64-sided.  Since you're probably going to have or buy a complete role
playing dice set, part of me wanted to require rolling two 10-sided, one
20-sided, and one 8-sided dice to generate numbers between 1 and 128.  But that
seemed like a net gain in work.  So a D8, 86 times it is.  

Hopefully you won't have to do this too often.  If done correctly, you will
only need to do this once per person you wish to communicate with.  You can use
the generated key to send an encrypted list of symmetric keys, or your public
key that you will use from then on.
