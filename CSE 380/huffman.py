from math import ceil, log
from pprint import pprint
from collections import Counter
from anytree import Node,RenderTree
from sympy import primerange
import numpy
import time
 
def show_results_table(message, code_table):
  total_characters = len(message)
  total_unique_characters = len(code_table)
  total_bits = 0
  for char, count, code in code_table:
    total_bits += count * len(code)
  average_bits_per_character = total_bits / total_characters
  fixed_bits_per_character = ceil(log(total_unique_characters, 2))
  total_fixed_bits = total_characters * fixed_bits_per_character
  compression_ratio = (total_fixed_bits - total_bits) / total_fixed_bits
  table = []
  table.append(['Total Characters', total_characters])
  table.append(['Total Unique Characters', total_unique_characters])
  table.append(['Total Bits', total_bits])
  table.append(['Average Bits per Character', average_bits_per_character])
  table.append(['Fixed Bits per Character', fixed_bits_per_character])
  table.append(['Total Fixed Bits', total_fixed_bits])
  table.append(['Compression Ratio', compression_ratio])
  return table
 
def create_table(elements, print_tree=False):
  elements = [[str(x) for x in item] for item in elements]#Stringify the array
  counter = Counter(x for xs in elements for x in set(xs))#Create the counter
  myList = sorted(counter, key = counter.get, reverse=False)#Initialize a sorted list of our keys
  myList = [[x] for x in myList]
 
  myNodes = {}#Used for rendering the tree
  for i in myList:
    myNodes[','.join(i)] = Node(','.join(i))
 
  table = {}#Initialize output dictionary
  for i in myList:
    table[','.join(i)] = ""
  
  for i in range(len(myList)):
    val1 = myList[0]
    val2 = myList[1]
    
    myList.remove(val1)
    myList.remove(val2)
    newVal = val1+val2
    newValFreq = counter[','.join(val1)]+counter[','.join(val2)]
 
    if print_tree:
      myNodes[','.join(newVal)] = Node(newVal)
      myNodes[','.join(val1)].parent = myNodes[','.join(newVal)]
      myNodes[','.join(val2)].parent = myNodes[','.join(newVal)]
 
    #Update dictionary
    for i in val1:
      if type(i) is str:
        table[i] = "0"+table[i]
      else:
        table[','.join(i)] = "0"+table[','.join(i)]
    for i in val2:
      if type(i) is str:
        table[i] = "1"+table[i]
      else:
        table[','.join(i)] = "1"+table[','.join(i)]
 
    counter[','.join(newVal)] = newValFreq
    for q in range(len(myList)):
      if counter[','.join(myList[q])] > newValFreq:
        myList.insert(q, newVal)
        break
      elif q == len(myList)-1:
        myList.append(newVal)
 
    if len(myList) == 0:
      myList.insert(0, newVal)
      counter[','.join(newVal)] = newValFreq
      break
 
  #Print out all the stuff
  if print_tree:
    for pre, fill, node in RenderTree(myNodes[','.join(myList[0])]):
      print("%s%s" % (pre, node.name))
 
  data = list()#Restructure the dictionary as a 2d array
  to_iter = set([item for sublist in elements for item in sublist])
  for i in to_iter:
    data.append([i, counter[i], table[i]])
    #print("%s %s %s"% (i, counter[''.join(i)], table[''.join(i)]))
  pprint(data)
  return data
 
def primesfrom3to(n):
    """ Returns a array of primes, 3 <= p < n """
    sieve = numpy.ones(n//2, dtype=numpy.bool)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = False
    return 2*numpy.nonzero(sieve)[0][1::]+1
 
list_of_gaps = []
prev = 3
gap = 0
 
starttime = time.time()
for prime in primesfrom3to(1000000)[1:]:
  list_of_gaps.append([prime-prev])
  prev = prime
  
 
pprint(show_results_table(list_of_gaps, create_table(list_of_gaps, False)))
print(time.time()-starttime)
