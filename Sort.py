import random
import time

def create_random_array(N):
    arr = []
    for _ in range(N):
        arr.append(random.randint(1, 1000000))
    return arr

import threading
import heapq

def heap_sort(arr):
    heap = []

    for num in arr:
        heapq.heappush(heap, num)

    sorted_arr = []
    while heap:
        sorted_arr.append(heapq.heappop(heap))

    return sorted_arr

def k_way_merge(arrays):
    result = []
    heap = []

    # Initialize the heap with the first element from each array
    for i, array in enumerate(arrays):
        if len(array) > 0:
            heapq.heappush(heap, (array[0], i, 0))

    while heap:
        value, array_index, element_index = heapq.heappop(heap)
        result.append(value)

        if element_index + 1 < len(arrays[array_index]):
            next_element = arrays[array_index][element_index + 1]
            heapq.heappush(heap, (next_element, array_index, element_index + 1))

    return result

def parallel_sorting(arr):
	subarrays = [arr[i:i+int(len(arr)/8)] for i in range(0, len(arr), int(len(arr)/8))]
	threads = []
	# Sort each subarray using dual pivot quicksort
	for i in range(len(subarrays)):
		t = threading.Thread(target = heap_sort,args=(subarrays[i],))
		t.start()
		threads.append(t)

	for t in threads:
		t.join()
	
	# Merge the sorted subarrays using k-way merge
	return k_way_merge(subarrays)

# Driver code 
size = 100000
arr = create_random_array(size)
s = time.time_ns()
arr = parallel_sorting(arr)
e = time.time_ns()
print("Sorted", size ,"elements in:",(e-s)/10**9)