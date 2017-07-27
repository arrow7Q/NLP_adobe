let $ = global.$

let setQueryResult = (res) =>{
  $('#solr_result').text(JSON.stringify(res))
  $('.solr-result').show()
}

module.exports= (queryMap, callback = setQueryResult, ) => {
  let q_text = $('#demo_solr_q_text').val()
  $.ajax({
    type: 'get',
    url: "solr/search",
    data:`q=${JSON.stringify(q_text)}`,
    success: setQueryResult
  });
}
