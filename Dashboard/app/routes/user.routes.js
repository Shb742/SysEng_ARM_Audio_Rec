module.exports = (app) => {
	const users = require('../controllers/user.controller.js');
	const auth = require('../controllers/auth.controller.js');

	// Create a new user
	app.post('/singup', [auth.checkAuth,users.singup]);

	// Update user details
	// app.post('/update', [auth.checkAuth,users.update]);

	// Get Number Of Alerts
	app.get('/countusers', [auth.checkAuth, users.count]);

	// List All Users
	app.get('/listusers', [auth.checkAuth,users.find]); 

	// Ping
	app.get('/ping', [auth.checkAuth,users.ping]);

	// Delete an user
	app.delete('/delete/:userId', [auth.checkAuth,users.delete]);

	// Login
	app.post('/login', users.login);

	// Logout
	app.get('/logout', users.logout);	
}