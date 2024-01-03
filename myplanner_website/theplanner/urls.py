from django.urls import path
from .views import HomeView
from .views import HomeDetailView
from .views import TaskView
from .views import TaskDetailView
from .views import SessionView
from .views import SessionDetailView
from .views import PlannerView
from .views import PlannerDetailView
from .views import CreateTaskView
from .views import EditTaskView
from .views import DeleteTaskView
from .views import CreateHomeEntryView

urlpatterns = [
    path('home/', HomeView.as_view(), name="home"),
    path('home/create/', CreateHomeEntryView.as_view(), name='create_home_entry'),
    path('home/<int:pk>', HomeDetailView.as_view(), name="home_details"),
    path('tasks/', TaskView.as_view(), name="task"),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name="task_details"),
    path('create_task/<int:pk>', CreateTaskView.as_view(), name="create_task"),
    path('task_details/edit/<int:pk>', EditTaskView.as_view(), name="edit_task"),
    path('task_details/<int:pk>/delete', DeleteTaskView.as_view(), name="delete_task"),
    path('sessions/', SessionView.as_view(), name="session"),
    path('session_details/<int:pk>', SessionDetailView.as_view(), name="session_details"),
    path('planner/', PlannerView.as_view(), name="planner"),
    path('planner_details/<int:pk>', PlannerDetailView.as_view(), name="planner_details"),
]
