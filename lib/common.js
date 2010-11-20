var fs = require('fs');

function sendResponse(res, code, body) {
  var isString;
  var headers = {
    'Server': 'Shopicient/0.1'
  };
  
  if(body) {
    isString = body instanceof String || typeof body == 'string';

    if(!isString)
      body = JSON.stringify(body);

    headers['Content-Type'] = isString ? 'text/plain' : 'application/json';
    headers['Content-Length'] = body.length;
  }

  res.writeHead(code, headers);

  if(body)
    res.end(body, 'utf8');
  else
    res.end();
}

function sendFile(res, file) {
  fs.readFile(file, function(err, data) {
    if(err) {
      res.writeHead(500, {
        'Content-Type': 'text/plain',
        'Content-Length': (''+err).length
      });
      res.end(''+err);
      return;
    }

    res.writeHead(200, {
      'Content-Type': 'text/html',
      'Content-Length': data.length
    });

    res.end(data, 'utf8');
  });
}

function guard(handler) {
  return function(req, res, next) {
    if(req.session.user) {
      handler(req, res, next);
    } else {
      sendResponse(res, 403, 'not authorized');
    }
  };
}

exports.sendResponse = sendResponse;
exports.sendFile = sendFile;
exports.guard = guard;
