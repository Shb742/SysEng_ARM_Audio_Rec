module.exports = (app) => {

    const dictionary = require('../controllers/dictionary.controller');
    const auth = require('../controllers/auth.controller.js');

    app.get('/api/dictionary', [auth.checkAuth, dictionary.read]);
    app.post('/api/dictionary', [auth.checkAuth, dictionary.update]);

};
