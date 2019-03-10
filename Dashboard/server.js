/**
 * Import necessary modules
 */
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
const express = require('express');
const fs = require('fs');
const helmet = require('helmet');
const http = require('http');
const https = require('https');
const mongoose = require('mongoose');
const session = require('express-session');

// Load .env file. Throws error if it is not present
const dotenvResult = dotenv.config();
if (dotenvResult.error) {
    console.log('Failed to load .env (environment variables).');
    console.log('Re-running setup script will most likely fix this issue.');
    process.exit(1);
} else console.log('.env loaded.');

// Configuring the database
mongoose.Promise = global.Promise;
mongoose.set('useCreateIndex', true);
mongoose.connect(process.env.DASHBOARD_DATABASE_URL, {
    useNewUrlParser: true
}).then(() => {
    console.log('Connected to MongoDB database.');
}).catch((err) => {
    console.log('Could not connect to MongoDB database.', err);
    process.exit();
});

// Create an Express app
const app = express();

// Redirect HTTP request to HTTPS
app.use((req, res, next) => {
    if (req.secure) next();
    else res.redirect(301, `https://${req.headers.host}${req.url}`);
});

// Use Helmet to secure response headers
app.use(helmet());

// Parse requests for application/x-www-form-urlencoded and application/json
app.use(bodyParser.urlencoded({extended: true, limit: '15mb'}));
app.use(bodyParser.json({limit: '15mb'}));

// Serve static files in /root
app.use(express.static('root'));

// Mount express-session middleware to track login sessions
app.use(session({
    secret: process.env.DASHBOARD_SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        maxAge: parseInt(process.env.DASHBOARD_SESSION_COOKIE_MAXAGE),
        secure: true
    }
}));

// Load routes
require('./app/routes/alert.routes')(app);
require('./app/routes/user.routes')(app);
require('./app/routes/dictionary.routes')(app);
require('./app/routes/static.routes')(app);


// Define a local variable within Express app instance for dictionary
app.locals.dictionary = process.env.DASHBOARD_DICTIONARY;


// Creates HTTP and HTTPS server
http.createServer(app).listen(process.env.DASHBOARD_HTTP_PORT, () => {
    console.log(`HTTP server is listening on port ${process.env.DASHBOARD_HTTP_PORT || 80}.`);
});
const https_options = {
    key: fs.readFileSync(process.env.DASHBOARD_TLS_PRIVATE_KEY),
    cert: fs.readFileSync(process.env.DASHBOARD_TLS_CERTIFICATE)
};
https.createServer(https_options, app).listen(process.env.DASHBOARD_HTTPS_PORT, () => {
    console.log(`HTTPS server is listening on port ${process.env.DASHBOARD_HTTPS_PORT || 443}.`);
});
