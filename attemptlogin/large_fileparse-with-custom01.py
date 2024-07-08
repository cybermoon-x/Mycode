#!/usr/bin/python3
"""Alta3 Research | RZFeeser@alta3.com
   Solution to Customization 01"""

# parse keystone.common.wsgi and return number of failed login attempts
loginfail = 0 # counter for fails
posts = 0 # total times we see pattern, "POST"

# open the file for reading
with open("/home/student/mycode/attemptlogin/keystone.common.wsgi") as kfile:

    # loop over the file
    for line in kfile:
        # if this 'fail pattern' appears in the line...
        if "- - - - -] Authorization failed" in line:
            loginfail += 1 # this is the same as loginfail = loginfail + 1
        # the following elif agumentation MUST be AFTER we check for a fail
        # this statement assumes the if statement above it tested false
        elif "POST" in line:  # can ONLY be true if the "if" was false!
            posts += 1 # this is the total number of times we see this pattern

# display the number of failed log in attempts
print("The number of failed log in attempts is", loginfail)

# display the number of successful log in attempts
print("The number of successful POSTs is", posts)

