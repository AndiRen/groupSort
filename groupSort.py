#%%##########
## Imports ##
#############

import random
import time

#%%#############################
## Example Arrays for Sorting ##
################################

arr1=[random.randint(0, 100000000) for i in range(1000000)] #mergeSort is better
arr2=[random.randint(0, 55000000) for i in range(1000000)] #range upper limit groupSort with digit buckets
arr3=[random.randint(0, 35000000) for i in range(1000000)] #range upper limit groupSort basic
arr4=[random.randint(0, 10000000) for i in range(1000000)] #groupSort is faster than mergeSort
arr5=[random.randint(0, 1000000) for i in range(1000000)] #groupSort is faster than mergeSort
arr6=[random.randint(0, 100000) for i in range(1000000)] #groupSort is much faster than mergeSort
arr7=[random.randint(0, 10000) for i in range(1000000)] #groupSort is much faster than mergeSort

#mergeSort code by: Mayank Khanna
#taken from https://www.geeksforgeeks.org/merge-sort/ 
#Used for comparison

#%%############
## Functions ##
###############

####################################################################################################

#The basic implementation

def groupSort(arr,reporting=False):
    """
    info here
    """

    #start the timer
    start_time=time.time()

    #create a dict of all unique elements in the array and their instances
    sorting_dict,max_,min_,sorted=create_ele_dict(arr)

    #if sorted just return as is without concatanating the keys' lists of values
    if sorted==False:
        #use the range to add k instances of each unique value, in order
        sorted_array=sort_the_keys(sorting_dict,min_,max_)
    else:
        sorted_array=arr

    end_time=time.time()-start_time

    if reporting==True:
        #display results
        print(f"Total items sorted: {len(sorted_array)}")
        print(f"Total time taken: {end_time}")
    
    return sorted_array

####################################################################################################

def create_ele_dict(arr):
    """
    info here
    """
    
    #setup
    sorting_dict={}
    min_,max_=arr[0],arr[0]
    
    #To track if already sorted
    sorted=True
    previous=None

    #creating the dict O(n)
    for ele in arr:
        #either add the new key, or increase count of key instances
        if ele in sorting_dict:
            sorting_dict[ele]+=1
        else:
            sorting_dict[ele]=1
        #keep track of the max and min
        if ele > max_:
            max_=ele
        if ele < min_:
            min_=ele
        
        #running check to see if sorted
        if sorted==True:
            if previous==None or ele >= previous:
                previous=ele
            else:
                sorted=False
    
    return sorting_dict,max_,min_,sorted

####################################################################################################

def sort_the_keys(sorting_dict,min_,max_):
    """
    info here
    """
    
    sorted_array=[]
    
    #for each spot in the range, look for a matching key in the dict
    for i in range(min_, max_+1):
        if i in sorting_dict:
            sorted_array+=[i]*sorting_dict[i]
    
    return sorted_array

####################################################################################################
####################################################################################################
####################################################################################################

#The extended implementation

def groupSort_digits(arr,reporting=False):
    """
    info here
    """
    
    #start the timer
    start_time=time.time()
    
    #Create digit length buckets
    length_dict,max_length=create_length_groups(arr,reporting)
    
    if reporting==True:
        print("Processing Digit Length Groups")
    
    #Process all 1-3 digit buckets together
    sorted_array=process_small_groups(length_dict,reporting)
    
    #Process all 4+ digit buckets separately
    sorted_array=process_large_groups(sorted_array,length_dict,max_length,reporting)
    end_time=time.time()-start_time
    
    if reporting==True:
        print(f"Total items sorted: {len(sorted_array)}")
        print(f"Total time taken: {end_time}")
    
    return sorted_array

####################################################################################################

def create_length_groups(arr,reporting):
    """
    info here
    """
    
    len_dict_start=time.time()
    length_dict={}
    max_length=0
    
    #turn each element into a string to see how many digits i has
    for val in arr:
        str_val=str(val)
        len_val=len(str_val)
        #Keep track of the range of the digit buckerts, i.e. 1->max_length
        if len_val>max_length:
            max_length=len_val
        
        #drop each element into its matching digit length bucket
        if len_val in length_dict:
            length_dict[len_val].append(str_val)
        else:
            length_dict[len_val]=[str_val]
    
    if reporting==True:
        print(f"Time To Create Length Dictionary: {time.time()-len_dict_start}")
    
    return length_dict,max_length

####################################################################################################

def process_small_groups(length_dict,reporting):
    """
    info here
    """
    
    small_list=[]
    
    #for each of the 1-3 digit length groups, add their elements into a single list
    for i in range(1, 4):
        group_start=time.time()
        key=i
        try:
            small_list+=length_dict[key]
        except:
            pass
        
        #sort this list of all small elements together, using the groupSort approach
        if key==3:
            sorted_array=sort_small_groups(small_list)
            if reporting==True:
                print(f"Group {key}, sorted in group: {len(small_list)} -- total sorted so far: {len(sorted_array)} -- time taken for group: {time.time()-group_start}")
    
    return sorted_array

####################################################################################################

def sort_small_groups(arr):
    """
    info here
    """
    
    sorted_group=[]
    group_dict={}
    
    #create a dict of all unique elements and their instances
    for ele in arr:
        if ele in group_dict:
            group_dict[ele]+=1
        else:
            group_dict[ele]=1
            
    #use the range of the 1-3 digit length buckets to search for matcing keys 
    for i in range(1000):
        if str(i) in group_dict:
            #if found, populate that key's number of instances into a list
            sorted_group+=[i]*group_dict[str(i)]
    
    return sorted_group        

####################################################################################################

def process_large_groups(sorted_array,length_dict,max_length,reporting):

    #max_length is the number of digits for the group with the most digits
    for i in range(4, max_length+1):  
        group_start=time.time()
        key=i    
        
        #grab the list of values for given digit bucket 
        bucket_arr=length_dict[key]
        #split elements into top and bottom halves and group bottom halves to top halves
        top_dict,top_min,top_max,odd=setup_top_halves(bucket_arr)
        #sort the bottom halves and reconnect them to their matching top halves
        top_dict=process_bottom_halves(top_dict,odd)
        #sort the top halves
        sorted_group=sort_top_halves(top_dict,top_min,top_max)
        #concatante sorted results into a sorted array of the digit bucket
        sorted_array+=sorted_group
        
        if reporting==True:
            print(f"Group {key}, sorted in group: {len(sorted_group)} -- total sorted so far {len(sorted_array)} -- time taken for group: {time.time()-group_start}")
    
    return sorted_array
       
####################################################################################################

def setup_top_halves(arr):
    """
    info here
    """
      
    group_start_time=time.time()
    top_dict={}
    
    #Setup range max/min corner cases depending on whether there is an even or odd number of digits
    corner=str(arr[0])
    if len(corner)%2==0:
        corner=corner[0:len(corner)//2]
    else:
        corner=corner[0:len(corner)//2+1]

    top_min,top_max=corner,corner

    #Create the decimal portion range library
    for val in arr:
        #Turn every ele into a string
        str_val=str(val)
        #divide the string in half, always taking the larger half first
        if len(str_val)%2==0:
            #use the top half for the key
            key=str_val[0:len(str_val)//2]
            #use the bottom half for the values
            value=str_val[len(str_val)//2:]
            odd=False
        else:
            #When odd, +1 index to get the larger half for the key
            key=str_val[0:len(str_val)//2+1]
            value=str_val[len(str_val)//2+1:]
            odd=True

        #Insert the keys and fill in the values
        if key in top_dict:
            #test_dict[key].append(int(str(val)[len(str(val))//2:]))
            top_dict[key].append(int(value))
        else:
            #test_dict[key]=[int(str(val)[len(str(val))//2:])]
            top_dict[key]=[int(value)]
        
        #get the max/min for the range
        if key > top_max:
            top_max=key
        if key < top_min:
            top_min=key

    #calculate the range
    range_=int(top_max)-int(top_min)+1
    
    return top_dict,top_min,top_max,odd

####################################################################################################

def process_bottom_halves(top_dict,odd):
    """
    info here
    """
    
    #For every digit bucket, sort every top-half's bottom halves
    for key in top_dict:
        #get a dictionary of the bottom halves
        bottom_dict,bottom_min,bottom_max=create_bottom_dictionary(top_dict,key)
        #use the dictionary of bottom halves and the range of the bottom halves to sort them
        top_dict[key]=sort_bottom_halves(bottom_dict,key,bottom_min,bottom_max,odd)
    
    return top_dict

####################################################################################################

def create_bottom_dictionary(top_dict,key):
    """
    info here
    """
    
    bottom_dict={}
    
    #min/max corner cases for range
    bottom_min,bottom_max=top_dict[key][0],top_dict[key][0]
    
    #for every top half, make a dictionary of it's bottom halves
    for val in top_dict[key]:
        if val in bottom_dict:
            bottom_dict[val]+=1
        else:
            bottom_dict[val]=1
        #get the range of the bottom halves
        if val > bottom_max:
            bottom_max=val
        if val < bottom_min:
            bottom_min=val

    return bottom_dict,bottom_min,bottom_max

####################################################################################################

def sort_bottom_halves(bottom_dict,key,bottom_min,bottom_max,odd):
    """
    info here
    """

    bottom_sorted_array=[]
    
    #Use the bottom-halves range along with their dictionary to sort them
    for i in range(bottom_min,bottom_max+1):
        #find each spot in the range attempt to find a matching bottom-half in the dictionary
        if i in bottom_dict:
            #If dealing with decimal places, add leading zeros as necessary
            str_val=str(i)
            if odd==True:
                str_val='0'*(len(key)-1-len(str_val))+str_val
            else:
                str_val='0'*(len(key)-len(str_val))+str_val

            #reattach every bottom-half to its top-half, then add all instances into a sorted array
            bottom_sorted_array+=([int(f"{key}{str_val}")]*bottom_dict[i])
    
    return bottom_sorted_array

####################################################################################################

def sort_top_halves(top_dict,top_min,top_max):
    """
    info here
    """
    
    sorted_array=[]
    
    #for every spot in the top-halve's range, attempt to find a matching key in the dict 
    for i in range(int(top_min), int(top_max)+1): 
        if str(i) in top_dict:
            #concatanate all top-halves into a sorted_array for the bucket
            sorted_array+=(top_dict[str(i)])
    
    return sorted_array
####################################################################################################

#%%

