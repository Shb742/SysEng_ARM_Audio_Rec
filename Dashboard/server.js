const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

// create express app
const app = express();

// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true ,limit:'15mb' }));

// parse requests of content-type - application/json
app.use(bodyParser.json({limit:'15mb'}));


// Configuring the database
const dbConfig = require('./config/database.config.js');

// create connection to database
// the mysql.createConnection function takes in a configuration object which contains host, user, password and the database name.
const db = mysql.createConnection (dbConfig);
// connect to database
db.connect((err) => {
    if (err) {
        console.log('Could not connect to the database.', err);
        process.exit();
    }
    console.log('Connected to database');
});
global.db = db;



// Require Alert routes
require('./app/routes/alert.routes.js')(app);




// define a simple route
app.get('/', (req, res) => {
	// res.sendFile('home.html', {root : __dirname});
	//res.render('home.html');
	 res.json({"message": "Welcome to the Dashboard for EDVS!"});
	// res.writeHeader(200, {"Content-Type": "text/html"});  
	// res.write("<h1>hi</h1>");
	// res.end();
});

// listen for requests
app.listen(3000, () => {
	console.log("Server is listening on port 3000");
});