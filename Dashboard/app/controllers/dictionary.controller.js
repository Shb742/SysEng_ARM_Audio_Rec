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
            if (dict === undefined || dict.length == 0){
                Dictionary.findOneAndUpdate({}, {'content': 'help me /1e-21/\nhelp help /1e-25/\nsomeone help /1e-37/\nsomebody help /1e-30/\n'}, {upsert: true}, function (err, doc) {
                    if (err) return res.send(500, {error: err});
                });
                return res.send([{'content': 'help me /1e-21/\nhelp help /1e-25/\nsomeone help /1e-37/\nsomebody help /1e-30/\n'}]);
            }
            return res.send(dict);
        }).catch(err => {
        return res.status(500).send({
            message: err.message || "Some error occurred while retrieving dictionary."
        });
    });
};

