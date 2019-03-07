module.exports = (app) => {

    const users = require('../controllers/user.controller.js');
    const auth = require('../controllers/auth.controller.js');

    // Create a new user
    app.post('/signup', [auth.checkAuth, users.signup]);

    // Update user details
    // app.post('/update', [auth.checkAuth,users.update]);

    // Get Number Of Alerts
    app.get('/countusers', [auth.checkAuth, users.count]);

    // Get number of devices
    app.get('/countdevices', [auth.checkAuth, users.countdevices]);

    // List All Users
    app.get('/listusers', [auth.checkAuth, users.find]);

    // List Devices
    app.get('/listdevices', [auth.checkAuth, users.findDevices]);

    // Ping
    app.get('/ping', [auth.checkAuth, users.ping]);

    // Delete an user
    app.delete('/delete/:userId', [auth.checkAuth, users.delete]);

    // Log in
    app.post('/login', users.login);

    // Log out
    app.get('/logout', users.logout);
};
