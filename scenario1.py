#!/usr/bin/python

#
# This script reads in the command line options and sends out an email 
# message using the values supplied with the flags.
# 
# One immediate shortcoming is that it will only take two
# recipients right now, a main and cc
#
# Usage: 
#   -t <recipient> (to)
#   -c <recipient> (cc)
#   -f <sender>    (from)
#   -a <attachment file>
#   content is supplied as stdin

import sys
import getopt
import fileinput
import sendgrid

def usage():
  print " Usage:" + sys.argv[0] + "[-s <subject>] -t <recipient> [-c <recipient>] -f <sender> [-a <attachment file>]"
  print "          -p <password> -u <username>"
  print "   -a <attachment file> a file to be included as an attachment"
  print "   -c <recipient> carbon copy recipient"
  print "   -f <sender>    who is sending the email"
  print "   -p <sendgrid password> the sendgrid account holder password"
  print "   -t <recipient> the person to which you are sending the email"
  print "   -u <sendgrid username> the sendgrid account holder login"
  print "   content is supplied as stdin"
  sys.exit(1)

  
def main (argv):
  #
  # Parse the arguments
  try:
    opts, args = getopt.getopt(argv, "a:c:f:p:s:t:u:", ["to", "cc", "from",
    "attachment"])
  except getopt.GetoptError:
    print " Error in argument list"
    usage()

  for opt, arg in opts:
    print "processing opt: " + opt
    if opt in ("-a", "--attachment"):
      attachment = arg
    elif opt in ("-c", "--cc"):
      cc = arg
    elif opt in ("-f", "--from"):
      sender = arg
    elif opt in ("-p"):
      login_password = arg
    elif opt in ("-s"):
      subject = arg
    elif opt in ("-t", "--to"):
      to = arg
      print "Processing the to/recipient " + to
    elif opt in ("-u"):
      login_username = arg

  if 'to' not in locals(): 
    print "Unspecified recipient"
    usage()

  if 'sender' not in locals(): 
    print "Unspecified sender"
    usage()

#  print "sending to " + to + " from: " + sender 
#  print "Leftover args: ", args

  #
  # Start the message setup.
  print "Username: " + login_username
  print "Password: " + login_password
  
  sg = sendgrid.SendGridClient(login_username, login_password)

  message = sendgrid.Mail()
  message.set_from (sender)

  if 'subject' in locals():
    message.set_subject (subject)

  message.add_to (to)
  #
  # Read in the body of the message.
  text = ""
  for line in fileinput.input(args):
    text += line
    sys.stdout.write(line)

  message.set_text (text)

  status, msg = sg.send(message)

  print "Status: ", status
  print "Message: ", msg





if __name__ == "__main__":
  main(sys.argv[1:])

  
