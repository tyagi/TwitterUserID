"""
This Module is for finding userid by using screen_name/username.

+------------+
|Dependencies|
+------------+
	
	* Twython (pip install twython
	* OAuth (usually gets installed with Twython)

.. moduleauthor:: Ankur Tyagi (warlock_ankur)
"""


from twython import Twython
import logging
import time

APP_KEY = "pbPc7sYa1dfjh9l3g30egwBYf"
APP_SECRET = "M5fYl6TPcx6KCUElsSjqCNbiWUlkjVFVJxwFeNKP40Y3NJI601"
READFILE = "names.txt"
WRITEFILE = "names2.txt"

def getScreenNames():
	f = open(READFILE)
	screen_names = f.readlines()
	f.close()
	for i in range(len(screen_names)):
		screen_names[i] = screen_names[i].strip('\n')
	
	return screen_names

# Have not Used Show_User because that gives us only 180req while this can give us total of 600req
def lookupUser(names):
	twitter = Twython(APP_KEY, APP_SECRET)
	try:
		users = twitter.lookup_user(screen_name = names)
	except Exception as e:
		logging.error("Error Occured while fetching the Users. Error = %s", e)
		return None

	return users

def userlimitexceed(names):
	users = []
	lst = 0
	for i in range(100, len(names), 100):
		newnames = names[lst:i]
		_users = lookupUser(newnames)
		if users == None :
			logging.info("Rate Limited. Going to Sleep for 15 min.")
			print "Rate Limited. Going to Sleep for 15 min."
			time.sleep(15*60)
			logging.info("Waked Up!!. Restarting the retrieval Process.")
			print "Waked Up!!. Restarting the retrieval Process."
			i = i - 100
		else :
			users.append(_users)
			lst = i

	if len(names) > i:
		newnames = names[lst:len(names)]
		_users = lookupUser(newnames)
		users.append(_users)

	return users

def writeUserIds(users):
	f = open(WRITEFILE, "w")
	for user in users:
		f.write(user['screen_name'] + ', ' + user['id_str'] + '\n')
	f.close()

def appendUserIds():
	names = getScreenNames()
	users = []
	if len(names) > 100:
		users = userlimitexceed(names)
	
	users = lookupUser(names)
	if users == None :
		logging.info("Rate Limited. Going to Sleep for 15 min.")
		print "Rate Limited. Going to Sleep for 15 min."
		time.sleep(15*60)
		logging.info("Waked Up!!. Restarting the retrieval Process.")
		print "Waked Up!!. Restarting the retrieval Process."
		users = lookupUser(names)

	writeUserIds(users)

if __name__ == '__main__':
	logging.basicConfig(filename="TwitterUserId.log", format='%(asctime)s %(message)s', level=logging.DEBUG)
	appendUserIds()