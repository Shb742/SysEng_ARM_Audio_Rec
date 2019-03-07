// AUTH
const User = require('../models/user.model.js');
const admintoken = process.env.ADMIN_TOKEN || "DEFAULT@Admin123ToKen0qekksd";
const sanitize = require('mongo-sanitize');

exports.checkAuth = (req, res, next) => {
	sanitize(req);//make safe for mongodb
	if (escape(req.query.token) ==  admintoken){
		res.locals.authlevel = 0;//admin
		next();
	}else if (req.session) {
		User.findById(sanitize(req.session.userId))
		.exec(function (error, user) {
			if (error) {
				res.status(500).send({ERROR: ' ' + error});
			} else {
				if (user === null) {
					res.status(400).send({ERROR: 'Not authorized!'});
				} else {
					res.locals.authlevel = user.authlevel;
					next();
				}
			}
		});
	}else{
		res.redirect('/login');
	}
}