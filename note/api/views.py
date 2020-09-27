from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import JSONParser

from account.models import Account
from note.models import NotePost
from note.api.serializers import NotePostSerializer, NotePostUpdateSerializer, NotePostCreateSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_note_view(request, slug):

	try:
		note_post = NotePost.objects.get(slug=slug)
	except NotePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = NotePostSerializer(note_post)
		return Response(serializer.data)



@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_note_view(request, slug):

	try:
		note_post = NotePost.objects.get(slug=slug)
	except NotePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if note_post.author != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = NotePostUpdateSerializer(note_post, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = note_post.pk
			data['title'] = note_post.title
			data['body'] = note_post.body
			data['slug'] = note_post.slug
			data['date_updated'] = note_post.date_updated
			data['username'] = note_post.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_note_view(request, slug):

	try:
		note_post = NotePost.objects.get(slug=slug)
	except NotePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if note_post.author != user:
		return Response({'response': "You dont have permisson to delete that."})

	if request.method == "DELETE":
		operation = note_post.delete()
		data = {}
		if operation:
			data["success"] = "delete success"
		else:
			data["failure"] = "delete failed"
		return Response(data=data)




@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_note_view(request):

	if request.method == 'POST':
		
		mutable = request.POST._mutable
		request.POST._mutable = True

		print(request.user.pk)
		request.POST['author'] = request.user.pk
		
		request.POST._mutable = mutable

		print(request.data)
		data = request.data

		serializer = NotePostCreateSerializer(data=data)
		print(serializer)
		# set mutable flag back
		data._mutable = mutable

		data = {}
		if serializer.is_valid():
			note_post = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = note_post.pk
			data['title'] = note_post.title
			data['body'] = note_post.body
			data['slug'] = note_post.slug
			data['date_updated'] = note_post.date_updated
			data['username'] = note_post.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiNoteListView(ListAPIView):
	queryset = NotePost.objects.all()
	serializer_class = NotePostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'body', 'author__username')


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_author_of_notepost(request, slug):
	try:
		note_post = NotePost.objects.get(slug=slug)
	except NotePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if note_post.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)
	