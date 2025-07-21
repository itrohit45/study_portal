from django.urls import path
from . import views


urlpatterns = [
   path('home',views.Home,name='home'),
   path('books/', views.search_books, name='search_books'),
   path('notes',views.note,name='notes'),
   path('note-detail/<int:pk>',views.note_detail,name='notedetail'),    
   path('note-delete/<int:pk>',views.note_delete,name='notedelete'), 
   path('homework',views.homework,name='homework'),  
   path('homework/<int:homework_id>',views.delete_homework,name='delete_homework'),  
   path('todo',views.todo,name='todo'),    
   path('create-todo',views.create_todo,name='create-todo'),    
   path('delete-todo/<int:todo_id>',views.delete_todo,name='delete-todo'),
   path('conversion',views.conversion,name='conversion'),   
   path('wikipedia',views.wikipedia_view,name='wikipedia'),
   path('contact',views.contact,name='contact'),

]