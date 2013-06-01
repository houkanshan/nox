(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'jquery', 'lodash', 'backbone', 'mods/movies'], function(app, $, _, Backbone, Movies) {
    var Question, _ref;

    return Question = (function(_super) {
      __extends(Question, _super);

      function Question() {
        this.toRenderJSON = __bind(this.toRenderJSON, this);        _ref = Question.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      Question.prototype.defaults = {
        question: '额，这并不是个问题, 这是个bug。。。',
        headUrl: ' ',
        type: ' ',
        movies: [
          {
            id: '2',
            name: 'aaa',
            cover_url: '/images/sample_cover.jpg',
            director: 'kk',
            summary: 'xxxxxx'
          }, {
            id: '1',
            name: 'bb',
            cover_url: 'http://img3.douban.com/view/photo/photo/public/p1812483670.jpg',
            director: 'houkanshan',
            summary: 'xxxxxx'
          }
        ]
      };

      Question.prototype.toRenderJSON = function() {
        var question;

        question = this.toJSON();
        app.movies.update(question.movies);
        question.movie = app.movies.bestOne();
        return question;
      };

      return Question;

    })(Backbone.Model);
  });

}).call(this);
