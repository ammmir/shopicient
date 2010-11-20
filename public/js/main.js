// main application

HashHistory.initialize();
HashHistory.register(/^#test/, function(hash) {
  console.log('test hash: ' + hash);
});
HashHistory.loadURL(function() {
  // we're called in case no fragment is matched
  console.log('no fragments matched.');
});
//HashHistory.save("#fragment");

function Shopicient() {
  this.root = $("#content");
}

Shopicient.prototype.run = function() {
};

