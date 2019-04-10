//Imports
const express = require('express');
var session = require('express-session');
const bodyParser = require('body-parser');
require('dotenv').config()//load .env files
var https = require('https');
var http = require('http');
var fs = require('fs');
//Imports*


//HTTPS
const ports = [80,443];
var sslkey = fs.readFileSync('./config/ssl/ssl-key.pem');
var sslcert = fs.readFileSync('./config/ssl/ssl-cert.pem')
var credentials = {
    key: sslkey,
    cert: sslcert
};


// create express app
const app = express();

// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true ,limit:'15mb' }));

// parse requests of content-type - application/json
app.use(bodyParser.json({limit:'15mb'}));


//use sessions for tracking logins
app.use(session({
  secret: (process.env.SESSION_SECRET || '075nV3JbOlgSV7rPGzajyAXQIw4NeXA12bfSzKj'),
  resave: true,
  saveUninitialized: false,
  cookie: { maxAge: 3600000,secure: true }
}));


// Configuring the database
const dbConfig = require('./config/database.config.js');
const mongoose = require('mongoose');

mongoose.Promise = global.Promise;

// Connecting to the database
mongoose.set('useCreateIndex', true);
mongoose.connect(dbConfig.url, {
	useNewUrlParser: true
}).then(() => {
	console.log("Successfully connected to the database");
}).catch(err => {
	console.log('Could not connect to the database.', err);
	process.exit();
});


//Force HTTPS
const forceSecure = function(req, res, next) {
	if (req.secure) {
		// Already https; don't do anything special.
		next();
	}
	else {
		// Redirect to https.
		res.redirect('https://' + req.headers.host + req.url);
	}
};
app.use(forceSecure);

// // Require Alert routes
require('./app/routes/alert.routes.js')(app);

// // Require User routes
require('./app/routes/user.routes.js')(app);

//For the startic files
app.use(express.static('root'));


var httpServer = http.createServer(app);
httpServer.listen(ports[0]);

var httpsServer = https.createServer(credentials,app);
httpsServer.listen(ports[1], () => {
	console.log("Server is listening");
});
