// AUTH
const User = require('../models/user.model.js');
const admintoken = process.env.ADMIN_TOKEN || "DEFAULT@Admin123ToKen0qekksd";

exports.checkAuth = (req, res, next) => {
	if (req.query.token ==  admintoken){
		res.locals.authlevel = 0;//admin
		next()
	}else if (req.session) {
		User.findById(req.session.userId)
		.exec(function (error, user) {
			if (error) {
				res.status(500).send({message: 'ERROR : ' + error});
			} else {
				if (user === null) {
					console.log("User not auth");
					res.status(400).send({message: 'ERROR : Not authorized!'});
				} else {
					console.log("User authed");
					res.locals.authlevel = user.authlevel;
					next()
				}
			}
		});
	}else{
		res.redirect('/');
	}
}