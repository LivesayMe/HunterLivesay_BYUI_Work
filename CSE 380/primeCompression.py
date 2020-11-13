import sympy
from math import ceil, log
from pprint import pprint
from collections import Counter
from anytree import Node,RenderTree
from sympy import primerange
import numpy
import time
 
listNums = list()
def getByte(i):
    b = [0]*8
    num = 30*i
    if sympy.isprime(num+1):
        b[0] = 1
    if sympy.isprime(num-1):
        b[1] = 1
    if sympy.isprime(num+3):
        b[2] = 1
    if sympy.isprime(num-3):
        b[3] = 1
    if sympy.isprime(num+7):
        b[4] = 1
    if sympy.isprime(num-7):
        b[5] = 1
    if sympy.isprime(num+11):
        b[6] = 1
    if sympy.isprime(num+-11):
        b[7] = 1
    return b
 
def primesfrom3to(n):
    """ Returns a array of primes, 3 <= p < n """
    sieve = numpy.ones(n//2, dtype=numpy.bool)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = False
    return 2*numpy.nonzero(sieve)[0][1::]+1

#First bit indicates polarity of first set, every reminaing number indicates length of next substr
#0000011111011101
def encodeRLE(msg):
  output = [int(msg[0])]
  curBit = msg[0]
  
  lastIndex = 0
  for i in range(len(msg)):
    if msg[i] != curBit:
      curBit = "1" if curBit == "0" else "0"
      output.append(i-lastIndex)
      lastIndex = i
  return output
 
def decodeRLE(nums):
    msg = ""
    curBit = str(nums[0])
    for i in nums[1:]:
        msg += str([curBit])*i
        curBit = "1" if curBit == "0" else "0"
    return msg
 
def getCompressedPrimes(n):
    compressed = ""
    k = 0
    i = 0
    constants = [-13,-11,-7,-1,1,7,11,13]
    for prime in primesfrom3to(n)[2:]:
        while True:
            if 30*k+constants[i] == prime:
                compressed += '1'
                i += 1
                if i == 8:
                    i = 0
                    k += 1
                break
            else:
                compressed += '0'
                i += 1
                if i == 8:
                    i = 0
                    k += 1
        
    return compressed

 
def decompress(x):
    #Chop the string into bytes
    chunks, chunk_size = len(x), 8
    b = [x[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
 
    primes = list()
    constants = [-11,-7,-3,-1,1,3,7,11]
    for i in range(len(b)):
        for q in range(len(b[i])):#The current bitstring to decode
            if b[i][q] == "1":
                primes.append(30*i+constants[q])
    return primes
 
    
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
 
#First do 30k compression
n = 179424673
m = getCompressedPrimes(n)
print(len(m))
#Then RLE encode
m = encodeRLE(m)
print(len(m))
#Then huffman encode
table = create_table([[x] for x in m], False)
pprint(show_results_table(m, table))
