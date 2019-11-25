const mongoose = require('mongoose');
const bcryptjs = require('bcryptjs');
const Schema = mongoose.Schema;
const sanitizerPlugin = require('mongo-sanitize');

const UserSchema = new Schema({
    username: {
        type: String,
        unique: true,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    location: String,
    authlevel: {
        type: Number,
        default: 2
    },
    lastSeen: {
        type: Date,
        default: Date.now
    },
    createdDate: {
        type: Date,
        default: Date.now
    }
});

UserSchema.plugin(sanitizerPlugin);


//authenticate input against database
UserSchema.statics.authenticate = (username, password, callback) => {
    User.findOne({username: username})
        .exec(function (err, user) {
            if (err) {
                return callback(err)
            } else if (!user) {
                var err = new Error('User not found.');
                err.status = 401;
                return callback(err);
            }
            bcryptjs.compare(password, user.password, function (err, result) {
                if (result === true) {
                    return callback(null, user);
                } else {
                    return callback();
                }
            })
        });
}


//hashing a password before saving it to the database
UserSchema.pre('save', function (next) {
    var user = this;
    bcryptjs.hash(user.password, 10, function (err, hash) {
        if (err) {
            return next(err);
        }
        user.password = hash;
        next();
    })
});

var User = mongoose.model('User', UserSchema);

module.exports = User;