var WebServer = require('./web').WebServer,
         Site = require('./site').Site;

var Shopicient = function() {
}

Shopicient.prototype.run = function init() {
  global['Shopicient'] = this;

  this.site = new Site();
  this.server = new WebServer(this.site);

  this.server.listen(8080);
};

new Shopicient().run();
