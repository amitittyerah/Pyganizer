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