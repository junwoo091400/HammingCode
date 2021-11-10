import numpy as np

n = 2 # log2 of the one side of the square block
N = 2**(n*2) # Total block size (bits)

N_data = N - 2*n - 1 # Valid data bits
Data_test = np.random.randint(0,2,N_data)
print(Data_test)

Hamming_block = np.zeros(N, dtype=int) # The Hamming Block

'''
Example : 4 x 4 block

Mask idxs : 1, 2, 4, 8
Data idxs : 3 | 5,6,7 | 9,10,11,12,13,14,15
Zero idx : 0

'''

'''
data_idx = 0
# Go through the whole data range in the block and input the data.
for i in range(1, n*2):
    Hamming_block[2**i + 1:2**(i+1)] = Data_test[data_idx:data_idx+ 2**i - 1]
    data_idx += 2**i -1 # Update the data idx for the next data input
'''

##
# Go through the whole data, input them & calculate XOR for mask calculation
Hamming_xor = 0
Hamming_idx = 3 # Real index of the Hamming block where data will be stored
Hamming_setbit_count = 0 # For position 0 mask bit setting

# Quick function for determinining if a number is power of 2 (0 is exception)
def is_power_of_2(num):
    return (num & (num-1)) == 0

# for i in range(16):
#     print(i, is_power_of_2(i))

for data_idx in range(N_data):
    data = Data_test[data_idx]
    Hamming_block[Hamming_idx] = data # Input the data
    if data == 1:
        Hamming_xor = Hamming_xor ^ Hamming_idx # XOR the index
        Hamming_setbit_count += 1
    if(is_power_of_2(Hamming_idx + 1)):
        Hamming_idx += 2 # If we would've reached the 'Mask' idx, skip it.
    else:
        Hamming_idx += 1 # Normal case

print(Hamming_xor)

##
# Mask bit setting
for mask_idx_log in range(0, n*2):
    mask_idx = 2**mask_idx_log
    if Hamming_xor & mask_idx: # If Mask idx location bit of total XOR is set
        Hamming_block[mask_idx] = 1
        Hamming_setbit_count += 1
    else:
        Hamming_block[mask_idx] = 0

# Set the position 0 mask bit (Total parity check)
Hamming_block[0] = Hamming_setbit_count % 2

##
# Function to verify if it's a valid hamming block
def isValid_Hamming_block(block):
    block_xor = 0
    setbit_count = 0
    for block_idx in range(np.size(block)):
        if(block[block_idx]):
            block_xor ^= block_idx
            setbit_count += 1
    if block_xor == 0 and setbit_count % 2 == 0: # Position 0 bit & other mask bits are correct
        return True
    else:
        return False # 1 or more errors

print(np.reshape(Hamming_block, (2**n, 2**n)))
print(isValid_Hamming_block(Hamming_block))