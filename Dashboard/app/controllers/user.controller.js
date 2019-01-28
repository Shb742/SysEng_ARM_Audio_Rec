const User = require('../models/user.model.js');
const sanitize = require('mongo-sanitize');

// Create and Save a new Alert
exports.singup = (req, res) => {
	// Validate request
	if (res.locals.authlevel != 0){
		return res.status(400).send({
			ERROR: 'Not authorized!'
		});
	}
	sanitize(req.body);
	if (req.body.username &&
		req.body.password && 
		!isNaN(parseInt(req.body.authlevel))) {
		
		var userData = {
		  username: escape(req.body.username),
		  password: req.body.password,
		  authlevel: req.body.authlevel
		}

		User.create(userData, function (error, user) {
		  if (error) {
			return res.status(400).send({
				ERROR : ''+error
			});
		  } else {
			// req.session.userId = user._id;
			return res.status(200).send({
				session_token: user._id 
			});
			
			// return res.redirect('/');
		  }
		});
	} else {
	return res.status(400).send({
		ERROR: 'Malformed request'
	});
  }
	
};


//Get total number of users
exports.count = (req, res) => {
	// Validate request
	//countDocuments()
	if (res.locals.authlevel != 0){
		return res.status(400).send({
			ERROR: 'Not authorized!'
		});
	}
	User.count().then(count => {
		return res.status(200).send({
			TotalUsers : count
		});
	}).catch(err => {
		return res.status(500).send({
			ERROR: err.message || "Some error occurred while retrieving users."
		});
	});
}


// Retrieve and return users from the database.
exports.findDevices = (req, res) => {
	// Validate request
	var Qlimit = parseInt(req.query.limit);
	if (isNaN(Qlimit)){
		Qlimit = 10;
	}
	var skipnum = parseInt(req.query.skip);
	if (isNaN(skipnum)){
		skipnum = 0;
	}

	User.find({"authlevel":1}, null, {limit: Qlimit, skip: skipnum})
	.then(users => {
		return res.send(users);
	}).catch(err => {
		return res.status(500).send({
			message: err.message || "Some error occurred while retrieving alerts."
		});
	});
};

// Retrieve and return users from the database.
exports.find = (req, res) => {
	// Validate request
	if (res.locals.authlevel != 0){
		return res.status(400).send({
			ERROR: 'Not authorized!'
		});
	}
	var Qlimit = parseInt(req.query.limit);
	if (isNaN(Qlimit)){
		Qlimit = 10;
	}
	var skipnum = parseInt(req.query.skip);
	if (isNaN(skipnum)){
		skipnum = 0;
	}

	User.find({}, null, {limit: Qlimit, skip: skipnum})
	.then(users => {
		return res.send(users);
	}).catch(err => {
		return res.status(500).send({
			message: err.message || "Some error occurred while retrieving alerts."
		});
	});
};

// login
exports.login = (req, res) => {
	sanitize(req.body);
	User.authenticate(req.body.username, req.body.password, function (error, user) {
	  if (error || !user) {
		return res.status(400).send({
			ERROR: 'Wrong Credentials'
		});
	  } else {
		req.session.userId = user._id;
		//Update last-seen
		// User.findByIdAndUpdate(user._id,{lastSeen: new Date()})
		// .exec(function (error, usr) {
		//   if (error) {
		// 	return res.status(500).send({
		// 		ERROR: 'Something went wrong'
		// 	});
		//   } else if (usr === null) {
		//   	return res.status(400).send({
		// 		ERROR: 'Not authorized!'
		// 	});
		// }
		// });
		//Update last-seen*
		return res.redirect('/pages/index.html');
	  }
	});
};



// // Allow updating of user password
// exports.update = (req, res) => {
// 	User.findById(req.session.userId)
//     .exec(function (error, user) {
//       if (error) {
//         return next(error);
//       } else {
//         if (user === null) {
//           var err = new Error('Not authorized!');
//           err.status = 400;
//           return next(err);
//         } else {
//           return res.send('<h1>Name: </h1>' + user.username + '<a type="button" href="/logout">Logout</a>')
//         }
//       }
//     });
// };


// Update last seen
exports.ping = (req, res) => {
	User.findByIdAndUpdate(req.session.userId,{lastSeen: new Date()})
	.exec(function (error, user) {
	  if (error) {
		return res.status(500).send({
			ERROR: 'Something went wrong'
		});
	  } else {
		if (user === null) {
		  	return res.status(400).send({
				ERROR: 'Not authorized!'
			});
		} else {
			return res.status(200).send({
				Success : "lastSeen updated"
			});
		}
	  }
	});
};


// logout
exports.logout = (req, res) => {
	if (req.session) {
		// delete session object
		req.session.destroy(function (err) {
			if (err) {
				return res.status(500).send({
					ERROR: 'Something went wrong'
				});
			} else {
				res.redirect('/pages/login.html');
				// return res.status(200).send({
				// message: "Logged out" 
				// });
			}
		});
	}
};

// Delete a user
exports.delete = (req, res) => {
	// Validate request
	if (res.locals.authlevel == 0){
		User.findByIdAndRemove(req.params.userId)
		.then(alert => {
			if(!alert) {
				return res.status(404).send({
					message: "User not found with id " + req.params.userId
				});
			}
			return res.send({message: "User deleted successfully!"});
		}).catch(err => {
			if(err.kind === 'ObjectId' || err.name === 'NotFound') {
				return res.status(404).send({
					message: "User not found with id " + req.params.userId
				});
			}
			return res.status(500).send({
				message: "Could not delete user with id " + req.params.userId
			});
		});
	}else{
		return res.status(400).send({
			ERROR: 'Not authorized!'
		});
	}
};
