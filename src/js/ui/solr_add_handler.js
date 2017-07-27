let $ = global.$

let setQueryResult = (res) =>{
  $('#solr-add-result').text(JSON.stringify(res))
  $('.solr-add-result-holder').show()
}
let next_id = 1;
module.exports= () => {
  let q_text = $('#demo_solr_add_text').val()
  let doc = {
    id:next_id++,
    text_t: q_text,
    title_t: "Same Title"
  }
  $.ajax({
    type: 'get',
    url: "solr/add",
    data:`doc=${JSON.stringify(doc)}`,
    success: setQueryResult
  });
}
