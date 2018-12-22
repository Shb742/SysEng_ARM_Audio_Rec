const Alert = require('../models/alert.model.js');

// Create and Save a new Alert
exports.create = (req, res) => {
	// Validate request
	if (res.locals.authlevel > 1){
		return res.status(400).send({
			ERROR: 'Not authorized!'
		});
	}
	if(!req.body.content) {
		return res.status(400).send({
			ERROR: "Content can not be empty"
		});
	}

	// Create an alert
	const alert = new Alert({
		content: req.body.content || "Untitled", 
		type: req.body.type || "audio/wav",
		location: req.body.location || "Unspecified",
		file: req.body.file
	});

	// console.log(alert._id); -- maybe push update to webpage
	
	// Save Alert in the database
	alert.save()
	.then(data => {
		return res.status(200).send({
			Success : alert._id
		});
	}).catch(err => {
		return res.status(500).send({
			ERROR: err.message || "Some error occurred while creating the Alert."
		});
	});

};

// Retrieve and return all alerts from the database.
exports.find = (req, res) => {
	var Qlimit = parseInt(req.query.limit);
	if (isNaN(Qlimit)){
		Qlimit = 10;
	}
	if (req.query.file == undefined){
		Alert.find({}, null, {limit: Qlimit}).select("+file")
		.then(alerts => {
			return res.send(alerts);
		}).catch(err => {
			return res.status(500).send({
				message: err.message || "Some error occurred while retrieving alerts."
			});
		});
	}else{
		Alert.find({}, null, {limit: Qlimit})
		.then(alerts => {
			return res.send(alerts);
		}).catch(err => {
			return res.status(500).send({
				message: err.message || "Some error occurred while retrieving alerts."
			});
		});
	}
	
};

// Find a single alert with a alertId
exports.findOne = (req, res) => {
	Alert.findById(req.params.alertId).select("+file")
	.then(alert => {
		if(!alert) {
			return res.status(404).send({
				message: "Note not found with id " + req.params.alertId
			});            
		}
		return res.send(alert);
	}).catch(err => {
		if(err.kind === 'ObjectId') {
			return res.status(404).send({
				message: "Alert not found with id " + req.params.alertId
			});                
		}
		return res.status(500).send({
			message: "Error retrieving alert with id " + req.params.alertId
		});
	});
};


// Delete an alert with the specified alertId in the request
exports.delete = (req, res) => {
	// Validate request
	if (res.locals.authlevel != 0){
		return res.status(400).send({
			message: 'ERROR : Not authorized!'
		});
	}
	Alert.findByIdAndRemove(req.params.alertId)
	.then(alert => {
		if(!alert) {
			return res.status(404).send({
				message: "Alert not found with id " + req.params.alertId
			});
		}
		return res.send({message: "Alert deleted successfully!"});
	}).catch(err => {
		if(err.kind === 'ObjectId' || err.name === 'NotFound') {
			return res.status(404).send({
				message: "Alert not found with id " + req.params.alertId
			});                
		}
		return res.status(500).send({
			message: "Could not delete alert with id " + req.params.alertId
		});
	});
};