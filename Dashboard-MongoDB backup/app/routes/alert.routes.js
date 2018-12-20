module.exports = (app) => {
	const alerts = require('../controllers/alert.controller.js');

	// Create a new alert
	app.post('/api/alerts', alerts.create);

	// Retrieve all alerts
	app.get('/api/alerts', alerts.find);

	// Retrieve a single Alert with alertId
	app.get('/api/alerts/:alertId', alerts.findOne);

	// Delete an alert with alertId
	app.delete('/api/alerts/:alertId', alerts.delete);
	
	// // Update an alert with alertId
	// app.put('/api/alerts/:alertId', alerts.update);
}