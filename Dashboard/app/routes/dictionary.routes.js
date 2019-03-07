module.exports = (app) => {

    const dictionary = require('../controllers/dictionary.controller');
    const auth = require('../controllers/auth.controller.js');

    app.get('/api/dictionary', [auth.checkAuth, dictionary.read]);
    app.post('/api/dictionary', [auth.checkAuth, dictionary.update]);

    // // Update dictionary
    // app.post('/api/update/dictionary', [auth.checkAuth, (req, res) => app.locals.dictionary = req.body.dictionaryForm]);
    //
    // // Get dictionary
    // app.get('/api/get/dictionary', [auth.checkAuth, (req, res) => res.send({dictionary: app.locals.dictionary})]);


};