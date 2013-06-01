define [
  'app'
  'jquery'
  'lodash'
  'backbone'
  'collections/questionSet'
  'models/question'
  ], (app, $, _, Backbone, QuestionSet, Question)->

    class QuestionView extends Backbone.View
      className: 'question-wrapper'
      template: _.template($('#question-dialog-tmpl').html())
      collection: new QuestionSet()
      currentQuestion: new Question()
      events:
        'click button[type=submit]': 'answerQuestion'
      initialize: ->
        app.on('panel:show', @hideUp)
        app.on('panel:hide', @showDown)
        @collection.on('add', @gotNewQuestion, this)
        # first question fire
        @getQuestion()
      hideUp: =>
        @$el.addClass('hide-up')
      showDown: =>
        @$el.removeClass('hide-up')
        
      render: ()->
        @hideUp()
        _.delay(()=>
          @showDown()
        , 100)
        question = @currentQuestion.toRenderJSON()
        @$el.html(@template(question))
        @

      gotNewQuestion: (model, collection)->
        @currentQuestion = model
        @render()
        @

      getQuestion: (answer={value: 2})->
        $.post('/questions/', answer)
          .done((r)=>
            @addQuestion(r)
          )
          .fail((r)=>
            # 测试数据
            @trick?= '是么？那'
            @trick += '那'
            r =
              type: 'question'
              question: @trick + '你吃过测试么？'
            @addQuestion(r)
          )

      answerQuestion: (e)->
        e = $(e.target)
        answer =
          value: e.val()
        @getQuestion(answer)
        @

      addQuestion: (gotQuestion)->
        queston = new Question(gotQuestion)
        @collection.add(queston)
        app.trigger 'getMovies', gotQuestion.movies_url
        @
