(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'jquery', 'lodash', 'backbone', 'collections/questionSet', 'models/question'], function(app, $, _, Backbone, QuestionSet, Question) {
    var QuestionView, _ref;

    return QuestionView = (function(_super) {
      __extends(QuestionView, _super);

      function QuestionView() {
        this.showDown = __bind(this.showDown, this);
        this.hideUp = __bind(this.hideUp, this);        _ref = QuestionView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      QuestionView.prototype.className = 'question-wrapper';

      QuestionView.prototype.template = _.template($('#question-dialog-tmpl').html());

      QuestionView.prototype.collection = new QuestionSet();

      QuestionView.prototype.currentQuestion = new Question();

      QuestionView.prototype.events = {
        'click button[type=submit]': 'answerQuestion'
      };

      QuestionView.prototype.initialize = function() {
        app.on('panel:show', this.hideUp);
        app.on('panel:hide', this.showDown);
        this.collection.on('add', this.gotNewQuestion, this);
        this.getQuestion();
        return this.hideUp();
      };

      QuestionView.prototype.hideUp = function() {
        return this.$el.addClass('hide-up');
      };

      QuestionView.prototype.showDown = function() {
        if (!this.currentQuestion.get('uid') || app.loading) {
          return;
        }
        return this.$el.removeClass('hide-up');
      };

      QuestionView.prototype.render = function() {
        var question;

        question = this.currentQuestion.toRenderJSON();
        this.$el.html(this.template(question));
        return this;
      };

      QuestionView.prototype.gotNewQuestion = function(model, collection) {
        this.currentQuestion = model;
        this.render();
        this.showDown();
        return this;
      };

      QuestionView.prototype.getQuestion = function(answer) {
        var _this = this;

        if (answer == null) {
          answer = {
            answer: -1
          };
        }
        app.trigger('loading');
        app.loading = true;
        return $.post('/questions/', answer).done(function(r) {
          app.loading = false;
          app.uid = r.uid;
          return _this.addQuestion(r);
        }).fail(function(r) {
          var _ref1;

          if ((_ref1 = _this.trick) == null) {
            _this.trick = '是么？那';
          }
          _this.trick += '那';
          r = {
            type: 'question',
            question: _this.trick + '你吃过Bug么？'
          };
          return _this.addQuestion(r);
        });
      };

      QuestionView.prototype.answerQuestion = function(e) {
        var answer;

        this.hideUp();
        e = $(e.target);
        answer = {
          uid: app.uid,
          answer: e.val()
        };
        this.getQuestion(answer);
        return this;
      };

      QuestionView.prototype.addQuestion = function(gotQuestion) {
        var queston;

        queston = new Question(gotQuestion);
        this.collection.add(queston);
        app.trigger('getMovies', gotQuestion.movies_url);
        return this;
      };

      return QuestionView;

    })(Backbone.View);
  });

}).call(this);
