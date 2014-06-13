from os import listdir, rename
from os.path import isfile, join, isdir
import sys
import re
import operator

VIDEO_EXTS = ['mp4', 'wmv', 'flv', 'avi', 'mkv']
WORD_OCCURANCES = {}
LAST_NUM = 0
EPISODES = {}

class Episode:
	'''
		Episode object
	'''
	def __init__(self, parts, ext):
		self.parts = parts
		self.ext = ext
		self.__identify_episode_number()

	def get_file_name(self, prefix):
		return '%s %s.%s' % (prefix, self.episode_number, self.ext)

	def __unicode__(self):
		print self.episode_number

	def __identify_episode_number(self):
		global LAST_NUM
		ints = [part for part in self.parts if part.isdigit()]
		print "%s : %s" % (ints, self.parts)
		if len(ints) == 1:
			self.episode_number = int(ints[0])
		else:
			min_diff = 0
			suspect = 0
			for ep_suspect in ints:
				diff = int(ep_suspect) - LAST_NUM
				if suspect == 0 or (min_diff > diff and diff > 0 and ep_suspect != 0):
					min_diff = diff
					suspect = ep_suspect
			self.episode_number = int(suspect)
		LAST_NUM = self.episode_number

def get_name_input():
	'''
		Grab the new file name format from the user
	'''
	WAITING = False
	while not WAITING:
		new_name_maker = raw_input("Enter the new name : ")
		new_name_marker_indices = new_name_maker.split()
		new_name = ' '.join([sorted_occurances[int(name_index)][0] for name_index in new_name_marker_indices])
		print new_name
		WAITING = raw_input("Is this ok? (y/n)") == "y"
	return new_name

def clean(file_name):
	'''
		Clean up the file name. Remove multiple spaces
	'''
	return re.sub(r'\([^)]*\)', '', file_name)

def breakdown(file_name):
	'''
		Breakdown the file name and filter out non-video ones
	'''
	global WORD_OCCURANCES
	file_name_parts = file_name.split('.')
	file_name_renamed = ''.join(file_name_parts[:-1])
	file_ext = file_name_parts[-1]
	
	# Only if they are video files
	if file_ext not in VIDEO_EXTS:
		return False

	# Clean up the file name
	file_name_renamed = clean(file_name_renamed)

	pattern = re.compile(r"[_]")
	file_name_arr = pattern.split('_'.join(file_name_renamed.split()))

	for part in file_name_arr:
		if part in WORD_OCCURANCES:
			WORD_OCCURANCES[part] += 1
		else:
			WORD_OCCURANCES[part] = 1
	
	EPISODES[file_name] = Episode(file_name_arr, file_ext)

# Grab all the files in the specified directory
folder_path = sys.argv[1]
if not isdir(folder_path):
	print "Err > Folder not found"
	sys.exit()
files_in_directory = [file for file in listdir(folder_path) if isfile(join(folder_path, file))]
num_files_in_directory = len(files_in_directory)
print "Info > There are %s files in this directory " % (num_files_in_directory)

# We are interested in getting the name of the series and the episode
for file in files_in_directory:
	file_parts = breakdown(file)

# Sort the work occurances
sorted_occurances = sorted(WORD_OCCURANCES.iteritems(), key=operator.itemgetter(1), reverse=True)


# More than halfway there ;) 
# Now, lets show the user a numbered list of word occurances so that the user can create his own filename
for index, value in enumerate(sorted_occurances):
	if value[1] > 5:
		print '%s - %s' % (index, value)

# Get the new name format
new_name_format = get_name_input()
print "\n\n\nNew name received as %s\n\n" % (new_name_format)

# Iterate through the new episode names and rename them
for fname, episode in EPISODES.iteritems():
	new_name = episode.get_file_name(new_name_format)
	print '%s ----> %s\n' % (fname, new_name)
	new_path = join(folder_path, new_name)
	old_path = join(folder_path, fname)
	
	if not isfile(new_path):
		rename(old_path, new_path)