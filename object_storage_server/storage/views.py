from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User

from .forms import ObjectPermissionForm
from .models import Object
import json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Object
from django.http import JsonResponse
from django.conf import settings
from storage.s3_utils import S3ResourceSingleton, upload_file, objects_list, delete_file
from django.core.paginator import Paginator
from django.db.models import Sum

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Object

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


@csrf_exempt
def upload_file_view(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            file_name = file.name
            file_size = file.size
            dot_position = file_name.rfind('.')
            if dot_position != -1:
                file_type = file_name[dot_position + 1:]
            else:
                file_type = ''

            # ایجاد شیء Object
            obj = Object(
                file_name=file_name,
                size=file_size,
                type=file_type,
                owner=request.user 
            )
            obj.save()

            # آپلود فایل با استفاده از تابع `upload_file از utils.py
            success = upload_file(file , obj.id)

            if success:
                return JsonResponse({'message': 'File uploaded successfully'}, status=200)
            else:
                return JsonResponse({'message': 'Failed to upload file'}, status=500)
        except UnicodeEncodeError as e:
            print(f"UnicodeEncodeError: {e}")
            return JsonResponse({'message': 'Failed to encode file name'}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'message': 'An error occurred'}, status=500)
    else:
        return render(request, 'storage/upload_file.html')


from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Object

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

def objects_list_view(request):
    # Initialize the Singleton with settings
    S3ResourceSingleton()

    if request.method == 'GET':
        total_size = 0

        query = request.GET.get('query', None)
        page_number = request.GET.get('page')

        object_key = objects_list()
        if object_key is not None:

            # Fetch objects owned by the logged-in user
            owned_objects = Object.objects.filter(owner=request.user)
            if owned_objects.exists():
                total_size1 = owned_objects.aggregate(total_size=Sum('size'))['total_size'] or 0
                total_size += total_size1

            # Fetch objects accessed by the logged-in user
            # accessed_objects = request.user.accessed_objects.all()
            # if accessed_objects.exists():
            #     total_size2 = accessed_objects.aggregate(total_size=Sum('size'))['total_size'] or 0
            #     total_size += total_size2

            # Check if there is a query in the search bar
            # if query:
            #     owned_objects = owned_objects.filter(file_name__icontains=query)
            #     accessed_objects = accessed_objects.filter(file_name__icontains=query)

            # Combine both query sets into a single list
            list_of_objects = list(owned_objects) #+ list(accessed_objects)

            # Use Django's paginator to paginate the combined list
            paginator = Paginator(list_of_objects, 3)
            page_objects = paginator.get_page(page_number)

            # Render the template with the context
            return render(request, 'storage/objects_list.html', {
                'message': 'List of objects showed successfully',
                'list_of_objects': page_objects,  # Pass paginated objects directly
                'total_pages': page_objects.paginator.num_pages,
                'total_size': total_size,
                'query': query,
                'current_page': page_objects.number,
            })

        else:
            return render(request, 'storage/objects_list.html', {
                'message': 'Failed to show list of objects',
                'list_of_objects': [],
                'total_pages': 0,
                'total_size': total_size,
            })
    else:
        return render(request, 'storage/objects_list.html', {
            'error': 'GET method required'
        })

