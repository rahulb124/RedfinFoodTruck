#!/usr/bin/env python

# Make sure to install requests before running:
# > pip install requests
# Documentation for the requests library can be found here: http://docs.python-requests.org/en/master/

#Imports 
import requests
import datetime


#API Request URL and AppToken for Socrata API
url = "http://data.sfgov.org/resource/bbb8-hzi6.json"
appToken = "1scxbEzlzH87tdByH9V8FU2Qf"

#Filtering for Name, Location, Start and End using SoQL and ordering by name alphabetically
selectQuery = "&$select=applicant,location,start24,end24&$order=applicant"


#Getting current date/time using datetime module
todaysDatetime = datetime.datetime.today()
dayOfTheWeek = str(todaysDatetime.isoweekday())
currentTime = datetime.datetime.now().time()


#Returning list of FoodTrucks that are open at the time request was made.
def filterFoodTrucks(data, currentTime):
	result = []
	for item in data:
		
		#Handling semantics of Time notation
		startHours,startMinutes = item["start24"].split(":")
		endHours,endMinutes = item["end24"].split(":")
		
		if(endHours == "24"):
			endHours = "0"

		#API time must be put into datetime format for comparison
		openTime = datetime.datetime.now().replace(hour=int(startHours),minute=int(startMinutes),second=0,microsecond=0)
		closeTime = datetime.datetime.now().replace(hour=int(endHours),minute=int(endMinutes),second=0,microsecond=0)
		

		if (openTime.time() <= currentTime and closeTime.time() > currentTime):
			result.append(item)
	return result


#Printing of  filtered data to user
def printData(filteredTrucks):
	print("Food Trucks in San Francisco Open Right Now")
	dash = '-' * 48
	print(dash)
	print("NAME                                    ADDRESS")
	print(dash)
	index = 0

	#handling 10 Foodtrucks at a time while waiting for user input
	while(len(filteredTrucks) > 0):
		if(index < 10 and index < len(filteredTrucks)):
			
			print('{:<40}{:<40}'.format(filteredTrucks[index]["applicant"],filteredTrucks[index]["location"]))
			index += 1
		else:
			if(len(filteredTrucks) <= 10):
				break
			userInput = input("Press 1 to continue or Press 2 to quit: ")
			if(userInput == "1"):
				#removes first 10 items from list 
				del filteredTrucks[:10]
				index = 0
			elif (userInput == "2"):
				break;


def makerequest():
	response = requests.get(url+"?$$app_token="+appToken+"&dayorder="+dayOfTheWeek+selectQuery)
	if response.status_code == 200:
	    data = response.json()
	    filteredTrucks = filterFoodTrucks(data, currentTime)
	    printData(filteredTrucks)
	else:
		#handling error in retrieving data
		print('HTTP', response.status_code)
		print("Error retrieving data")



makerequest()






