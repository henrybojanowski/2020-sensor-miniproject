import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f :
            r = json.loads(line)
            #print("list(r.keys())[0] IS: ",list(r.keys())[0])
            #if list(r.keys())[0]=="lab1":
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            #print("temperature is (in load_data): ",temperature[time], {room: r[room]["temperature"][0] })
            #print("temperature indexed:",temperature[time]["lab1"])

            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
       "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
       "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
       
    }

    return data
p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
p.add_argument("file", help="path to JSON data file")
P = p.parse_args()

file = Path(P.file).expanduser()

data = load_data(file)



def anomaly(data_input): 
	# inputs a 1D array, outputs 1D array 
	#min and max determined by cleaning data that is more than
			# one standard deviation away
			#subtract away data points that are outside of one st. dev.
			# then take the max and min of that data: that is how we 
			# determined the bounds (for class1,lab1,office)
	#anomaly is if there's a point outside of one standard deviation 

	
	one_stdv=1*np.std(data_input)
	data_mean=np.mean(data_input)


	# variables for for loop: 
	
	anomaly_counter=0
	counter=0
	anomolies=np.zeros(100)
	for i in data_input:
		#print("i is: ",i)
		#print(data_input[0])
		dev_from_mean=abs(data_mean-data_input[counter])
		if(dev_from_mean>=one_stdv):
			#print("if statement executes")
			anomolies[anomaly_counter]=i
			anomaly_counter=anomaly_counter+1
		counter=counter+1
	return anomolies
print("*******TASK 3 DATA******* \n")
for k in data:
	#k is either "temperature" "co2" or "occupancy"
	
	for x,y in data[k].items():
		which_room = x
		# which_room gets set to either "lab1" "class1" or "office"
	    
		if(which_room=="lab1" and k=="temperature"):

			print("LAB1 DATA ")
			time = data[k].index
			a=np.array(data[k]["lab1"][time])
			without_nan = [x for x in a if str(x) != 'nan']
			lab1_anomoly_array=anomaly(without_nan)
			#without_zeros=[x for x in lab1_anomoly_array if int(x)!=0]
			count1=0

			for i in lab1_anomoly_array:
				if(i==0):
					break
				count1=count1+1

			lab1_anomoly_array=lab1_anomoly_array[0:count1]
			#print("lab1_anomoly_array: ",lab1_anomoly_array)
			#print("length of lab1 temperature anomaly array: ",len(lab1_anomoly_array))
			#print("length of lab1 temperature array with bad points: ",len(without_nan))
			print("DATA for Task 3 question 1: percent of bad data points for lab1: ",100*len(lab1_anomoly_array)/(len(without_nan)),"%")
			

			
			counter=0
			for i in lab1_anomoly_array: 
				#print("i is: ",i)
				if i==0:
					break
				without_nan.remove(i)
				# all the bad data points have been removed from without_nan with the above for loop



			#print("length of lab1 temperature array without bad points: ",len(without_nan))
			print("DATA for Task 3 question 1 temperature median of lab1 room without bad data points: ", np.median(without_nan))
			print("DATA for Task 3 question 1 variance of lab1 temperature without bad points: ",np.var(without_nan))
	
			print("DATA for Task 3 question 3: lab1 bounds for temperature:   min: ",np.amin(without_nan), "  max: ",np.amax(without_nan) )
			print("END OF LAB1 DATA \n")
			#lab1code
		if(which_room=="class1" and k=="temperature"):
			print("CLASS1 DATA: ")
			time = data[k].index
			a=np.array(data[k]["class1"][time])
			without_nan = [x for x in a if str(x) != 'nan']
			class1_anomoly_array=anomaly(without_nan)
			#print("class1_anomoly_array: ",class1_anomoly_array)
			#without_zeros=[x for x in lab1_anomoly_array if int(x)!=0]
			count1=0
			for i in class1_anomoly_array:
				if(i==0):
					break
				count1=count1+1

			class1_anomoly_array=class1_anomoly_array[0:count1]
			
			#print("class1_anomoly_array: ",class1_anomoly_array)
			#print("length of class1 temperature anomaly array: ",len(class1_anomoly_array))
			#print("length of class1 temperature array with bad points: ",len(without_nan))
			print("DATA for Task 3 question 1 percent of bad data points for class1: ",100*len(class1_anomoly_array)/(len(without_nan)),"%")

			
			counter=0
			for i in class1_anomoly_array: 
				#print("i is: ",i)
				if i==0:
					break
				without_nan.remove(i)
				# all the bad data points 

				#have been removed from without_nan with the above for loop
				


			#print("length of class1 temperature array without bad points: ",len(without_nan))
			print("DATA for Task 3 question 1 temperature median of class1 room without bad data points: ", np.median(without_nan))
			print("DATA for Task 3 question 1 variance of class1 temperature without bad points: ",np.var(without_nan))
			print("DATA for Task 3 question 3 class1 bounds for temperature:   min: ",np.amin(without_nan), "  max: ",np.amax(without_nan) )

			print("END OF CLASS1 DATA \n")
			#class1 code
		if(which_room=="office" and k=="temperature"):
			print("OFFICE DATA: ")
			time = data[k].index
			a=np.array(data[k]["office"][time])
			without_nan = [x for x in a if str(x) != 'nan']
			office_anomaly_array=anomaly(without_nan)
			#without_zeros=[x for x in lab1_anomoly_array if int(x)!=0]
			count1=0
			for i in office_anomaly_array:
				if(i==0):
					break
				count1=count1+1

			office_anomaly_array=office_anomaly_array[0:count1]
			
			#print("lab1_anomoly_array: ",office_anomaly_array)
			#print("length of office temperature anomaly array: ",len(office_anomaly_array))
			#print("length of office temperature array with bad points: ",len(without_nan))
			print("DATA for Task 3 question 1: percent of bad data points for office: ",100*len(office_anomaly_array)/(len(without_nan)),"%")

			
			counter=0

			for i in office_anomaly_array: 
				#print("i is: ",i)
				if i==0:
					break
				without_nan.remove(i)
				# all the bad data points have been removed from without_nan with the above for loop
				


			#print("length of temperature array without bad points ",len(without_nan))
			print("DATA for Task 3 question 1: temperature median of office room without bad data points: ", np.median(without_nan))
			print("DATA for Task 3 question 1: variance of office temperature data without bad points: ",np.var(without_nan))
			print("DATA for Task 3 question 3 office bounds for temperature:   min: ",np.amin(without_nan), "  max: ",np.amax(without_nan) )
			print("END OF OFFICE DATA \n")
			#office code