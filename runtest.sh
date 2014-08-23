#!/bin/bash
#
# This shell script calls the python SendGrid API script.  Using a shell script provides 
# a quick harness to call the script with multiple combinations of parameters.
TMPFILE=$(mktemp)
cleanup() {
  rm $TMPFILE
}
trap cleanup EXIT SIGINT SIGTERM

USR=ipachip
PASS=Testlab123

#
# Happy path:
RECIP=chip@pupman.com
FROM=sgtestr@yahoo.com

#
# Testing scenario 1, happy path:
SUBJ="Test 1"
./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" testmsg.txt
echo ./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" testmsg.txt
SUBJ="Test 1, from yesterday"
./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" -d "$(date -R -d -1day)" testmsg.txt
echo ./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" -d "$(date -R -d -1day)" testmsg.txt


#
# Testing scenario 2, CC
SUBJ="Test 2, with CC"
CARBCOP=chip.atkinson@gmail.com
./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" -c "$CARBCOP" testmsg.txt
echo ./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" -c "$CARBCOP" testmsg.txt

#
# Testing scenario 3, Attachment and attachment name
SUBJ="Test 3, with Attachment"
ATT=scenario1.py
ANAME="scenario1.py"
./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" -c "$CARBCOP" -a $ATT -A $ANAME testmsg.txt
echo ./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" -c "$CARBCOP" -a $ATT -A $ANAME testmsg.txt


#
# Make a large file of random bytes and send it.  If it works, then double the size and try again.  
# Repeat until fail
# Start with 1M
SIZE=$((1024 * 1024))
while :; do
  SUBJ="Test 4, size $SIZE"
  cat /dev/urandom | base64 | head -c$SIZE > $TMPFILE
  echo "Mailing a file of $SIZE bytes"
  if ! ./scenario1.py -s "$SUBJ" -t "$RECIP" -f "$FROM" -p "$PASS" -u "$USR" $TMPFILE; then
    echo "Failed to mail, aborting"
    break
  fi
  SIZE=$((SIZE * 2))
done
