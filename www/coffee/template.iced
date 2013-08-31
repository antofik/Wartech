window.template = {};

window.template.load = (url, callback) ->
  url = 'template/' + url + '.html';
  await $.get url, {}, defer reply
  callback(reply)

