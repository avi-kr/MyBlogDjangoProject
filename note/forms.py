from django import forms

from note.models import NotePost 


class CreateNotePostForm(forms.ModelForm):

	class Meta:
		model = NotePost
		fields = ['title', 'body']


class UpdateNotePostForm(forms.ModelForm):

	class Meta:
		model = NotePost
		fields = ['title', 'body']

	def save(self, commit=True):
		note_post = self.instance
		note_post.title = self.cleaned_data['title']
		note_post.body = self.cleaned_data['body']


		if commit:
			note_post.save()
		return note_post