module.exports = (app) => {

    const sendStaticOptions = {
        root: process.cwd() + '/root',
        dotfiles: 'deny'
    };

    // Login page
    app.get('/login', (req, res) => res.sendFile('login.html', sendStaticOptions));

    // Alerts table page
    app.get('/alerts', (req, res) => res.sendFile('alerts.html', sendStaticOptions));

    // Users table page
    app.get('/users', (req, res) => res.sendFile('users.html', sendStaticOptions));

    // Devices table page
    app.get('/devices', (req, res) => res.sendFile('devices.html', sendStaticOptions));

    // Settings page
    app.get('/settings', (req, res) => res.sendFile('settings.html', sendStaticOptions));

    // 404 Page Not Found page
    app.get('*', (req, res) => res.status(404).sendFile('404.html', sendStaticOptions));

};