let solr = require('solr')
let client = solr.createClient({core:"/gettingstarted"});
module.exports = (doc, callback)=>{

  /*var doc1 = {
    id: '1',
    title_t: 'Foo bar',
    text_t: 'Fizz buzz frizzle'
  };
  var doc2 = {
    id: '2',
    title_t: 'Far boo',
    text_t: 'Wuzz fizz drizzle'
  };
*/


  client.add(doc, function(err) {
    if (err) console.error(`Error occurred during Add ${err}`);
    client.commit(function(err) {
      if (err) console.error(`Error occurred during Commit ${err}`);
      console.log(`Added ${JSON.stringify(doc)}`);
      if(callback)
        callback(doc)
    /*client.add(doc2, function(err) {
      if (err) throw err;
      console.log('Second document added');
      client.commit(function(err) {
        console.log(err)

      });
      */
    });
  });
}
