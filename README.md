# nScope
Stop manually checking your scope files.

## About
Python script used to compare URLs found during EPT engagements to a pre-defined scope list. Relies on two external files (for now): in-scope-ips.txt and urls-to-check.txt. Populate both accordingly and run the script. The script attempts to resolve each found URL to its underlying IP address and then, if the URL successfully resolved, checks it against the provided, scoped IPs. It also times everything which is useful for determining if any given URL should be retried manually or to set expectations for how long it takes to communicate with a given host if it is in scope and you start scanning it.

## Usage
// todo

## ToDo
- Implement args parsing
- Add flags n stuff?
