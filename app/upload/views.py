# Import necessary modules and models

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Todo
from .forms import TodoForm,TaskSearchForm
from django.http import JsonResponse
from django.utils import timezone
from .models import Todo
from django.db.models import Count
from datetime import timedelta
from datetime import timedelta
import random
# Import random for testing with random dates
from datetime import datetime, timedelta

# Define the index view
def index(request):
	# Get all todo items and order them by ID
	todo_list = Todo.objects.order_by('id')
	# Create a new TodoForm instance
	form = TodoForm()
	# Create a context dictionary with the todo list and form
	context = {'todo_list' : todo_list, 'form' : form}
    # Render the index template with the context
	return render(request, 'todo/index.html', context)

# Define the addTodo view, which requires a POST request
@require_POST
def addTodo(request):
    # Create a new TodoForm instance with the POST data
	form = TodoForm(request.POST)
    # Check if the form is valid
	if form.is_valid():
    # Create a new Todo instance with the form data
			new_todo = Todo(text=request.POST['text'],
			complete=False,  # Default value, can be adjusted
            at=timezone.now().date())
    # Save the new Todo instance
			new_todo.save()
    # Redirect to the index view
	return redirect('index')

# Define the completeTodo view
def completeTodo(request, todo_id):
    # Get the Todo instance with the given ID
    todo = Todo.objects.get(pk=todo_id)
    # Mark the Todo instance as complete
    todo.complete = True
    # Update the completion date to the current date
    todo.at = timezone.now().date()
    # Save the changes
    todo.save()
    # Redirect to the index view
    return redirect('index')

# Define the taskList view
def taskList(request):
    # Create a new TaskSearchForm instance with the GET data
    form = TaskSearchForm(request.GET)
    # Get all Todo instances
    tasks = Todo.objects.all()
    # Get the search query from the GET data
    query = request.GET.get('query', '')
    # If a query is provided, filter the tasks by the query
    if query:
        tasks = tasks.filter(text__icontains=query)
    # Create a context dictionary with the tasks and form
    context = {
        'todo_list': tasks,
        'form': form,
    }
    # Render the taskList template with the context
    return render(request, 'todo/taskList.html', context)

# Define the deleteCompleted view
def deleteCompleted(request):
# Delete all completed Todo instances
	Todo.objects.filter(complete__exact=True).delete()
# Redirect to the index view
	return redirect('index')


# Define the deleteAll view
def deleteAll(request):
    # Delete all Todo instances
    Todo.objects.all().delete()
    # Redirect to the index view
    return redirect('index')

# Define the tasks_graph view
def tasks_graph(request):
    # Call the tasks_per_day_view function to get the context
    context = tasks_per_day_view(request)
    # Render the tasks_graph template with the context
    return render(request, 'todo/tasks_graph.html')

def tasks_per_day_view(request):
    # Define the time range for the past 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Query the database for completed tasks in the past 30 days
    tasks = Todo.objects.filter(complete=True, at__range=[start_date, end_date])

    # Count tasks per day
    tasks_per_day = (Todo.objects
                     .filter(complete=True, at__range=[start_date, end_date])
                     .values('at__date')  # Group by date
                     .annotate(count=Count('id'))  # Count tasks per day
                     .order_by('at__date'))  # Order by date
    
    # Count non-completed tasks per day
    tasks_per_day_not_completed = (
        Todo.objects
        .filter(complete=False, at__range=[start_date, end_date])
        .values('at__date')
        .annotate(count=Count('id'))
        .order_by('at__date')
    )

    # Create dictionaries to store the task counts
    completed_counts = {entry['at__date']: entry['count'] for entry in tasks_per_day}
    not_completed_counts = {entry['at__date']: entry['count'] for entry in tasks_per_day_not_completed}
    # Get all dates in the time range
    all_dates = sorted(set(completed_counts.keys()).union(not_completed_counts.keys()))

    context = {
        'dates': [date.strftime('%Y-%m-%d') for date in all_dates],
        'completed_counts': [completed_counts.get(date, 0) for date in all_dates],
        'not_completed_counts': [not_completed_counts.get(date, 0) for date in all_dates],
		'all_dates':[all_dates],
    }

    return JsonResponse(context)
