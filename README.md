# URL Shortener

This is a simple URL shortener fullstack app. The frontend is in HTML+CSS+Vue.js and the
backend in Python+Flask, with the database (to store the shortened URLs) is in SQLite.

Here's a quick demo (where the URL is a Google query for how to embed font-awesome icons):
![](urlShortenerDemo.gif)

To run, first:
	
	$ cd UrlShortener/SourceCode

For the server/backend:					-- Will run on port 8080

	$ cd backend

	If SQLite3 is not already installed:
		$ sudo apt-get install sqlite3
	If Flask is not installed:
		$ pip install --user flask
	If Flask-Cors is not installed:
		$ pip install --user flask_cors

	$ FLASK_APP=run.py flask run

For the client/frontend:				-- Will run on port 5000
	
	$ cd frontend

	If Node.js is not installed:
		$ curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
		$ sudo apt-get install -y nodejs
	If Vue cli is not installed:
		$ npm install -g @vue/cli

	$ cd src
	$ npm run start
