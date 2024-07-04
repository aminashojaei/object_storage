from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User

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
        'users': User.objects.all(),
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


@login_required
def update_permissions(request, pk):
    obj = get_object_or_404(Object, pk=pk)
    
    if obj.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit permissions for this object.")

    if request.method == 'POST':
        selected_users = request.POST.getlist("selected_users")
        users = User.objects.filter(username__in=selected_users)
        obj.permitted_users.set(users)
        obj.save()
        return redirect("index")
    
    return redirect("index")
