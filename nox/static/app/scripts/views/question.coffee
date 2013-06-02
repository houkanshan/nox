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
        @hideUp()

      hideUp: =>
        @$el.addClass('hide-up')
      showDown: =>
        if not @currentQuestion.get('uid') or app.loading
          return
        @$el.removeClass('hide-up')
        
      render: ()->
        question = @currentQuestion.toRenderJSON()
        @$el.html(@template(question))
        @

      gotNewQuestion: (model, collection)->
        @currentQuestion = model
        @render()
        @showDown()
        @

      getQuestion: (answer={answer: -1})->
        app.trigger('loading')
        app.loading = true
        $.post('/questions/', answer)
          .done((r)=>
            app.loading = false
            app.uid = r.uid
            @addQuestion(r)
          )
          .fail((r)=>
            # 测试数据
            @trick?= '是么？那'
            @trick += '那'
            r =
              type: 'question'
              question: @trick + '你吃过Bug么？'
            @addQuestion(r)
          )

      answerQuestion: (e)->
        @hideUp()
        e = $(e.target)
        answer =
          uid: app.uid
          answer: e.val()
        @getQuestion(answer)
        @

      addQuestion: (gotQuestion)->
        queston = new Question(gotQuestion)
        @collection.add(queston)
        app.trigger 'getMovies', gotQuestion.movies_url
        @
