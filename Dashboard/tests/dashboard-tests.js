const assert = require('chai').assert;
var should = require('chai').should();
var sinon = require('sinon');
const nock = require('nock');

// load the software we are testing
const dashboard = require('../dashboard');
const server = require('../server');

//TESTS
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
