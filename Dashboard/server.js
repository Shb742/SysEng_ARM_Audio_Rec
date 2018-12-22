const express = require('express');
var session = require('express-session');
const bodyParser = require('body-parser');
require('dotenv').config()//load .env files

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
  cookie: { maxAge: 3600000,secure: false }
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




// // Require Alert routes
require('./app/routes/alert.routes.js')(app);

// // Require User routes
require('./app/routes/user.routes.js')(app);

//For the startic files
app.use(express.static('root'));


// define a simple route
// app.get('/', (req, res) => {
// 	// res.sendFile('home.html', {root : __dirname});
// 	//res.render('home.html');
// 	 res.json({"message": "Welcome to the Dashboard for EDVS!"});
// 	// res.writeHeader(200, {"Content-Type": "text/html"});  
// 	// res.write("<h1>hi</h1>");
// 	// res.end();
// });

// listen for requests
app.listen(3000, () => {
	console.log("Server is listening on port 3000");
});