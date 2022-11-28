# Custom class to hold data for each checked URL
# Contains the url, the resolved IP (if successfully resolved), and the time it took to resolve
class resolved_url:
	def __init__(self, url, ip, time_to_resolve):
		self.url = url
		self.ip = ip
		self.time_to_resolve = time_to_resolve

	# String representation function for displaying results
	def string_rep(self):
		return ("\t[Url]: %s\n\t[IP]: %s\n\t[Resolved In]: %s\n" % (self.url, self.ip, self.time_to_resolve))

	def output_csv(self):
		return ("%s,%s,%s\n") % (self.url, self.ip, self.time_to_resolve)