// get chai's assertation library
const assert = require('chai').assert;
var should = require('chai').should();
var sinon = require('sinon');
const nock = require('nock');
const scope = nock('https://edvs.uk.to/')
  .post('pages/login.html', 'username=kimia&password=123kimia321')
  .reply(200, "Right Credentials")

// load the software we are testing
const dashboard = require('../dashboard');
//create a test
// const string  = '&';
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
    var first_update = 0;
    var rows_length_before = dashboard.updateAlerts(first_update);
    //fake alert
    var rows_length_after = dashboard.updateAlerts(first_update);
    var difference = rows_length_after - rows_length_before;
    assert.equal(difference, 1);

  });
});

// describe('check to see if the new alert gets added to the table and old one is now the second alert', function(){
//   it('Done', function(){
//     //FAKE ALERT
//     var rows = dashboard.checkForAlerts(first_update);
//     var row0 = rows[0];
//     var row1 = rows[1];
//
//     assert.equal(row1,row2);
//
//   });
// });

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
    }, 500);

    interval.should.be.false;
    clock.tick(15501);
    interval.should.be.true;

  });
});
