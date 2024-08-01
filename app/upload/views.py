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

def index(request):
	todo_list = Todo.objects.order_by('id')
	form = TodoForm()
	context = {'todo_list' : todo_list, 'form' : form}

	return render(request, 'todo/index.html', context)

@require_POST
def addTodo(request):
	form = TodoForm(request.POST)

	if form.is_valid():
			new_todo = Todo(text=request.POST['text'],
			complete=False,  # Default value, can be adjusted
            at=timezone.now().date())
			new_todo.save()

	return redirect('index')

def completeTodo(request, todo_id):
	todo = Todo.objects.get(pk=todo_id)
	todo.complete = True
	# end_date = timezone.now().date()
	# start_date = end_date - timedelta(days=30)
	# start_date_ordinal = start_date.toordinal()
	# end_date_ordinal = end_date.toordinal()
	# random_ordinal = random.randint(start_date_ordinal, end_date_ordinal)
	# todo_date = datetime.fromordinal(random_ordinal).date()  
	todo.at = timezone.now().date()
	todo.save()  
# Save the changes to the database
    

	return redirect('index')
def taskList(request):
    form = TaskSearchForm(request.GET)
    tasks = Todo.objects.all()
    
    # Get the search query from GET parameters
    query = request.GET.get('query', '')

    if query:
        tasks = tasks.filter(text__icontains=query)


    context = {
        'todo_list': tasks,
        'form': form,
    }
    return render(request, 'todo/taskList.html', context)

def deleteCompleted(request):
	Todo.objects.filter(complete__exact=True).delete()
	return redirect('index')

def deleteAll(request):
	Todo.objects.all().delete()
	return redirect('index')
def tasks_graph(request):
    context = tasks_per_day_view(request)
    
    # Render the tasks_graph template with the context
    # response_data = {
    #     'dates': [entry['at__date'] for entry in tasks_per_day],
    #     'counts': [entry['count'] for entry in tasks_per_day],
    # }

    
    # Return JSON response
	# redirect ('index')
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
    
    tasks_per_day_not_completed = (
        Todo.objects
        .filter(complete=False, at__range=[start_date, end_date])
        .values('at__date')
        .annotate(count=Count('id'))
        .order_by('at__date')
    )
    completed_counts = {entry['at__date']: entry['count'] for entry in tasks_per_day}
    not_completed_counts = {entry['at__date']: entry['count'] for entry in tasks_per_day_not_completed}
    all_dates = sorted(set(completed_counts.keys()).union(not_completed_counts.keys()))

    context = {
        'dates': [date.strftime('%Y-%m-%d') for date in all_dates],
        'completed_counts': [completed_counts.get(date, 0) for date in all_dates],
        'not_completed_counts': [not_completed_counts.get(date, 0) for date in all_dates],
		'all_dates':[all_dates],
    }
    return JsonResponse(context)
# context = {
    #     'dates': [entry['at__date'] for entry in tasks_per_day],
    #     'counts': [entry['count'] for entry in tasks_per_day],
	# 	'not_completed_counts_dates': [entry['at__date'] for entry in tasks_per_day_not_completed],
	# 	'not_completed_counts_count': [entry['count'] for entry in tasks_per_day_not_completed],
    # }