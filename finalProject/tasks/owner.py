from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class OwnerListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return self.model.objects.all()


class OwnerDetailView(LoginRequiredMixin, DetailView):

    def get_queryset(self):
        return self.model.objects.all()


class OwnerCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.owner != request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.owner != request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)