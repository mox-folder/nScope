# nScope
Stop manually checking your scope files.

## About
Python script used to compare URLs found during EPT engagements to a pre-defined scope list. Relies on two external files (for now): in-scope-ips.txt and urls-to-check.txt. Populate both accordingly and run the script. The script attempts to resolve each found URL to its underlying IP address and then, if the URL successfully resolved, checks it against the provided, scoped IPs. It also times everything which is useful for determining if any given URL should be retried manually or to set expectations for how long it takes to communicate with a given host if it is in scope and you start scanning it.

## Usage
Until I get around to implementing CLI arguments, you can just run `python3 nscope.py` provided you've created your in-scope-ips.txt and urls-to-check.txt files.

If you haven't made those files: the expected format is simply a text file with either one IP or one URL per line, no commas or extra characters.

## ToDo
- Implement args parsing
- Add flags n stuff?
