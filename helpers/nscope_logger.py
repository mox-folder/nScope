# Imports
import os

# Custom class to log all runtime output (including display text) to auto-generated log file
class logger:
	def __init__(self):
		self.file_path = None
		self.logged_messages = ""

	def initialize_logfile(self, start_time, directory):
		self.file_path = "%s/nScope.log" % (directory)

		if not os.path.exists(self.file_path):
			with open(self.file_path, 'w') as fp:
				fp.close()

	def log_message(self,message):
		self.logged_messages += "\n%s" % (message)

	def write_logfile(self):
		tmp_file = open(self.file_path,'w')
		tmp_file.write(self.logged_messages)
		tmp_file.close()
