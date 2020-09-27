from django.urls import path
from note.api.views import(
	api_detail_note_view,
	api_update_note_view,
	api_delete_note_view,
	api_create_note_view,
	api_is_author_of_notepost,
	ApiNoteListView
)

app_name = 'note'

urlpatterns = [
	path('<slug>/', api_detail_note_view, name="detail"),
	path('<slug>/update', api_update_note_view, name="update"),
	path('<slug>/delete', api_delete_note_view, name="delete"),
	path('create', api_create_note_view, name="create"),
	path('list', ApiNoteListView.as_view(), name="list"),
	path('<slug>/is_author', api_is_author_of_notepost, name="is_author"),
]