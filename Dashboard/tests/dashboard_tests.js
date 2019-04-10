// get chai's assertation library


const assert = require('chai').assert;
var should = require('chai').should();
var sinon = require('sinon');
const nock = require('nock');
// load the software we are testing
const dashboard = require('../dashboard');
//create a test
describe('Replace characters', function(){
  it('& -> amp', function(){

    var isItAmpt = dashboard.escapeHtml('&');
    assert.equal(isItAmpt, '&amp;');
  });
});

describe('Replace characters', function(){
  it('< -> lt', function(){

    var isItAmpt = dashboard.escapeHtml('<');
    assert.equal(isItAmpt, '&lt;');
  });
});

describe('Replace characters', function(){
  it('> -> gt', function(){

    var isItAmpt = dashboard.escapeHtml('>');
    assert.equal(isItAmpt, '&gt;');
  });
});

describe('Replace characters', function(){
  it(' single_quote  -> lt', function(){

    var isItAmpt = dashboard.escapeHtml('\'');
    assert.equal(isItAmpt, '&#039;');
  });
});

describe('Replace characters', function(){
  it(' " -> lt', function(){

    var isItAmpt = dashboard.escapeHtml('\"');
    assert.equal(isItAmpt, '&quot;');
  });
});

describe('check to see if the new alert gets added to the table', function(){
  it('Done', function(){
    var first_update = 3;
    var rows_length_before = dashboard.updateAlerts(first_update);
    console.log(rows_length_before);
    var middle = dashboard.addARow(first_update);
    console.log(middle);
    var rows_length_after = dashboard.updateAlerts(first_update);
    console.log(rows_length_after);
    // var difference = rows_length_after - rows_length_before;
    // assert.equal(difference, 1);

  });
});

describe('check to see if the new alert gets added to the table and old one is now the second alert', function(){
  it('Done', function(){
    first_update= true;
    var middle = dashboard.addARow(first_update);
    console.log(middle);
    var rows = dashboard.checkForAlerts(first_update);
    // var row0 = rows[0];
    // var row1 = rows[1];

    // assert.equal(row1,row2);

  });
});

describe('when a new person logs in, ', function(){
  it('Does the table of users change', function(){

    var beforeLogin = dashboard.updateUserTable();
    console.log(beforeLogin);
    const scope = nock('https://edvs.uk.to/')
      .post('pages/login.html', 'username=kimia&password=123kimia321')
      .reply(200, "Right Credentials")
    var afterLogin = dashboard.updateUserTable();
    var difference = afterLogin - beforeLogin;
    assert.equal(difference, 1);
  });
});

describe('when a new device gets added, ', function(){
  it('Does the table of devices change', function(){

    var beforeAddingADevice = dashboard.updateDeviceTable();
    console.log(beforeLogin);
    dashboard.addADevice();
    var afterAddingADevice = dashboard.updateUserTable();
    var difference = afterAddingADevice - beforeAddingADevice;
    assert.equal(difference, 1);
  });
});

var clock;
beforeEach(function () {
     clock = sinon.useFakeTimers();
 });
afterEach(function () {
    clock.restore();
});
describe('does it wait 15 secs?', function(){
  it('Check for alerts', function(){

    var interval = false;
    setInterval(function () {
        interval = true;
    }, 5000);

    interval.should.be.false;
    clock.tick(15501);
    interval.should.be.true;

  });
});
