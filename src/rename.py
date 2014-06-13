from os import listdir, rename
from os.path import isfile, join, isdir
import sys
import re
import operator

from episode import Episode
from formats import VIDEO_EXTS

WORD_OCCURANCES = {}
EPISODES = {}
SEASONED_FLAG = False

class Rename:
	'''
		Base class
	'''
	@staticmethod
	def get_name_input(sorted_occurances):
		'''
			Grab the new file name format from the user
		'''
		WAITING = False
		while not WAITING:
			new_name_maker = raw_input("Enter the new name : ")
			new_name_marker_indices = new_name_maker.split()
			# Based on the user specified indcides, generate the new file name prefix
			new_name = ' '.join([sorted_occurances[int(name_index)][0] for name_index in new_name_marker_indices])
			print new_name
			WAITING = raw_input("Is this ok? (y/n)") == "y"
		return new_name

	@staticmethod
	def clean(file_name):
		'''
			Clean up the file name. Remove everything in between brackets
		'''
		return re.sub(r'\([^)]*\)', '', file_name)

	@staticmethod
	def breakdown(file_name):
		'''
			Breakdown the file name and filter out non-video ones
		'''
		global WORD_OCCURANCES

		# Get the file extension
		file_name_parts = file_name.split('.')
		file_name_renamed = '_'.join(file_name_parts[:-1])
		file_ext = file_name_parts[-1]
		
		# Only if they are video files. Don't care about the .DS_Store's
		if file_ext not in VIDEO_EXTS:
			return False

		# Clean up the file name
		file_name_renamed = Rename.clean(file_name_renamed)

		# Use a pattern match to split with underscores
		pattern = re.compile(r"[_]")
		# Split the filename at spaces and join with underscores
		file_name_arr = pattern.split('_'.join(file_name_renamed.split()))

		# Iterate through the parts of the file and try to see if it matches the SXEX pattern where X is an integer
		regex = re.compile("S\d+E\d+", re.IGNORECASE)
		for index, file_part in enumerate(file_name_arr):
			if regex.search(file_part):
				SEASONED_FLAG = True
				file_part = file_part.lower().replace('s', '').replace('e', '').replace('+', '')
				file_name_arr[index] = file_part

		# Increment word occurances
		for part in file_name_arr:
			if part in WORD_OCCURANCES:
				WORD_OCCURANCES[part] += 1
			else:
				WORD_OCCURANCES[part] = 1
		
		# Update the dictionary
		EPISODES[file_name] = Episode(file_name_arr, file_ext)

	def __init__(self, folder_name):
		# Grab all the files in the specified directory
		folder_path = folder_name
		# Check if the specified folder actually exists
		if not isdir(folder_path):
			print "Err > Folder not found"
			sys.exit()
		# Get all the files in the directory
		files_in_directory = [file for file in listdir(folder_path) if isfile(join(folder_path, file))]
		num_files_in_directory = len(files_in_directory)
		print "Info > There are %s files in this directory " % (num_files_in_directory)

		# We are interested in getting the name of the series and the episode number
		for file in files_in_directory:
			Rename.breakdown(file)

		# Sort the work occurances
		sorted_occurances = sorted(WORD_OCCURANCES.iteritems(), key=operator.itemgetter(1), reverse=True)

		# More than halfway there ;) 
		# Now, lets show the user a numbered list of word occurances so that the user can create his own filename
		for index, value in enumerate(sorted_occurances):
			if value[1] > 5:
				print '%s - %s' % (index, value)

		# Get the new name format
		new_name_format = Rename.get_name_input(sorted_occurances)
		print "\n\n\nNew name received as %s\n\n" % (new_name_format)

		# Iterate through the new episode names and rename them
		for fname, episode in EPISODES.iteritems():
			new_name = episode.get_file_name(new_name_format)
			print '%s ----> %s\n' % (fname, new_name)
			new_path = join(folder_path, new_name)
			old_path = join(folder_path, fname)
			
			if not isfile(new_path):
				#pass
				rename(old_path, new_path)

if __name__ == '__main__':
	Rename(sys.argv[1])