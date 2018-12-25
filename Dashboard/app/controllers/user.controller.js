const User = require('../models/user.model.js');

// Create and Save a new Alert
exports.singup = (req, res) => {
	// Validate request
	if (res.locals.authlevel != 0){
		return res.status(400).send({
			message: 'ERROR : Not authorized!'
		});
	}
	if (req.body.username &&
		req.body.password && 
		req.body.authlevel) {

		var userData = {
		  username: req.body.username,
		  password: req.body.password,
		  authlevel: req.body.authlevel
		}

		User.create(userData, function (error, user) {
		  if (error) {
			return res.status(400).send({
				message: 'ERROR : '+error
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
		message: 'ERROR : Malformed request'
	});
  }
	
};


// Retrieve and return all alerts from the database.
exports.find = (req, res) => {
	// Validate request
	if (res.locals.authlevel != 0){
		return res.status(400).send({
			message: 'ERROR : Not authorized!'
		});
	}
	var Qlimit = parseInt(req.query.limit);
	if (isNaN(Qlimit)){
		Qlimit = 10;
	}
	User.find({}, null, {limit: Qlimit})
	.then(users => {
		return res.send(users);
	}).catch(err => {
		return res.status(500).send({
			message: err.message || "Some error occurred while retrieving alerts."
		});
	});
};

// Retrieve and return all alerts from the database.
exports.login = (req, res) => {
	User.authenticate(req.body.username, req.body.password, function (error, user) {
	  if (error || !user) {
		return res.status(400).send({
			message: 'ERROR : Wrong Credentials'
		});
	  } else {
		req.session.userId = user._id;
		return res.redirect('/');
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


// Allow updating of user password
exports.ping = (req, res) => {
	User.findByIdAndUpdate(req.session.userId,{lastSeen: new Date()})
	.exec(function (error, user) {
	  if (error) {
		return res.status(500).send({
			message: 'ERROR : Something went wrong'
		});
	  } else {
		if (user === null) {
		  	return res.status(400).send({
				message: 'ERROR : Not authorized!'
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
					message: 'ERROR : Something went wrong'
				});
			} else {
				return res.status(200).send({
				message: "Logged out" 
				});
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
