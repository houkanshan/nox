import os
import urllib2
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response

from movie.models import Movie, Question, Answer
from movie.serializers import AnswerSerializer, QuestionSerializer, MovieSerializer



def index_view(request):
    return render(request, "index.html")

def photo_view(request, pid):
    photo_url = "http://img3.douban.com/lpic/s" + pid + ".jpg"
    dest_addr = os.path.join(settings.COVER_PATH, "..", "cover/", pid, ".jpg")
    stream = urllib2.urlopen(photo_url)
    new_file = open(dest_addr, "wb")
    new_file.write(stream.read())
    new_file.close()
    return HttpResponse(dest_addr)


class MovieViewSet(viewsets.ViewSetMixin,
                   generics.GenericAPIView,
                   mixins.SubModelMixin):

    serializer_class = MovieSerializer
    def get_movies(self, request, *args, **kwargs):
        movies = []
        """
        movie = Movie(name="a", directors=["a"], actors=["a"],
                      types=["a"], countries=["a"], languages='a',
                      year='a', length='a', rate='a',
                      watcher='a', tags=["a"])
        bmovie = Movie(name="b", directors=["b"], actors=["b"],
                      types=["b"], countries=["b"], languages=["b"],
                      year='b', length='b', rate='b',
                      watcher='b', tags=["b"])
        """
        movie = Movie(id="3642843", name="a", directors="a", actors="a",
                      types="a", countries="a", languages='a',
                      year='a', length='a', rate='a',
                      watcher='a', tags="a", cover_url="/photos/3624843")
        bmovie = Movie(id="11529526", name="b", directors="b", actors="b",
                      types="b", countries="b", languages="b",
                      year='b', length='b', rate='b',
                      watcher='b', tags="b", cover_url="/photos/3624843")
        movies.append(movie)
        movies.append(bmovie)
        movie_json = MovieSerializer(movies)
        return Response(movie_json.data)


class QuestionViewSet(viewsets.ViewSetMixin,
                      generics.GenericAPIView):

    serializer_class = QuestionSerializer
    def answer_question(self, request, *args, **kwargs):
        answer = Answer(request.DATA)
        question = Question(pk=1, question="asda")
        question_json = QuestionSerializer(question)
        return Response(question_json.data)

    def ask_question(self, request, *args, **kwargs):
        _view = MovieViewSet.as_view({'get': 'get_movies'})
        return _view(request, args, kwargs)



