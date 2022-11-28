# Imports
import argparse, os, socket, sys
from datetime import datetime
from helpers.nscope_logger import logger
from helpers.resolved_url import resolved_url

# Global level vars
args = None
logger = logger()
logging_enabled = False
in_scope_ips = []
urls_to_check = []
resolved_urls_in_scope = []
exhausted_urls = []
start_time = None
end_time = None
directory = None

# Defines command line arguments and returns the initialized parser object
def init_parser():
	# Set up argument parsing
	parser = argparse.ArgumentParser(description = "Stop manually checking your scope files.")

	parser.add_argument("-ips",
		help = "Filepath for in-scope ips (format: 1 IP per line, no commas); default=.\\in-scope-ips.txt",
		type=str,
		default="in-scope-ips.txt",
		action="store")

	parser.add_argument("-urls",
		help = "Filepath for URLs to check (format: 1 URL per line, no commas); default=.\\urls-to-check.txt",
		type=str,
		default="urls-to-check.txt")

	parser.add_argument("-v",
		help = "Display all results after running, even exhausted URLs.",
		action="store_true")

	parser.add_argument("-o",
		help = "Output results to file based on selected option; currently only supports csv (1 per line) format; default = no output; all=Log successful matches *and* exhausted urls to respective files; matches=Log only successful matches to file; urls=Log only exhausted urls to file",
		choices=["all","matches","urls"],
		default="None")

	parser.add_argument("-l",
		help = "Log all output, including displayed text, to a log file. Helpful for documenting timestamped proof-of-work.",
		action="store_true")

	return parser

# Reads lines from a file and removes extraneous characters (such as \n) from each line 
# Returns a list [] of lines from the provided file
def read_file_and_strip_lines(infile):
	tmp_file = open(infile,'r')
	tmp_lines = tmp_file.readlines()
	tmp_file.close()
	lines = []
	for line in tmp_lines:
		lines.append(line.strip())
	return lines

def xprint(message):
	if (logging_enabled):
		logger.log_message(message)
	print(message)

def check_urls():
	# Loop through each url, time logic for each url, attempt to resolve the URL to an IP, and log the results
	# On error (i.e. a URL fails to resolve) display error and continue
	for url in urls_to_check:
		xprint('\t[*] Attempting to resolve %s to IP...' % (url))
		try:
			resolve_start = datetime.now()
			tmp_ip = socket.gethostbyname(url)
			resolve_delta = datetime.now() - resolve_start
			if tmp_ip in in_scope_ips:
				xprint("\t[+] Match found: IP %s for url %s is in scope!" % (tmp_ip,url))
				resolved_urls_in_scope.append(resolved_url(url, tmp_ip, resolve_delta))
			else:
				xprint('\t[-] Resolved IP %s for url %s is not in scope.' % (tmp_ip, url))
				exhausted_urls.append(resolved_url(url,None,resolve_delta))
		except:
			xprint("\t[!] Error resolving URL: %s; passing!" % (url))
			exhausted_urls.append(resolved_url(url,None,resolve_delta))
			pass

def display_results():
	# Set the end time, get overall run time, determine number of successful scope matches and overall success rate
	end_time = datetime.now()
	delta = end_time - start_time
	matches = len(resolved_urls_in_scope)
	success_rate = matches/len(urls_to_check)

	# Display runtime and findings to user
	xprint('\n[*] Completed @ %s; Runtime: %s' % (end_time,delta))
	xprint('[*] Found %s scope matches; Success rate: %s' % (matches, success_rate))

	# Display matched URL data
	if len(resolved_urls_in_scope) > 0:
		xprint('\n[*] Matches data:')
		for url in resolved_urls_in_scope:
			xprint(url.string_rep())

	if args['v']:
		# Display exhausted (i.e. not-matching) URL data
		xprint('\n[!] Exhausted URL data:')

		if len(exhausted_urls) > 0:
			for url in exhausted_urls:
				xprint(url.string_rep())

def output_matches():
	if len(resolved_urls_in_scope) > 0:
		xprint("[*] Valid matches found; logging to file.")
		filename = "%s/nscope_matched_urls.txt" % (directory)
		with open(filename,'w') as file:
			file.write("URL,IP,ResolveTime\n")
			for url in resolved_urls_in_scope:
				file.write(url.output_csv())
			file.close()
	else:
		xprint("\n[!] No resolved URLs to log to file; skipping!\n")

def output_exhausted_urls():
	if len(exhausted_urls) > 0:
		xprint("[*] Exhausted URLs found; logging to file.")
		filename = "%s/exhausted_urls.txt" % (directory)
		with open(filename,'w') as file:
			file.write("URL,IP,ResolveTime\n")
			for url in exhausted_urls:
				file.write(url.output_csv())
			file.close()
	else:
		xprint("\n[!] No exhausted URLs to log to file; skipping!")

def output_results():
	if args['o'] == "all":
		output_matches()
		output_exhausted_urls()
	elif args['o'] == "matches":
		output_matches()
	elif args['o'] == "urls":
		output_exhausted_urls()

# Main logic
if __name__ == "__main__":

	# Init args parser and parse CLI args (if any)
	parser = init_parser()
	args = vars(parser.parse_args())

	# Set the start time and print a simple banner
	start_time = datetime.now()

	# Set up working directory for output and/or logging
	if args['l'] or args['o'] in ['all','matches','urls']:
		directory = ("%s_nscope") % (start_time.isoformat(sep=" ", timespec="seconds").replace(' ','_'))
		if not os.path.exists(directory):
			os.makedirs(directory)

	# Set up logger according to provided args
	logging_enabled = args['l']
	if logging_enabled:
		logger.initialize_logfile(start_time,directory)

	xprint("====\tnScope\t====\n\nStarted @ %s" %(start_time))

	# Read IPs and URLs from files and initialize lists for results
	in_scope_ips = read_file_and_strip_lines(args['ips'])
	urls_to_check = read_file_and_strip_lines(args['urls'])

	# Display relevant information
	xprint("[*] Loaded %s in-scope IPs\n[*] Loaded %s urls to check if in-scope" % (len(in_scope_ips), len(urls_to_check)))

	check_urls()
	display_results()
	output_results()

	# Quit gracefully
	if logging_enabled:
		logger.write_logfile()
	sys.exit(0)
