from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task, Home, Session, Planner, CalendarRow
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import HomeForm as HomeFormFunctionBased
from .forms import HomeForm
from django.db.models import Q
from django.http import JsonResponse

class HomeView(ListView):
    model = Home
    template_name = 'home.html'
    context_object_name = 'home_entries'

    def get_queryset(self):
        sort_option = self.request.GET.get('sort')

        if sort_option == 'start_time':
            return Home.objects.all().order_by('startTime')
        elif sort_option == 'duration':
            # Calculate duration and order by it
            return Home.objects.all().order_by('endTime', 'startTime')
        else:
            return Home.objects.all().order_by('startTime')
class CreateHomeEntryView(View):
    template_name = 'create_home_entry.html'

    def get(self, request, *args, **kwargs):
        form = HomeForm()
        return render(request, self.template_name, {'form': form, 'overlap_error': False})

    def post(self, request, *args, **kwargs):
	    form = HomeForm(request.POST)
	    error_message = None

	    if form.is_valid():
	        start_time = form.cleaned_data['startTime']
	        end_time = form.cleaned_data['endTime']

	        # Check for overlapping activities
	        overlapping_activities = Home.objects.filter(
	            Q(startTime__lte=start_time, endTime__gt=start_time) |
	            Q(startTime__lt=end_time, endTime__gte=end_time)
	        )

	        if overlapping_activities.exists():
	            error_message = "Error: Overlapping activities detected. Please choose a different time range."
	        else:
	            # Process the form data (save to the database, etc.)
	            form.save()
	            return redirect('home')

	    return render(request, self.template_name, {'form': form, 'error_message': error_message})
class HomeDetailView(DetailView):
	model = Home
	template_name = 'home_details.html'
class TaskView(ListView):
    model = Task
    template_name = 'tasks.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(task__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate the total and completed tasks
        total_tasks = context['object_list'].count()
        completed_tasks = context['object_list'].filter(completed=True).count()

        # Calculate the percentage completed (avoid division by zero)
        percentage_completed = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Add the calculated values to the context
        context['total_tasks'] = total_tasks
        context['completed_tasks'] = completed_tasks
        context['percentage_completed'] = percentage_completed

        return context

def task_list(request):
    if request.is_ajax():
        search_query = request.GET.get('search', '')
        tasks = Task.objects.filter(task__icontains=search_query)
        data = {'tasks': [{'id': task.id, 'task': task.task} for task in tasks]}
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'})
class TaskDetailView(DetailView):
	model = Task
	template_name = 'task_details.html'
class CreateTaskView(CreateView):
	model = Task
	template_name = 'create_task.html'
	fields = '__all__'
	success_url = reverse_lazy('task')
class EditTaskView(UpdateView):
	model = Task
	template_name = 'edit_task.html'
	fields = '__all__'
	success_url = reverse_lazy('task')
class DeleteTaskView(DeleteView):
	model = Task
	template_name = 'delete_task.html'
	fields = '__all__'
	success_url = reverse_lazy('task')
class SessionView(ListView):
	model = Session
	template_name = 'sessions.html'
class SessionDetailView(DetailView):
	model = Session
	template_name = 'session_details.html'
class PlannerView(ListView):
    model = Planner
    template_name = 'planner.html'
    context_object_name = 'planners'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar_rows'] = CalendarRow.objects.all()
        return context
class PlannerDetailView(DetailView):
	model = Planner
	template_name = 'planner_details.html'