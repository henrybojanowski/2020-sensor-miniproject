#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
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


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)
    #print("length of data should be three: ",len(data)," END")
    counter=0
    print("\n")
    for k in data: 
        #k is either "temperature" "occupancy" or "co2"
        #print("data[k] is: ", data[k], "END")
        #print("k is: ",k)

        #for task 2 Q4 I need all data, not just room data 
        #putting question four between the 1st and 2nd for loop
        
        if(counter <1):
            counter=counter+1
            time=data[k].index
            time_diff_array=np.array(np.diff(time.values).astype(np.int64) // 1000000000)
            print("Task 2 question 4: ")
            #print("size of time_diff_array: ",len(time_diff_array))
            #print("time_diff_array: ",time_diff_array, " END")
            print("mean of time interval sensor readings: ",np.mean(time_diff_array))
            print("variance of time interval sensor readings: ",np.var(time_diff_array))
            plt.hist(time_diff_array)
            plt.xlabel("time interval between sensor readings (for all sensors) in seconds")
            plt.ylabel("frequency")
            plt.title("frequency of time interval sensor readings for all rooms")
            print(" END of Task 2 question 4 \n")
        for x,y in data[k].items():
            #print("this should be a room: ",x," END")
            which_room=x
            # which_room gets set to either "lab1" 
            # "class1" or "office"


            if(which_room!="lab1"): 
                continue 
                #looking to use lab1 as my room for qs 1-3
                #if the room isn't lab1, below is NOT executed

            if(which_room=="lab1" and k=="temperature"): 
                time = data[k].index
                #print("data[k][lab1][time] is: ", data[k]["lab1"][time])
                a=np.array(data[k]["lab1"][time])
                print
                #print("a is: ",a," END a")
                # for i in a: 
                #     if(a[i]!=nan):
                #         without_nan[i]=a[i]
                without_nan = [x for x in a if str(x) != 'nan']
                #print("without_nan : ",without_nan," END ")
                #print("number of ", k, "values in lab1 : " ,len(without_nan))
                print("Task 2 question 1 data: ")
                median=np.median(without_nan)
                print("median of temperature for lab1: ", median)
                print("Variance of  temperature for lab1: ",np.var(without_nan, dtype=np.float64))
                print("End of task 2 question 1 data \n")
                
                #data[k].hist()
               
                plt.figure()
                
                plt.hist(without_nan)
               
                plt.xticks(np.arange(np.min(without_nan),np.max(without_nan),1))
                plt.xlabel("temperature (degrees Celsius)")
                plt.ylabel("frequency")
                plt.title("Frequency of temperatures for lab1 data")
            elif(which_room=="lab1" and k=="occupancy"):
                time = data[k].index
                #print("data[k][lab1][time] is: ", data[k]["lab1"][time])
                a=np.array(data[k]["lab1"][time])
                #print("a is: ",a," END a")
                # for i in a: 
                #     if(a[i]!=nan):
                #         without_nan[i]=a[i]
                without_nan = [x for x in a if str(x) != 'nan']
                #print("without_nan : ",without_nan," END ")
                #print("number of ", k, "values in lab1 : " ,len(without_nan))
                
                median=np.median(without_nan)
                print("Task 2 question 2 data: ")
                print("median of occupancy: ", median)
                print("Variance of  occupancy: ",np.var(without_nan, dtype=np.float64))
                print("END of Task 2 question 2 data: ")
                #data[k].hist()
               
                plt.figure()
                
                plt.hist(without_nan)
               
                plt.xticks(np.arange(np.min(without_nan),np.max(without_nan),1))
                plt.xlabel("room occupancy")
                plt.ylabel("frequency")
                plt.title("Frequency of room occupancies for lab1 data ")
            elif(which_room=="lab1" and k=="co2"):
                time = data[k].index
                #print("data[k][lab1][time] is: ", data[k]["lab1"][time])
                a=np.array(data[k]["lab1"][time])
                #print("a is: ",a," END a")
                # for i in a: 
                #     if(a[i]!=nan):
                #         without_nan[i]=a[i]
                without_nan = [x for x in a if str(x) != 'nan']
                #print("without_nan : ",without_nan," END ")
                #print("number of ", k, "values in lab1 : " ,len(without_nan))
                
                median=np.median(without_nan)
                #print("median of co2 concentration: ", median)
                #print("Variance of  co2 concentration: ",np.var(without_nan, dtype=np.float64))
                
                #data[k].hist()
               
                plt.figure()
                
                plt.hist(without_nan)
               
                plt.xticks(np.arange(np.min(without_nan),np.max(without_nan),2))
                plt.xlabel("co2 concentration (ppm)")
                plt.ylabel("frequency")
                plt.title("Frequency of co2 concentration for lab1 data")
    plt.show()
"""
    for k in data:
        # data[k].plot()
        #print("data[k] is: ",data[k], "END ")

        #new_arr=np.array()
        #if(k=="temperature"):
            # arry1=[11,3,5,87]
            # x= [-2,-1,1,2]
            # print("arry1: ", arry1, " norm.pdf(arry1) ",norm.pdf(arry1))
            # plt.plot(x, norm.pdf(arry1))
            #print("data ISS: ",data, " k is: ", k)
            
            #print("data[k] is: ",data[k],"hi")
            #plt2=plt
            time = data[k].index
            #print("time[lab1] " ,data[k]["lab1"][time], "END")
            a=np.array(data[k]["lab1"][time])
            print("number of ", k, "values in lab1 : " ,a.size)
            #b=norm.pdf(a)
            #print("a[0:3]",a[0:3])
            #print("np.arange(-4,4,0.001): ",np.arange(-4,4,0.001))
            #print("a: ",a)
            median=np.median(a)
            print("median of temperature: ", median)
            print("Variance of  temperature: ",np.var(a, dtype=np.float64))
            #x_axis_array= np.linspace((median-5),(median+5),a.size)
            #f=plt.figure(1)
            data[k].hist()
            #plt.width()
            plt.figure()
            #plt.hist([1,2,3,4])
            #plt.figure()
            plt.hist(a)
            #print("min of a: ", np.amin(a))
            plt.xticks(np.arange(np.min(a),np.max(a),4))
            plt.xlabel("temperature (degrees Celsius)")
            plt.ylabel("frequency")
            plt.title("Frequency of temperatures ")
            
            #plt2.plot(a, norm.pdf(a))
            #plt2.draw()
            #plt.raw_input()


            #plt.show()
            #print("data[k].sort_index is: ",data[k].sort_index())
            
            #print("np.diff(time.values).astype(np.int64) // 1000000000 IS: ",np.diff(time.values).astype(np.int64) // 1000000000)
            data[k].hist(width=0.04)
            y_vals=np.diff(time.values).astype(np.int64) // 1000000000
            plt.hist(np.median(data[k]), width=0.04)
            #plt.bar([1,2,3,4],y_vals, width=0.1)
            #plt.show()

            
            plt.figure()
            
            plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
            plt.xlabel("time difference of recordings (seconds)")
            plt.ylabel("# of recordings for each time difference")
            #is_k=k
            plt.title("time vs messages for temperature")
            
            
            dev_x = [25,26,27,28]
            dev_y=[1,2,3,5]
            plt.bar(dev_x,dev_y, width=0.1)
            print(np.median(dev_x))
            plt.bar(np.median(dev_x),[2])
            plt.show()
            
        elif(k=="occupancy"):
            time = data[k].index
            #print("time[lab1] " ,data[k]["lab1"][time], "END")
            a=np.array(data[k]["lab1"][time])
            #print("np.arange(-4,4,0.001): ",np.arange(-4,4,0.001))
            #print("a: ",a)
            print("Number of ", k, "values in lab1 : " ,a.size)
            print("median of occupancy: ", np.median(a))
            print("Variance of  occupancy: ",np.var(a, dtype=np.float64))
            #x_axis_array= np.linspace(10.,16.,a.size)
            # plt.figure()
            # plt.hist(a, width=0.1)
            # plt.draw()

            plt.figure()
            plt.hist(a)
            plt.xticks(np.arange(np.min(a),np.max(a),1))
            plt.xlabel("occupancy")
            plt.ylabel("frequency")
            plt.title("Frequency of occupancy (number people)")
        elif(k=="co2"):
            time = data[k].index
            #print("time[lab1] " ,data[k]["lab1"][time], "END")
            a=np.array(data[k]["lab1"][time])
            #print("np.arange(-4,4,0.001): ",np.arange(-4,4,0.001))
            #print("a: ",a)
            print("Number of ", k, "values in lab1 : " ,a.size)
            print("median of co2: ", np.median(a))
            print("Variance of  co2: ",np.var(a, dtype=np.float64))
            #x_axis_array= np.linspace(10.,16.,a.size)
            # plt.figure()
            # plt.hist(a, width=0.1)
            # plt.draw()

            plt.figure()
            plt.hist(a)
            plt.xticks(np.arange(np.min(a),np.max(a),1))
            plt.xlabel("co2 concentration (ppm)")
            plt.ylabel("frequency")
            plt.title("Frequency of co2 concentration")

"""
    #plt.show()


    
