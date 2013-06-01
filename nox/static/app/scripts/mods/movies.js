(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  define(['app', 'jquery', 'lodash', 'backbone'], function(app, $, _, Backbone) {
    var Movies, defaultMoive;

    defaultMoive = {
      noAction: true,
      cover_url: '/static/images/sample_cover.jpg',
      id: '0',
      name: '',
      director: '',
      summary: '没有什么电影能满足你了!!（╯‵□′）╯︵'
    };
    Movies = (function() {
      function Movies() {
        this.filter = __bind(this.filter, this);
        this["delete"] = __bind(this["delete"], this);
        this.update = __bind(this.update, this);
      }

      Movies.prototype.movieList = [];

      Movies.prototype.movieIdTrash = [];

      Movies.prototype.initialize = function() {};

      Movies.prototype.update = function(newList) {
        console.log(this.filter(newList));
        return this.movieList = this.filter(newList);
      };

      Movies.prototype["delete"] = function(movieId) {
        console.log('delete', movieId);
        this.movieIdTrash.push(movieId + '');
        this.update(this.movieList);
        return console.log('after delete', this.movieList);
      };

      Movies.prototype.filter = function(list) {
        var _this = this;

        return _.filter(list, function(e) {
          var _ref;

          return _ref = e.id, __indexOf.call(_this.movieIdTrash, _ref) < 0;
        });
      };

      Movies.prototype.bestOne = function() {
        if (this.movieList.length) {
          return this.movieList[0];
        } else {
          return defaultMoive;
        }
      };

      return Movies;

    })();
    _.extend(Movies.prototype, Backbone.Events);
    return Movies;
  });

}).call(this);
