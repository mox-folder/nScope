# nScope
Stop manually checking your scope files.

## About
Python script used to compare URLs and sub-domains found during EPT engagements to a pre-defined scope list. Relies on two external files (for now): in-scope-ips.txt and urls-to-check.txt. Populate both accordingly and run the script. The script attempts to resolve each found URL to its underlying IP address and then, if the URL successfully resolved, checks it against the provided, scoped IPs. It also times everything which is useful for determining if any given URL should be retried manually or to set expectations for how long it takes to communicate with a given host if it is in scope and you start scanning it.

## Usage
Until I get around to implementing CLI arguments, you can just run `python3 nscope.py` provided you've created your in-scope-ips.txt and urls-to-check.txt files.

If you haven't made those files: the expected format is simply a text file with either one IP or one URL per line, no commas or extra characters.

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
- Implement args parsing
- Add flags: verbose mode (reflect exhausted urls), IPs file, URLs file, output successful resolutions to file, output exhausted urls to file, output all results to flies
