
def HandleError(ret):
    if ret == 104:
         print "Could not establish connection. Check if Eye Tracker is running."
    elif ret == 105:
         print "Could not establish connection. Check the communication Ports."
    elif ret == 123:
         print "Could not establish connection. Another Process is blocking the communication Ports."
    elif ret == 201:
         print "Could not establish connection. Check if Eye Tracker is installed and running."
    else:
        print "Return Code is " + res + ". Refer to the iView X SDK Manual for its meaning."
	return