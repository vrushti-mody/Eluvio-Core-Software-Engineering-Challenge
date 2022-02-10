# Finds the longest strand of bytes that is identical between two or more files

from collections import defaultdict
import os

# dir location where all the sample files are stored
data_dir = './'

samples_prefix = 'sample.'

sample_files = []
# Read all files starting with 'sample.' prefix in the samples directory 
for file in os.listdir(data_dir):
    if file.startswith(samples_prefix):
    	sample_files.append(data_dir + file)


# Global params 
longest_len = 0
longest_strands = []
longest_strand_files = defaultdict(lambda: set())
longest_strand_offsets = defaultdict(lambda: [])
offsets_dict = defaultdict(lambda: set())


# Function to compare two strings and return position and length of longest common substrings
def longest_common_substring(str1, str2):
    N = len(str1)
    M = len(str2)

    pos = []
    lcs_dp = [[0 for x in range(M+1)] for y in range(N+1)]
    mx = 0
    for i in range(N + 1):
        for j in range(M + 1):
            if (i == 0 or j == 0):
                lcs_dp[i][j] = 0
            elif (str1[i-1] == str2[j-1]):
                lcs_dp[i][j] = lcs_dp[i-1][j-1] + 1
                if lcs_dp[i][j] > mx:
                    pos = []  
                if lcs_dp[i][j] >= mx:
                    pos.append([i, j])
                    mx = max(mx, lcs_dp[i][j])
            else:
                lcs_dp[i][j] = 0
    return mx, pos



for i in range(len(sample_files)):
	for j in range(len(sample_files)):
		print('looping', i, j) # log
		if i >= j:
			continue

		file1 = open(sample_files[i], "rb")
		file2 = open(sample_files[j], "rb")
		str1 = file1.read()
		str2 = file2.read()

		# Optimization to skip LCS computation for some cases
		if len(str1) < longest_len or len(str2) < longest_len:
			continue 


		current_longest_len, ending_positions = longest_common_substring(str1, str2)
		if current_longest_len < longest_len :
			continue 
		elif current_longest_len == longest_len :
			current_longest_strands = []
			current_strand = None
			for ep in ending_positions:
				current_strand = str1[ep[0]-current_longest_len : ep[0]] 
				longest_strands.append(current_strand)
				longest_strand_files[current_strand].add(i+1)
				longest_strand_files[current_strand].add(j+1)
				longest_strand_offsets[current_strand].append(( i+1, j+1 ,ep))
				offsets_dict[current_strand].add((sample_files[i], ep[0]))
				offsets_dict[current_strand].add((sample_files[j], ep[1]))
		else:
			longest_len = current_longest_len
			longest_strands = []
			longest_strand_files = defaultdict(lambda: set())
			longest_strand_offsets = defaultdict(lambda: [])
			for ep in ending_positions:
				current_strand = str1[ep[0]-current_longest_len : ep[0]] 
				longest_strands.append(current_strand)

				longest_strand_files[current_strand].add(i+1)
				longest_strand_files[current_strand].add(j+1)
				longest_strand_offsets[current_strand].append(( i+1, j+1 ,ep))
				offsets_dict[current_strand].add((sample_files[i], ep[0]))
				offsets_dict[current_strand].add((sample_files[j], ep[1]))

		ending_positions = None
		pos = None


# print results

# Length of the longest strand(s) 
# - note there can be multiple strands of this maximum length 
print('\nLength of the longest common strand is: ' + str(longest_len))

print('Total number of longest strands is: ' + str(len(longest_strand_offsets)))

# File names where each of the longest strands appear
print('\nFile names where each of the longest strands appear')
strand_idx = 0
for strand in longest_strand_offsets.keys():
	strand_idx += 1

	print('\nunique strand: ' + str(strand_idx))
	for list_item in offsets_dict[strand]:
		file_iden = 'sample.' + str(list_item[0])
		final_offset = str(list_item[1])
		# second_file = 'sample.' + str(list_item[1])
		# first_file_offset = str(list_item[2][0] - longest_len)
		# second_file_offset = str(list_item[2][1] - longest_len)
		print('file : ' + file_iden[-8:] + ' | ' + 'offset : ' + final_offset )


