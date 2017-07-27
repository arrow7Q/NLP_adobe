var express = require('express');
let app = express();
let query_processor = require('./query')
let feature_processor = require('./process_features')
let solr_query_processor = require('./solr/query')
let solr_add_processor = require('./solr/add')
//const feature_adder = re
app.use(express.static('public'))

app.get('/query', function (req, res) {
  let callback =  (text) =>{
    console.log(text)
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(text));
  }
  let q_text = decodeURIComponent(req.query.q)
  console.log(q_text)
  query_processor(q_text, callback)
})
app.get('/features', function (req, res) {
  let callback =  (text) =>{
    //console.log(text)
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(text));
  }
  feature_processor(callback)
})
app.post('/solr/add', function (req, res) {
  let add_text= JSON.parse(req.body)
  let callback =  (text) =>{
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(text));
  }
  solr_add_processor(add_text, callback)
})
app.get('/solr/search', function (req, res) {
  let callback =  (text) =>{
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(text));
  }
  try{
    let search_query = decodeURIComponent(req.query.q)
    let search_type = decodeURIComponent(req.query.type)

    solr_query_processor(search_query, search_type, callback)
  }
  catch(e){
    callback(e)
  }
})
var server = app.listen(8081, "127.0.0.1", function () {
  var host = server.address().address
  var port = server.address().port

  console.log("Helpbot app listening at http://%s:%s", host, port)
})
