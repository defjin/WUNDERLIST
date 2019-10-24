from django.shortcuts import render, get_object_or_404
from .models import Music, Comment, Artist
from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer, ArtistDetailSerializer, MusicDetailSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def music_list(request):
    musics = Music.objects.all()
    serializer = MusicSerializer(musics, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def music_detail(request, music_pk):
    music = get_object_or_404(Music, pk = music_pk)
    serializer = MusicDetailSerializer(music)
    return Response(serializer.data)

@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk = artist_pk)
    serializer = ArtistDetailSerializer(artist)
    return Response(serializer.data)

@api_view(['POST'])
def comments_create(request, music_pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(music_id=music_pk)
    return Response(serializer.data)

# @api_view(['GET'])
# def comment_list(request):
#     comments = Comment.objects.all()
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)   

# @api_view(['GET'])
# def comment_detail(request, comment_pk):
#     comment = get_object_or_404(Comment, pk = comment_pk)
#     serializer = MusicSerializer(comment)
#     return Response(serializer.data)