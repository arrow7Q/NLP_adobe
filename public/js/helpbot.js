"use strict";

(function e(t, n, r) {
  function s(o, u) {
    if (!n[o]) {
      if (!t[o]) {
        var a = typeof require == "function" && require;if (!u && a) return a(o, !0);if (i) return i(o, !0);var f = new Error("Cannot find module '" + o + "'");throw f.code = "MODULE_NOT_FOUND", f;
      }var l = n[o] = { exports: {} };t[o][0].call(l.exports, function (e) {
        var n = t[o][1][e];return s(n ? n : e);
      }, l, l.exports, e, t, n, r);
    }return n[o].exports;
  }var i = typeof require == "function" && require;for (var o = 0; o < r.length; o++) {
    s(r[o]);
  }return s;
})({ 1: [function (require, module, exports) {
    var init = require('./init');
    init();
  }, { "./init": 2 }], 2: [function (require, module, exports) {
    (function (global) {
      var $ = global.$;
      var handlers = require('./ui/handlers');

      function initHandlers() {
        $.each(handlers.click, function (index, handler) {
          console.log(index);
          $(handler.selector).click(handler.callback);
        });
      }

      module.exports = initHandlers;
    }).call(this, typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {});
  }, { "./ui/handlers": 4 }], 3: [function (require, module, exports) {
    (function (global) {
      //const query_handler = require('./process_query_handler')
      //const solr_query_handler = require('./solr_query_handler')
      var ui_utils = require('./utils');
      var $ = global.$;
      var queryTypeMap = {
        Information: "DEF",
        Process: "STP"
      };

      var answerProcessor = function answerProcessor(docs, type) {
        var newDocs = [];

        // testing -utkarsh
        var isInArray = function isInArray(arr, str) {
          return arr.indexOf(str.toLowerCase()) > -1;
        };

        $.each(docs, function (index, doc) {
          doc.scores = JSON.parse(doc.scores
          //--->
          // if( isInArray(doc.object, text) )
          //   doc.scores[type]+= 5 
          // console.log(doc.scores[type])
          //--->

          );doc.index = index;
          newDocs.push(doc);
        });
        var compareFn = function compareFn(doc1, doc2) {
          if (doc1.scores && doc2.scores && doc1.scores[type] !== undefined && doc2.scores[type] !== undefined) {
            if (doc1.scores[type] !== doc2.scores[type]) {
              return doc2.scores[type] - doc1.scores[type];
            } else {
              return doc1.index - doc2.index;
            }
          }
          return 0;
        };
        newDocs.sort(compareFn);
        return newDocs;
      };

      //testing --utkarsh
      // let boost = (docs, type, text ) =>{
      //   let modDocs = []

      // let isInArray = (arr, str) => {
      //     return arr.indexOf(str.toLowerCase()) > -1;
      // }

      //   $.each(docs, (index, doc) =>{
      //     doc.scores = JSON.parse(doc.scores)
      //     if( isInArray(doc.object, text) )
      //       doc.scores[type]+= 5 
      //     console.log(doc.scores[type])
      //   })
      // }


      var onSolrQueryResult = function onSolrQueryResult(res, type) {
        if (res && res.numFound > 0) {
          //let docs = res.docs.splice(0, 5)
          //console.log(text)  //for testting

          //let temp = boost(res.docs, type, text)
          var top_docs = answerProcessor(res.docs, type);
          top_docs = top_docs.splice(0, 5);
          var answerHtml = ui_utils.getTableHtml(top_docs, type

          //let answerHtml =   setscore(docs)
          );if (top_docs.length > 0 && top_docs[0]["text"]) {
            $('.first-answer').show();
            $('#first_answer').html(top_docs[0]["text"][0]);

            $('.predicted-answer').show();
            $('#processed_answer').html(answerHtml);
          }
        }
      };

      var onQueryResult = function onQueryResult(res) {
        //let q_text = $('#q_text').val()
        console.log(res // again testing


        );var query_result = JSON.parse(res);
        var query_param = {};
        //var q_type = queryTypeMap[query_result.qtype]
        var q_features = query_result.features || [];
        var q_text = q_features.join(' ');
        var query_string = "q=" + q_text;
        console.log(query_result.qtype);
        if (query_result.qtype) {
          //query_param.type = queryTypeMap[query_result.qtype]
          query_param.type = query_result.qtype;

          query_string += "&type=" + query_param.type;

          //onSolrQueryResult(q_text,q_type)
        }
        var successFn = function successFn(res) {
          onSolrQueryResult(res, query_param.type);
        };

        $.ajax({
          type: 'get',
          url: "solr/search",
          data: query_string,
          success: successFn
        });
      };

      //get the queryprocessed from the python script
      module.exports = function () {
        var q_text = $('#q_text').val();
        $.ajax({
          type: 'get',
          url: "query",
          data: "q=" + q_text,
          success: onQueryResult
        });
      };
    }).call(this, typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {});
  }, { "./utils": 9 }], 4: [function (require, module, exports) {
    var processQueryHandler = require('./process_query_handler');
    var processFeatureHandler = require('./process_feature_handler');
    var answerHandler = require('./answer_handler');
    var solrAddHandler = require('./solr_add_handler');
    var sorlQueryHandler = require('./solr_query_handler');

    var handlers = {
      click: [{
        selector: '#predict_answer',
        callback: answerHandler
      }, {
        selector: '#demo_process_question',
        callback: processQueryHandler
      }, {
        selector: '#demo_process_features',
        callback: processFeatureHandler
      }, {
        selector: '#demo_solr_add',
        callback: solrAddHandler
      }, {
        selector: '#demo_solr_search',
        callback: sorlQueryHandler
      }]
    };
    module.exports = handlers;
  }, { "./answer_handler": 3, "./process_feature_handler": 5, "./process_query_handler": 6, "./solr_add_handler": 7, "./solr_query_handler": 8 }], 5: [function (require, module, exports) {
    (function (global) {
      var $ = global.$;

      var setQueryResult = function setQueryResult(res) {
        var docs = JSON.parse(res);
        $.each(docs, function (id, doc) {
          $.ajax({
            type: 'post',
            url: "solr/add",
            data: JSON.stringify(doc)
          });
        });
      };
      var errorFn = function errorFn(error) {
        console.error("Error");
        console.error(error);
      };

      module.exports = function () {

        $.ajax({
          type: 'get',
          url: "features",
          //data:`text=${q_text}`,
          success: setQueryResult,
          error: errorFn
        });
      };
    }).call(this, typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {});
  }, {}], 6: [function (require, module, exports) {
    (function (global) {
      var $ = global.$;

      var setQueryResult = function setQueryResult(res) {
        $('#processed_query').text(res);
        $('.predicted-answer').show();
      };

      module.exports = function () {
        var callback = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : setQueryResult;


        var q_text = $('#demo_q_text').val();
        $.ajax({
          type: 'get',
          url: "query",
          data: "q=" + q_text,
          success: setQueryResult
        });
      };
    }).call(this, typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {});
  }, {}], 7: [function (require, module, exports) {
    (function (global) {
      var $ = global.$;

      var setQueryResult = function setQueryResult(res) {
        $('#solr-add-result').text(JSON.stringify(res));
        $('.solr-add-result-holder').show();
      };
      var next_id = 1;
      module.exports = function () {
        var q_text = $('#demo_solr_add_text').val();
        var doc = {
          id: next_id++,
          text_t: q_text,
          title_t: "Same Title"
        };
        $.ajax({
          type: 'get',
          url: "solr/add",
          data: "doc=" + JSON.stringify(doc),
          success: setQueryResult
        });
      };
    }).call(this, typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {});
  }, {}], 8: [function (require, module, exports) {
    (function (global) {
      var $ = global.$;

      var setQueryResult = function setQueryResult(res) {
        $('#solr_result').text(JSON.stringify(res));
        $('.solr-result').show();
      };

      module.exports = function (queryMap) {
        var callback = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : setQueryResult;

        var q_text = $('#demo_solr_q_text').val();
        $.ajax({
          type: 'get',
          url: "solr/search",
          data: "q=" + JSON.stringify(q_text),
          success: setQueryResult
        });
      };
    }).call(this, typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {});
  }, {}], 9: [function (require, module, exports) {
    module.exports = {
      getListHtml: function getListHtml(docs) {
        var text = "";
        $.each(docs, function (index, doc) {
          var doctext = doc.text && doc.text[0];
          if (typeof doctext === 'string') {
            doctext = doctext.replace(/(\n)+/g, '<br />');
            text += "<li>" + doctext + "</li>";
          }
        });
        return text.length === 0 ? text : "<ol>" + text + "</ol>";
      },
      getTableHtml: function getTableHtml(docs, type) {
        var text = "";
        $.each(docs, function (index, doc) {
          var doctext = doc.text && doc.text[0];
          if (typeof doctext === 'string') {
            doctext = doctext.replace(/(\n)+/g, '<br />');
            var score = doc.scores && doc.scores[type] ? doc.scores[type] : 0;
            text += "<tr><td>" + doctext + "</td><td>" + score + "</td> </tr>";
          }
        });
        return text.length === 0 ? text : "<table><tr><th>Result</th><th>Score</th></tr>" + text + "</ol>";
      }
    };
  }, {}] }, {}, [1]);
