# A simple API to get the Start and End dates and SANs (if any) of a certificate

import flask
from flask import request, jsonify
from socket import socket
import ssl
import M2Crypto

# Create Flask application object
app = flask.Flask(__name__)

# To see errors if error in code
# Otherwise will see generic Bad Gateway message in browser
app.config["DEBUG"] = True

# http://127.0.0.1:5000/ 
@app.route('/', methods=['GET'])
def home():
        return '''<h1>API for SSL Certificates</h1>
        <p>A simple API for getting dates and SAN names from an HTTPS web site</p>'''

# http://127.0.0.1:5000/api/v1/sslcert/getsubject  - will generate an error
# http://127.0.0.1:5000/api/v1/sslcert/getsubject?website=www.fiserv.com  - to pass a website
@app.route('/api/v1/sslcert/getsubject', methods=['GET'])
def api_subject():
    # Check if an website was provided as part of the URL.
    # If website is provided, assign it to a variable.
    # If no website is provided, display an error in the browser.
    if 'website' in request.args:
        website = request.args['website']
    else:
        return "Error: No website field provided. Please specify a website."

    try:
        cert = ssl.get_server_certificate((website,443))
    except:
        return website + " is not an https website"
    
    x509 = M2Crypto.X509.load_cert_string(cert)
    try:
        subject = x509.get_subject().as_text()
    except:
        return "having issue getting subject info"

    subject_name = {}
    subject_name.update({'Subject Name':subject})

    return jsonify(subject_name)

# To get Not Before and Not After dates
# example:
# http://127.0.0.1:5000/api/v1/sslcert/getdates?website=www.fiserv.com
@app.route('/api/v1/sslcert/getdates', methods=['GET'])
def api_dates():
    # Check if an website was provided as part of the URL.
    # If website is provided, assign it to a variable.
    # If no website is provided, display an error in the browser.
    if 'website' in request.args:
        website = request.args['website']
    else:
        return "Error: No website field provided. Please specify a website."

    try:
        cert = ssl.get_server_certificate((website,443))
    except:
        return website + " is not an https website"

    x509 = M2Crypto.X509.load_cert_string(cert)

    not_before_date = x509.get_not_before()
    not_after_date = x509.get_not_after()

    cert_dates = {}
    cert_dates.update({'Not Before Date': str(not_before_date)})
    cert_dates.update({'Not After Date': str(not_after_date)})

    return jsonify(cert_dates)

# To get list of SANs (if any) from certificate
# http://127.0.0.1:5000/api/v1/sslcert/getsans?website=www.fiserv.com
@app.route('/api/v1/sslcert/getsans', methods=['GET'])
def api_sans():
    # Check if an website was provided as part of the URL.
    # If website is provided, assign it to a variable.
    # If no website is provided, display an error in the browser.
    if 'website' in request.args:
        website = request.args['website']
    else:
        return "Error: No website field provided. Please specify a website."

    try:
        cert = ssl.get_server_certificate((website,443))
    except:
        return website + " is not an https website"

    x509 = M2Crypto.X509.load_cert_string(cert)

    try:
        san = x509.get_ext('subjectAltName')
    except:
        return website + " has no Subject Alt Names"

    san_names = {}
    san_names.update({'Subject Alt Names': san.get_value()})

    return jsonify(san_names)

# Runs the application
app.run()
