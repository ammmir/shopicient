require.paths.unshift('../vendor/connect/lib');

var util = require('util');

var common = require('./common');

var connect = require('connect'),
    MemoryStore = require('connect/middleware/session/memory');

var guard = common.guard;

var MINUTE = 60000;

var WebServer = function(site) {
  this.site = site;

  this.server = connect.createServer(
    // log HTTP requests
    connect.logger(),

    // decode application/x-www-form-urlencoded and application/json requests
    connect.bodyDecoder(),

    // populate req.cookies
    connect.cookieDecoder(),

    // dole out session cookies
    connect.session({ store: new MemoryStore({ reapInterval: 5 * MINUTE }) }),

    // conditional HTTP GETs
    connect.conditionalGet(),

    // handle /
    connect.router(this.mainHandler()),

    // cache manifest for offline app
    //connect.cacheManifest(),

    // merge static files into /
    connect.staticProvider({root: __dirname + "/../public", maxAge: 1000}),

    connect.errorHandler({ showStack: true })
  );
};

WebServer.prototype.getServer = function getServer() {
  return this.server;
};

WebServer.prototype.listen = function listen(port) {
  this.server.listen(port);
};

WebServer.prototype.mainHandler = function mainHandler() {
  var site = this.site;

  return function(app) {
    app.get('/', site.getRoot);
    //app.get('/api/orders', site.getOrders);
  };
};

exports.WebServer = WebServer;
