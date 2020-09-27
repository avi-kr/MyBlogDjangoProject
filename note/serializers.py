from rest_framework import serializers
from note.models import NotePost

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


class NotePostSerializer(serializers.ModelSerializer):

	username 		= serializers.SerializerMethodField('get_username_from_author')
	
	class Meta:
		model = NotePost
		fields = ['pk', 'title', 'slug', 'body', 'date_updated', 'username']


	def get_username_from_author(self, note_post):
		username = note_post.author.username
		return username

class NotePostUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = NotePost
		fields = ['title', 'body']

	def validate(self, note_post):
		try:
			title = note_post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			body = note_post['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
		
		except KeyError:
			pass
		return note_post



class NotePostCreateSerializer(serializers.ModelSerializer):


	class Meta:
		model = NotePost
		fields = ['title', 'body', 'date_updated', 'author']


	def save(self):
		
		try:
			image = self.validated_data['image']
			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			body = self.validated_data['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			
			note_post = NotePost(
								author=self.validated_data['author'],
								title=title,
								body=body,
								)

			note_post.save()
			return note_post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title, some content."})






