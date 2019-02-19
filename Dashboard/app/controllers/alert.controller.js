const Alert = require('../models/alert.model.js');

// Create and Save a new Alert
exports.create = (req, res) => {
	// Validate request
	if (res.locals.authlevel > 1){
		return res.status(400).send({
			ERROR: 'Not authorized!'
		});
	}
	if(!req.body.file) {
		return res.status(400).send({
			ERROR: "Content can not be empty"
		});
	}

	// Create an alert
	const alert = new Alert({
		content: escape(req.body.content) || "example",
		type: req.body.type || "data:audio/wav;base64,",
		location: escape(req.body.location) || "Unspecified",
		file: escape(req.body.file)
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


//Get total number of alerts
exports.count = (req, res) => {
	//countDocuments()
	Alert.count().then(count => {
		return res.status(200).send({
			TotalAlerts : count
		});
	}).catch(err => {
		return res.status(500).send({
			ERROR: err.message || "Some error occurred while retrieving alerts."
		});
	});
}

// Retrieve and return all alerts from the database.
exports.find = (req, res) => {
	var Qlimit = parseInt(req.query.limit);
	if (isNaN(Qlimit)){
		Qlimit = 10;
	}
	var skipnum = parseInt(req.query.skip);
	if (isNaN(skipnum)){
		skipnum = 0;
	}

	var find_file = "";
	if (req.query.file == undefined){
		find_file = "+file";
	}else{
		find_file = "-file";
	}
	Alert.find({},{},{ sort:{ 'createdAt' : -1 }, limit: Qlimit, skip: skipnum }).select(find_file)
	.then(alerts => {
		return res.send(alerts);
	}).catch(err => {
		return res.status(500).send({
			ERROR: err.message || "Some error occurred while retrieving alerts."
		});
	});

};

// Find a single alert with a alertId
exports.findOne = (req, res) => {
	var find_file = "";
	if (req.query.file == undefined){
		find_file = "+file";
	}else{
		find_file = "-file";
	}
	Alert.findById(escape(req.params.alertId)).select(find_file)
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
	Alert.findByIdAndRemove(escape(req.params.alertId))
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
