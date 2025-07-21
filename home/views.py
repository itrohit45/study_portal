from django.shortcuts import render, redirect
from .models import Notes, Homework, ToDo
import wikipedia
from django.conf import settings
import requests

# Create your views here.

def Home(request):
    return render(request, 'home/home.html')

def note(request):
   
    notes = Notes.objects.filter(user=request.user)

    if request.method == 'POST':
        user=request.user
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Notes.objects.create(user=user,title=title,description=description)
            return redirect('notes')
        
    context = {
        'notes': notes,
    }    
    return render(request, 'home/notes.html', context)


def note_detail(request, pk):
    note = Notes.objects.get(pk=pk)
    context ={
        'note':note
    }

    return render(request, 'home/notes-details.html', context)


def note_delete(request, pk):
    note = Notes.objects.get(pk=pk)
    note.delete()
    return redirect('notes')


def homework(request):
    homeworks = Homework.objects.filter(user=request.user)
    context = {
        'homeworks':homeworks
    }
    if request.method == 'POST':
        user=request.user
        subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due = request.POST.get('due')
        is_finished = request.POST.get('is_finished', False)

        homework = Homework.objects.create(
            user=user,
            subject=subject,
            title=title,
            description=description,
            due=due,
            is_finished=is_finished
        )
        homework.save()
        return redirect('homework')
    return render(request, 'home/homework.html', context)    




def delete_homework(request, homework_id):
    
    homework = Homework.objects.get(id=homework_id)
    homework.delete()
    return redirect('homework')  


def todo(request):
    todos = ToDo.objects.filter(user=request.user)
    todos_done = todos.filter(is_finished=True)
    return render(request, 'home/todo.html', {'todos':todos, 'todos_done': todos_done})

def create_todo(request):
    if request.method == 'POST':
        user=request.user
        title = request.POST.get('title')
        ToDo.objects.create(user=user,title=title)
    return redirect('todo')


def delete_todo(request, todo_id):

    if request.method == 'POST':
        todo = ToDo.objects.get(id = todo_id)
        todo.delete()
    return redirect('todo')


def conversion(request):
    context = {'input': False, 'answer': '', 'error': '', 'measurement': ''}

    if request.method == 'POST':
        measurement = request.POST.get('measurement')
        context['measurement'] = measurement

        if measurement in ['length', 'mass']:
            context['input'] = True
            measure1 = request.POST.get('measure1')
            measure2 = request.POST.get('measure2')
            input_value = request.POST.get('input')

            try:
                value = float(input_value)

                if value < 0:
                    context['error'] = 'Please enter a non-negative number.'
                else:
                    if measurement == 'length':
                        if measure1 == 'yard' and measure2 == 'foot':
                            context['answer'] = f'{value} yard = {value * 3} foot'
                        elif measure1 == 'foot' and measure2 == 'yard':
                            context['answer'] = f'{value} foot = {value / 3} yard'
                        else:
                            context['error'] = 'Invalid length units selected.'
                    elif measurement == 'mass':
                        if measure1 == 'pound' and measure2 == 'kilogram':
                            context['answer'] = f'{value} pound = {value * 0.453592:.4f} kilogram'
                        elif measure1 == 'kilogram' and measure2 == 'pound':
                            context['answer'] = f'{value} kilogram = {value * 2.20462:.4f} pound'
                        else:
                            context['error'] = 'Invalid mass units selected.'
            except (ValueError, TypeError):
                context['error'] = 'Please enter a valid number.'

        else:
            context['error'] = 'Invalid measurement type.'

    return render(request, 'home/conversion.html', context)

def wikipedia_view(request):
    context = {}
    if request.method == 'POST':
        text = request.POST.get('search_query')
        if text:
            try:
                page = wikipedia.page(text)
                context = {
                    'title': page.title,
                    'link': page.url,
                    'details': page.summary
                }
            except wikipedia.exceptions.DisambiguationError as e:
                context = {'error_message': f"Multiple results found: {e.options}"}
            except wikipedia.exceptions.PageError:
                context = {'error_message': "No page found with that title."}
            except Exception as e:
                context = {'error_message': f"An unexpected error occurred: {str(e)}"}
        else:
            context = {'error_message': 'Please enter a search query.'}
    return render(request, 'home/wikipedia.html', context)


def contact(request):
    return render(request, 'home/contactus.html')


def search_books(request):
    books = []
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            api_key = 'AIzaSyDgiMyWVKzisR-oV3Ey3REu7g_ZldObN8k'
            url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}'
            response = requests.get(url)
            data = response.json()
            if 'items' in data:
                books = data['items']
    return render(request, 'home/book.html', {'books': books})
