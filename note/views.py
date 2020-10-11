from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from note.models import NotePost
from note.forms import CreateNotePostForm, UpdateNotePostForm
from account.models import Account

NOTE_POSTS_PER_PAGE = 10


def create_note_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateNotePostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateNotePostForm()

	context['form'] = form

	return render(request, "note/create_note.html", context)


def detail_note_view(request, slug):

	context = {}

	note_post = get_object_or_404(NotePost, slug=slug)
	context['note_post'] = note_post

	return render(request, 'note/detail_note.html', context)



def edit_note_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	note_post = get_object_or_404(NotePost, slug=slug)

	if note_post.author != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateNotePostForm(request.POST or None, request.FILES or None, instance=note_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			note_post = obj

	form = UpdateNotePostForm(
			initial = {
					"title": note_post.title,
					"body": note_post.body,
			}
		)

	context['form'] = form
	return render(request, 'note/edit_note.html', context)


def get_note_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = NotePost.objects.filter(
				Q(title__icontains=q) | 
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))

def get_note_view(request):
	
	context = {}

	query = ""
	query = request.GET.get('q', '')
	context['query'] = str(query)
	print("get_note_view: " + str(query))

	note_posts = sorted(get_note_queryset(query), key=attrgetter('date_updated'), reverse=True)
	
	# Pagination
	page = request.GET.get('page', 1)
	note_posts_paginator = Paginator(note_posts, NOTE_POSTS_PER_PAGE)

	try:
		note_posts = note_posts_paginator.page(page)
	except PageNotAnInteger:
		note_posts = note_posts_paginator.page(NOTE_POSTS_PER_PAGE)
	except EmptyPage:
		note_posts = note_posts_paginator.page(note_posts_paginator.num_pages)

	context['note_posts'] = note_posts

	return render(request, "note/home.html", context)