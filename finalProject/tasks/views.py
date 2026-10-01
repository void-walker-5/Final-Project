from django.urls import reverse_lazy

from .models import Task
from .owner import (
    OwnerListView,
    OwnerDetailView,
    OwnerCreateView,
    OwnerUpdateView,
    OwnerDeleteView,
)


class TaskListView(OwnerListView):
    model = Task
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search', '').strip()

        if search:
            from django.db.models import Q

            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset.order_by('-updated_at')


class TaskDetailView(OwnerDetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(OwnerCreateView):
    model = Task
    template_name = 'tasks/task_form.html'

    fields = ['title', 'description', 'status']

    success_url = reverse_lazy('tasks:all')


class TaskUpdateView(OwnerUpdateView):
    model = Task
    template_name = 'tasks/task_form.html'

    fields = ['title', 'description', 'status']

    success_url = reverse_lazy('tasks:all')


class TaskDeleteView(OwnerDeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'

    success_url = reverse_lazy('tasks:all')

    