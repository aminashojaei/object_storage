from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView
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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Object
    fields = ['title']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Object
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if (self.request.user == post.author):
            return True
        return False
