# run.py
# 
# This is the Flask backend for a URL shortener service, which stores its
# "shortened" URLs in a SQLite database, ""
#
from flask import Flask, render_template, jsonify, request, redirect
from flask_cors import CORS
import requests
from math import floor
from sqlite3 import OperationalError
import string, sqlite3
from urllib.parse import urlparse
import string

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# To create a base62 identifier for the "short URL", given the base10 row_id
def toBase62(num, b = 62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res

# To find the row_id, given the base62 identifier in the "short URL"
def toBase10(num, b = 62):
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res
    
# To check whether or not proper table exists and, if not, create it
def table_check():
    create_table = """
        CREATE TABLE WEB_URL(
        ID INTEGER PRIMARY KEY     AUTOINCREMENT,
        URL  TEXT    NOT NULL
        );
        """
    with sqlite3.connect('shorturl.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(create_table)
        except OperationalError:
            pass
    
# Route 'taken' by the 'Create short URL' button
@app.route('/api/shorten')
def shorten():
	# Check to see if table exists
	table_check()
	# Print useful debugging info and extract the relevant argument (longUrl)
	print('--- Got request to shorten ---')
	longurl = request.args['longUrl']
	print("Longurl=" + longurl)
	# Adjust its format, if necessary
	if urlparse(longurl).scheme == '':
            longurl = 'http://' + longurl
    # Connect to the database and add it to the appropiate table
	with sqlite3.connect('shorturl.db') as conn:
            cursor = conn.cursor()
            insert_row = """
                INSERT INTO WEB_URL (URL)
                    VALUES ('%s')
                """%(longurl)
            result_cursor = cursor.execute(insert_row)
            # The identifier for the "short URL" will be the row_id in base62
            encoded_string = toBase62(result_cursor.lastrowid)
    
    # Construct the new "short URL" locally as well
	short_url= 'http://localhost:5000/' + encoded_string
	# Put it in a nice JSON format
	response = { 
		'shortUrl': short_url 
	}
	# And return it
	return response

# This is the route for when we receive a request to access one of our
# "shortened" URLs, i.e. when browsing to localhost:5000/<short_url>
@app.route('/<short_url>')
def redirect_short_url(short_url):
	# Get the original row_id we are looking for (in base10)
    decoded_string = toBase10(short_url)
    print
    redirect_url = 'http://localhost:5000'
    # Connect to the database and look for the URL of this row_id
    with sqlite3.connect('shorturl.db') as conn:
        cursor = conn.cursor()
        select_row = """
                SELECT URL FROM WEB_URL
                    WHERE ID=%s
                """%(decoded_string)
        result_cursor = cursor.execute(select_row)
        try:
			# If successful, make it the URL to redirect to
            redirect_url = result_cursor.fetchone()[0]
        except Exception as e:
            print (str(e))
    # And return it
    return redirect(redirect_url)

# Routes for all other cases
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
