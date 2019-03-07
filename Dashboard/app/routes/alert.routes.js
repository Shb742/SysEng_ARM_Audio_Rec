module.exports = (app) => {

    const alerts = require('../controllers/alert.controller.js');
    const auth = require('../controllers/auth.controller.js');

    // Create a new alert
    app.post('/api/alerts', [auth.checkAuth, alerts.create]);

    // Get Number Of Alerts
    app.get('/api/alerts/count/', [auth.checkAuth, alerts.count]);

    // Retrieve all alerts
    app.get('/api/alerts', [auth.checkAuth, alerts.find]);

    // Retrieve a single Alert with alertId
    app.get('/api/alerts/:alertId', [auth.checkAuth, alerts.findOne]);

    // Delete an alert with alertId
    app.delete('/api/alerts/:alertId', [auth.checkAuth, alerts.delete]);


};