from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from .forms import ObjectPermissionForm
from .models import Object

@login_required
def index(request):
    objects = [
        {'name': 'App School.fig', 'size': '10 GB', 'date_modified': '10 Oct'},
        {'name': 'BC Company.sketch', 'size': '10 GB', 'date_modified': '10 Oct'},
        {'name': 'BC Company.sketch', 'size': '10 GB', 'date_modified': '10 Oct'},
        {'name': 'BC Company.sketch', 'size': '10 GB', 'date_modified': '10 Oct'},
        {'name': 'BC Company.sketch', 'size': '10 GB', 'date_modified': '10 Oct'},
        {'name': 'BC Company.sketch', 'size': '10 GB', 'date_modified': '10 Oct'},
    ]
    context = {
        'objects': objects,
        'title': 'Home'
    }
    
    return render(request, 'storage/viewlist.html', context)


class ObjectListView(LoginRequiredMixin, ListView):

    model = Object
    template_name = 'storage/viewlist.html'
    context_object_name = 'objects'
    ordering = ['-date_posted']
    paginate_by = 24

    def get_queryset(self):
        user = self.request.user
        return Object.objects.filter(owner=user) | Object.objects.filter(permitted_users=user)


class ObjectCreateView(LoginRequiredMixin, CreateView):
    model = Object
    fields = ['title']


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Object
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if (self.request.user == post.author):
            return True
        return False


class ObjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Object
    form_class = ObjectPermissionForm
    fields = ['permitted_users']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if (self.request.user == obj.owner):
            return True
        return False


@login_required
def update_permissions(request, pk):
    obj = get_object_or_404(Object, pk=pk)
    
    if obj.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit permissions for this object.")

    if request.method == 'POST':
        form = ObjectPermissionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('object_detail', pk=obj.pk)
    else:
        form = ObjectPermissionForm(instance=obj)
    
    return render(request, 'object_permissions.html', {'form': form, 'object': obj})
