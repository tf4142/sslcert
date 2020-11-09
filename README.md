# sslcert
Python API for getting info from https website SSL certificate
Output is returned in JSON format.

## Installation

These instructions are written for python 3 running on a Linux server.
The assumption is made you have [Python 3](https://www.python.org/download/releases/3.0/) installed.

You may need to install these libraries if not already installed

```bash
sudo apt-get install python-dev
sudo apt-get install m2crypto
```

## Usage

To start application

```bash
python sslcert.py
```
To get Subject Name info
```bash
http://127.0.0.1:5000/api/v1/sslcert/getsubject?website=<https website>
Example:
[http://127.0.0.1:5000/api/v1/sslcert/getsubject?website=www.fiserv.com]
```

To get Not Before and Not After Dates
```bash
http://127.0.0.1:5000/api/v1/sslcert/getdates?website=<https website>
Example:
[http://127.0.0.1:5000/api/v1/sslcert/getdates?website=www.fiserv.com]
```

To get SANs (Subject Alternative Names)
```bash
http://127.0.0.1:5000/api/v1/sslcert/getsans?website=<https website>
Example:
[http://127.0.0.1:5000/api/v1/sslcert/getsans?website=www.fiserv.com]
```

## Known Issues
Will get a "No SNI provided" error when pulling Subect info for google.com

