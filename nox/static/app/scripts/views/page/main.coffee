define [
  'app'
  'jquery'
  'lodash'
  'backbone'
  'views/background'
  'views/question'
  'views/movie'
  'views/result'
  ], (app, $, _, Backbone,
    BackgroundView, QuestionView, MovieView, ResultView) ->

    class MainPage extends Backbone.View
      className: 'main-page'
      templateHtml: $('#main-page-tmpl').html()
      initialize: ->
        app.on 'getResult', @renderResult
        app.on 'getMovies', @renderMoive
        app.on 'restart', @restart

      restart: =>
        app.questionView.remove()
        app.movieView.remove()
        delete app.uid
        delete app.questionView
        delete app.movieView
        @render()
      render: =>
        (new BackgroundView()).render()
        @$el.html(@templateHtml)
        @content = @$el.find('.content')
        @renderQuestion()
        @renderMoive()
        @

      renderQuestion: =>
        if not app.questionView
          app.questionView = new QuestionView()
          @content.find('.question-wrapper')
            .replaceWith(app.questionView.render().el)
        else
          app.questionView.render()

      renderMoive: (moviesUrl)=>
        if not app.movieView
          app.movieView = new MovieView()
          @content.find('.movie-panel')
            .replaceWith(app.movieView.renderLoading().el)
        else
          app.movieView.renderLoading()

        if moviesUrl
          app.movieView.setUrl moviesUrl

      renderResult: (option={})=>
        resultView = new ResultView(option)

        @conent
          .append(resultView.render().el)

