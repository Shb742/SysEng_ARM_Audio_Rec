const Dictionary = require('../models/dictionary.model');

exports.update = (req, res) => {

    // Validate request
    if (res.locals.authlevel > 1) {
        return res.status(400).send({
            ERROR: 'Not authorized!'
        });
    }

    if (!req.body.content) {
        return res.status(400).send({
            ERROR: "Content can not be empty"
        });
    }

    Dictionary.findOneAndUpdate({}, {'content': req.body.content}, {upsert: true}, function (err, doc) {
        if (err) return res.send(500, {error: err});
        return res.send("succesfully saved");
    });

};

exports.read = (req, res) => {
    Dictionary.find({}, null, {})
        .then(dict => {
            console.log(dict);
            return res.send(dict);
        }).catch(err => {
        return res.status(500).send({
            message: err.message || "Some error occurred while retrieving dictionary."
        });
    });
};

