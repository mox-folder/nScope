# Imports
import requests, sys, socket
from datetime import datetime

scope_file = "in-scope-ips.txt"
check_file = "urls-to-check.txt"

class resolvedUrl:
	def __init__(self, url, ip, time_to_resolve):
		self.url = url
		self.ip = ip
		self.time_to_resolve = time_to_resolve

	def string_rep(self):
		return ("\t[Url]: %s\n\t[IP]: %s\n\t[Resolved In]: %s\n" % (self.url, self.ip, self.time_to_resolve))

def read_file_and_strip_lines(infile):
	tmp_file = open(infile,'r')
	tmp_lines = tmp_file.readlines()
	tmp_file.close()
	lines = []
	for line in tmp_lines:
		lines.append(line.strip())
	return lines


if __name__ == "__main__":
	start = datetime.now()
	print("====\tnScope\t====\n\nStarted @ %s" %(start))

	in_scope_ips = read_file_and_strip_lines(scope_file)
	urls_to_check = read_file_and_strip_lines(check_file)
	resolved_urls_in_scope = []
	exhausted_urls = []

	print ("[*] Loaded %s in-scope IPs\n[*] Loaded %s urls to check if in-scope" % (len(in_scope_ips), len(urls_to_check)))

	for url in urls_to_check:
		print('\t[*] Attempting to resolve %s to IP...' % (url))
		try:
			resolve_start = datetime.now()
			tmp_ip = socket.gethostbyname(url)
			resolve_delta = datetime.now() - resolve_start
			if tmp_ip in in_scope_ips:
				print("\t[+] Match found: IP %s for url %s is in scope!" % (tmp_ip,url))
				resolved_urls_in_scope.append(resolvedUrl(url, tmp_ip, resolve_delta))
			else:
				print('\t[-] Resolved IP %s for url %s is not in scope.' % (tmp_ip, url))
				exhausted_urls.append(resolvedUrl(url,None,resolve_delta))
		except:
			print("\t[!] Error resolving URL: %s; passing!" % (url))
			exhausted_urls.append(resolvedUrl(url,None,resolve_delta))
			pass

	end = datetime.now()
	delta = end - start
	matches = len(resolved_urls_in_scope)
	success_rate = matches/len(urls_to_check)

	print('\n[*] Completed @ %s; Runtime: %s' % (end,delta))
	print('[*] Found %s scope matches; Success rate: %s' % (matches, success_rate))
	print('\n[*] Matches data:')

	if len(resolved_urls_in_scope) > 0:
		for url in resolved_urls_in_scope:
			print(url.string_rep())

	print('\n[!] Exhausted URL data:')

	if len(exhausted_urls) > 0:
		for url in exhausted_urls:
			print(url.string_rep())

	sys.exit(0)
