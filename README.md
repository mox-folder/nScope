# nScope
Stop manually checking your scope files.

## About
Python script used to compare URLs and sub-domains found during EPT engagements to a pre-defined scope list. 

Relies on two external files: in-scope-ips.txt and urls-to-check.txt. Populate both accordingly and run the script. 

The script attempts to resolve each found URL to its underlying IP address and then, if the URL successfully resolved, checks it against the provided, scoped IPs. 

It also times everything which is useful for determining if any given URL should be retried manually or to set expectations for how long it takes to communicate with a given host if it is in scope and you start scanning it.

**Note**: Output & Logs from each run are stored in a working directory created in the current directory with the nomenclature of `./$Starting_Timestamp$_nscope/`.

## Usage
```
usage: nscope.py [-h] [-ips IPS] [-urls URLS] [-v] [-o {all,matches,urls}] [-l]

Stop manually checking your scope files.

options:
  -h, --help            show this help message and exit
  -ips IPS              Filepath for in-scope ips (format: 1 IP per line, no commas); default=.\in-scope-ips.txt
  -urls URLS            Filepath for URLs to check (format: 1 URL per line, no commas); default=.\urls-to-check.txt
  -v                    Display all results after running, even exhausted URLs.
  -o {all,matches,urls}
                        Output results to file based on selected option; currently only supports csv (1 per line) format; default = no output; all=Log successful matches
                        *and* exhausted urls to respective files; matches=Log only successful matches to file; urls=Log only exhausted urls to file
  -l                    Log all output, including displayed text, to a log file. Helpful for documenting timestamped proof-of-work.
```

## Example
Below is a screenshot of an example use-case of using nScope. 

For the example, the content of in-scope-ips.txt is:
```Text
64.233.176.100
8.8.8.8
172.253.124.100  
```

For the example, the content of urls-to-check.txt is:
```Text
google.com
tesla.com
```
![nScope example use](https://github.com/mox-folder/nScope/blob/main/nscopeExample.png)

## ToDo
- User input sanitization 
