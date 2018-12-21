const mongoose = require('mongoose');

const AlertSchema = mongoose.Schema({
	content: String,
	type: String,
	location: String,
	file: String,
	createdAt: { type: Date, expires: '43200m', default: Date.now }
}, {
	capped : true,
	size : 1677721600,
	max : 100,
	timestamps: true
});

module.exports = mongoose.model('Alert', AlertSchema);