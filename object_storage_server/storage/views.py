from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Object
from django.http import JsonResponse
from storage.s3_utils import S3ResourceSingleton, upload_file, objects_list, delete_file
from django.core.paginator import Paginator
from django.db.models import Sum
import boto3

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sum_size = 0
        print(context["objects"])
        for object in context["objects"]:
            print(object.file_name)
            sum_size += object.size
        context["sum_size"] = sum_size
        context["users"] = User.objects.all()
        return context


@login_required
def upload_file_view(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            file_name = file.name
            file_size = file.size
            file_type = file_name.split('.')[-1]
            obj = Object(
                file_name=file_name,
                size=file_size,
                file_format=file_type,
                owner=request.user
            )
            
            obj.save()

            success = upload_file(file, obj.pk)

            if success:
                return redirect("index")
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


@login_required
def update_permissions(request, pk):
    obj = get_object_or_404(Object, pk=pk)

    if obj.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit permissions for this object.")

    if request.method == 'POST':
        selected_users = request.POST.getlist("selected_users")
        users = User.objects.filter(username__in=selected_users)
        print(users)
        obj.permitted_users.set(users)
        obj.save()
        print("Success")
        return redirect("index")

    return redirect("index")


@csrf_exempt
def delete_file_view(request):
    # Initialize the Singleton with settings
    S3ResourceSingleton()

    if request.method == 'POST':
        file = json.loads(request.body)
        object_id = file["object_id"]
        success = delete_file(object_id)

        if success:
            Object.objects.get(id=object_id).delete()
            return JsonResponse({'message': 'File deleted successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Failed to delete file'}, status=500)
    else:
        return JsonResponse({'error': 'POST method required'}, status=400)


@login_required
def delete_object(request, pk):
    obj = get_object_or_404(Object, pk=pk)
    if obj.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this file.")
    
    S3ResourceSingleton()
    try:
        success = delete_file(obj.id)

    except boto3.exceptions.S3UploadFailedError:
        return HttpResponse("Failed to delete the file from S3", status=500)

    obj.delete()
    return redirect('index')