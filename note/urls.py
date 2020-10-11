from django.urls import path
from note.views import (
	create_note_view,
	detail_note_view,
	edit_note_view,
	get_note_view,
)

app_name = 'note'

urlpatterns = [
    path('', get_note_view, name="note"),
    path('create', create_note_view, name="create"),
    path('<slug>/', detail_note_view, name="detail"),
    path('<slug>/edit/', edit_note_view, name="edit"),
 ]