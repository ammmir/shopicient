var fs = require('fs'),
    url = require('url');

var common = require('./common');

var sendResponse = common.sendResponse,
        sendFile = common.sendFile;

var Site = function Site() {
};

Site.prototype.getRoot = function getRoot(req, res, next) {
  sendFile(res, __dirname + '/../public/index.html');
};

exports.Site = Site;
