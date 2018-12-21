const mongoose = require('mongoose');

const UserSchema = mongoose.Schema({
    usertoken: { type: String, unique: true, required: true },
    hash: { type: String, required: true },
    createdDate: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', UserSchema);