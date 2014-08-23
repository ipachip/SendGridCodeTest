#!/usr/bin/python

#
# This script reads in the command line options and sends out an email 
# message using the values supplied with the flags.
# 
# Shortcomings: 
#
# Only takes two recipients: a primary recipient and a CC
#
# To do:
# 1) Handle html file input
# 2) Better error reporting
#
# Implemented:
#  add_to(self, to):
#  add_cc(self, cc):
#  set_date(self, date):
#  set_from(self, from_email):
#  set_subject(self, subject):
#  set_text(self, text):
#  add_attachment(self, name, file_):
#  add_to_name(self, to_name):
#  set_from_name(self, from_name):
#  add_bcc(self, bcc):
#  set_replyto(self, replyto):
#  set_html(self, html):
#
# To implement:
#  add_attachment_stream(self, name, string):
#  set_headers(self, headers):
#
#
# See usage function below for current options and required parameters
#
#   

import sys
import getopt
import fileinput
import sendgrid
from sendgrid import SendGridError, SendGridClientError, SendGridServerError

def usage():
  print " Usage:" + sys.argv[0] + "[-a <attachment file>] [-A <attachment name>] [-b <bcc>] [-c <recipient>] "
  print "                          [-d <date>] -f <sender> [-F <from-name>] [-h] [-n <to-name>] "
  print "                          -p <password> [-s <subject>] -t <recipient> "
  print "                          -u <username> -v -x <header>"
  print "   -A <attachment name>     Name of the attachment.  required if attachment used"
  print "   -a <attachment file>     A file to be included as an attachment"
  print "   -b <bcc>                 Blind carbon copy recipient"
  print "   -c <recipient>           Carbon copy recipient"
  print "   -d <date>                Message date"
  print "   -f <sender>              Who is sending the email"
  print "   -F <from-name>           Name of sender, appended to sender"
  print "   -h                       Input is html"
  print "   -n <to-name>             Name of recipient as appears in body"
  print "   -p <sendgrid password>   The sendgrid account holder password"
  print "   -r <reply-to recipient>  Reply to recipient"
  print "   -s <subject>             Message subject" 
  print "   -t <recipient>           The person to which you are sending the email"
  print "   -u <sendgrid username>   The sendgrid account holder login"
  print "   -v verbose               Print out the message sent and parameters passed"
  print "   content is supplied as stdin or as a file name as the last argument"
  sys.exit(1)

  
def main (argv):
  #
  # Parse the arguments
  try:
    opts, args = getopt.getopt(argv, "A:a:b:c:d:f:F:n:p:r:s:t:u:hv", ["to", "cc", "from",
    "attachment"])
  except getopt.GetoptError:
    print " Error in argument list"
    usage()

  do_html = False
  verbose = False
  for opt, arg in opts:
    if verbose:
      print "processing opt: " + opt
    if opt in ("-A"):
      attach_name = arg
    elif opt in ("-a", "--attachment"):
      attachment = arg
    elif opt in ("-b"):
      bcc = arg
    elif opt in ("-c", "--cc"):
      cc = arg
    elif opt in ("-d"):
      date = arg
    elif opt in ("-f", "--from"):
      sender = arg
    elif opt in ("-F"):
      fromname = arg
    elif opt in ("-h"):
      do_html = True
    elif opt in ("-n"):
      to_name = arg
    elif opt in ("-p"):
      login_password = arg
    elif opt in ("-r"):
      reply = arg
    elif opt in ("-s"):
      subject = arg
    elif opt in ("-t", "--to"):
      to = arg
      if verbose:
        print "Processing the to/recipient " + to
    elif opt in ("-u"):
      login_username = arg
    elif opt in ("-v"):
      verbose = True

  #
  # Parameter checks
  if 'to' not in locals(): 
    print "Unspecified recipient"
    usage()

  if 'sender' not in locals(): 
    print "Unspecified sender"
    usage()

  if 'login_username' not in locals(): 
    print "SendGrid login username not supplied"
    usage()

  if 'login_password' not in locals(): 
    print "SendGrid password not supplied"
    usage()

  #
  # Start the message setup.
  if verbose:
    print "Username: " + login_username

  if verbose:
    print "Password: " + login_password
  
  #
  #  Create the sendgrid object
  sg = sendgrid.SendGridClient(login_username, login_password, raise_errors=True)

  message = sendgrid.Mail()


  #
  # Mandatory parameters
  message.set_from (sender)
  message.add_to (to)

  #
  # Optional parameters

  if 'subject' in locals():
    message.set_subject (subject)

  if 'attachment' in locals():
    if 'attach_name' not in locals(): 
      print "ERROR: Attachment name not supplied"
      usage ()
    message.add_attachment (attach_name, attachment)

  if 'cc' in locals():
    if verbose:
      print "Adding cc ", cc
    message.add_cc (cc)

  #
  # Add Bcc.  Note that there is at least one problem with bcc:
  # https://github.com/sendgrid/sendgrid-php/issues/23
  #
  if 'bcc' in locals():
    if verbose:
      print "Adding bcc ", bcc
    message.add_bcc (bcc)

  if 'date' in locals():
    message.set_date (date)

  if 'to_name' in locals():
    message.add_to_name(to_name)

  if 'from_name' in locals():
    message.add_from_name(from_name)

  if 'reply' in locals():
    message.set_replyto (reply)


  #
  # Read in the body of the message.
  text = ""
  for line in fileinput.input(args):
    text += line
    if verbose:
      sys.stdout.write(line)

  if do_html:
    message.set_html (text)
  else:
    message.set_text (text)

  status = 0
  msg = ''
  try: 
    status, msg = sg.send(message)
  except SendGridClientError, e: 
    print "ERROR: Send grid client error encountered:", e
  except SendGridServerError, e:
    print "ERROR: Send grid server error encountered:", e
  print "Status: ", status
  print "Message: ", msg





if __name__ == "__main__":
  main(sys.argv[1:])

  
