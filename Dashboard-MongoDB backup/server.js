const express = require('express');
const bodyParser = require('body-parser');

// create express app
const app = express();

// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true ,limit:'15mb' }));

// parse requests of content-type - application/json
app.use(bodyParser.json({limit:'15mb'}));


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