# groupSort

# 1. Overview  
A sorting algorithm that uses hash tables and range to approach a O(n) time complexity.  

# 2. Basic groupSort

## 2.1 Technical Description  

The base-level implementation of groupSort works on integers and uses two for loops.

### 2.1.1 Loop over Array

#### Time Complexity of Step

O(n), where n is the <ins>number of elements</ins> in the array

#### Step Logic

The first for loop looks at each element in the unsorted array, creating keys in a hash table  
for each unique element and increasing the count of a given key's value for every instance found.  
It also keeps track of the minimum and maxium values in the unsorted array to determine the range.  
Additionally, it checks to see if the array is already sorted as it goes along.

### 2.1.2 Loop over Range

#### Time Complexity of Step

O(m), where m is the <ins>size of the range</ins>

#### Step Logic

The range is used to impose a sequential order onto the keys of the hashtable.  
Looping over the range, if a matching key is found in the hash table,   
the total instances of the key (stored in the key's value) are populated into an array.  
As this process occurs for each spot in the range an ordered array is built,  
which upon completion of the loop, is a sorted version of the original array.

### 2.1.3 Final Time Complexity

The overall time complexity of the algorithm is max(O(n), O(m))

## 2.2 Limitations

### 2.2.1 Range

The range of the elements in the unsorted array can vary signficantly from the number of elements.  
Because of this, the range determines whether this approach is actually faster or slower than other algorithms.  
If the range is much larger than the number of elements to be sorted, groupSort will work slowly.  
If the range is much smaller than the number of elements to be sorted, groupSort will be very fast.

In theory, we would expect the upper threshold of an appropriate range to be nlog(n), where n is the size of the array.  
In practice, due to more computationally expensive operations being done in groupSort, it's upper range threshold  
is around 2/3*nlog(n).

### 2.2.2 Integers

Since this base-level implementation of of groupSort relies only on the range to sort the keys in the hash table,  
it cannot be used to sort floats, as the range between two floating point numbers is infinite.

# 3. Extended groupSort

## 3.1 Technical Description  

The extended implementation of groupSort will work with floats when completed.  
It is expected that, between the two versions, appropariate logic for working with strings will be uncovered.  

In the current version of the extended approach,  
the integer and decimal portions of a number are separated and treated as two different sorting problems.  
Additionally, in both problem, every number is placed into a top-level grouping according to the number of digits in the number.  
This allows all the numbers in each group to be turned into strings, cut in half, with bottom-halves being grouped into top-halves.  
Then, each top-half's bottom-halves can be sorted, the top-halves sorted, and the digit-length groups sorted.  
In this way, in the end, a sorted array is produced.  

When fully extended to floats, each integer will be a key for groupings of decimals.  
After the decimal portion and the integer portions are sorted, the full numbers will be populated into an array
as the ordered integer portions are looped-over and recombined with all their matching decimal portions.

Currently I have this approach working on integers, so will only describe those steps in further detail...

### 3.1.1 Create Digit-Length Buckets

#### Time Complexity of Step

O(n), where n is the <ins>number of elements</ins> in the unsorted array

#### Step Logic

Loop over the array converting every element into a string.  
Determine the number of digits in the element.  
For every unique length of digits, create a key in a hash table with a list of elements of matching length.  
Track the largest key to use as a range for sorting these groups at the end.

### 3.1.2 For each Digit-Length Bucket, Cut Numbers in Half, Grouping Bottom-Halves to Top-Halves

#### Time Complexity of Step

O(n) -- when all operations considered

O(b), where b is the <ins>number of digit-length buckets</ins>  
O(b) consists of b \* O(i) , where i is the <ins>number of instances</ins> in each bucket  
b \* i == n

#### Step Logic

Loop over numbers in digit-length bucket, converting them into strings.  
Cut the strings in half, grouping bottom-halves with top-halves.  
Find the range of the top-halves.

### 3.1.3 Sort Bottom-Halves

#### Time Complexity of Step

O(n) -- when all operations considered

O(b), where b is the <ins>number of digit-length buckets</ins>  
O(b) consists of b \* O(th\*bh) , where th and bh are the <ins>number of top and bottom halves</ins> in each bucket  
b \* th \* bh == n

#### Step Logic

For every digit-length group, for every top-half, sort the matching bottom-halves.  
This is accomplished using the basic groupSort approach of hash table and range.

### 3.1.4 Sort Top-Halves

#### Time Complexity of Step

O(n) -- when all operations considered

O(b), where b is the <ins>number of digit-length buckets</ins>  
O(b) consists of b \* O(th), where i is the <ins>number of top-halves</ins> in each bucket  
b \* th <= n

#### Step Logic

For every digit-length group, for every top-half, sort the matching bottom-halves.  
This is accomplished using the basic groupSort approach of hash table and range.

### 3.1.5 Concatanate Sorted Digit-Length Buckets

#### Time Complexity of Step

O(b), where b is the <ins>number of digit-length buckets</ins>  
b <= n

#### Step Logic

Every digit-length group has been sorted.
Range over them from 0 to (max_bucket_length), concatanating their ordered elements into one final ordered array.

### 3.1.6 Final Time Complexity

O(n) -- reported complexity when all operations are considered

Though for completeness, looping over n happens ~4 (sequential) times and one final loop over the buckets,  
so, in detail, O(4n + b).

To explain why its it is no greater than O(n) for each step, while many different levels of operations are occuring in a step,  
ultimately there is only one operation happening for every original element in the unsorted array.  
There are no nested operations with respect to the <ins>original input</ins>.

## 3.2 Limitations

### 3.2.1 Range

As with basic groupSort, there is an upper limit to the range that the extended verions can handle  
and still not be slower than mergeSort. However, the range is now about 2.75\*nlog(n).

### 3.2.2 Unfinished Details

Currently, I am trying to work out some kinks, like dealing with leading and trailing zeros in the decimal portion.  
Additionally, I need to add in 'negative' digit-length buckets to work with negative numbers.  
Note -- that is not a problem in the basic groupSort.  

# 4. Further Ideas

Instead of dividing each digit-length bucket element in half only,  
It would be even better to recursively break them in half over and over until they are just single digits.  
Alternatively, I could achieve a simliar result by grouping each digit place.  
Presumably, this would increase the size of ranges that could be worked with,  
and speed up the sort when working with ranges larger than there are elements (m>n).  

# 5. Benchmarks

Python version used: 3.9.7  
Processor: AMD Ryzen 5 3600 6-Core Processor 3.60 GHz  
RAM: 16.0 GB  
GPU: NVIDIA GeForce RTX 2060 Super  

### 1 million elements, 100 million range, 100 iterations (~mergeSort outperforms groupSort)

<ins>mergeSort average time</ins>: **3.5218 sec**

<ins>Basic groupSort average time</ins>: **24.8557 sec**

<ins>groupSort with Digit Buckets average time</ins>: **5.3258 sec**

### 1 million elements, 55 million range, 100 iterations (~range upper limit for groupSort with Digit Buckets)

<ins>mergeSort average time</ins>: **3.2718 sec**

<ins>Basic groupSort average time</ins>: **12.9940 sec**

<ins>groupSort with Digit Buckets average time</ins>: **3.4689 sec**

### 1 million elements, 15 million range, 100 iterations (~range upper limit for Basic groupSort)

<ins>mergeSort average time</ins>: **3.3170 sec**

<ins>Basic groupSort average time</ins>: **3.8615 sec**

<ins>groupSort with Digit Buckets average time</ins>: **2.2284 sec**

### 1 million elements, 10 million range, 100 iterations

<ins>mergeSort average time</ins>: **3.4948 sec**

<ins>groupSort average time</ins>: **2.7092 sec**

<ins>groupSort with Digit Buckets average time</ins>: **2.2659 sec**

### 1 million elements, 1 million range, 100 iterations

<ins>mergeSort average time</ins>: **3.4874 sec**

<ins>groupSort average time</ins>: **0.5025 sec**

<ins>groupSort with Digit Buckets average time</ins>: **1.5846 sec**

### 1 million elements, 100 thousand range, 100 iterations

<ins>mergeSort average time</ins>: **3.4980 sec**

<ins>groupSort average time</ins>: **0.2669 sec**

<ins>groupSort with Digit Buckets average time</ins>: **1.1380 sec**

### 1 million elements, 10 thousand range, 100 iterations

<ins>mergeSort average time</ins>: **3.5301 sec**

<ins>groupSort average time</ins>: **0.1719 sec**

<ins>groupSort with Digit Buckets average time</ins>: **0.9341 sec**

