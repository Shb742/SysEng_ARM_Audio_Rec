// *    Title: Testing a Node.js HTTP server with Mocha
// *    Author: Taylor Fausak
// *    Date: February 17, 2013
// *    Code version: 1.0.0
// *    Availability: https://taylor.fausak.me/2013/02/17/testing-a-node-js-http-server-with-mocha/



// get chai's assertation library
// const assert = require('chai').assert;
var should = require('chai').should();
var sinon = require('sinon');
const nock = require('nock');
var assert = require('assert'),
    http = require('http');
const scope = nock('https://edvs.uk.to/')
  .post('pages/login.html', 'username=kimia&password=123kimia321')
  .reply(200, "Right Credentials")

this.server = http.createServer(function (req, res) {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello, world!\n');
});
exports.listen = function () {
  this.server.listen.apply(this.server, arguments);
};

exports.close = function (callback) {
  this.server.close(callback);
};
var server = require('../server');

describe('server', function () {
  before(function () {
    server.listen(8080);
  });

  after(function () {
    server.close();
  });
});