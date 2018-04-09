from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from .forms import *
from django.db.utils import IntegrityError
from django.conf import settings
import logging, requests
import os

login_form = LoginForm
logger = logging.getLogger(__name__)

# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"],
                                password=cd["password"])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    messages.success(request, "You have been logged in sucessfully.")
                    if not request.user.is_superuser:
                        return redirect("uploaded_files")
                    else:
                        return redirect("users")
            else:
                return render(request, "account/login.html", dict(form=login_form, disabled=True))
        else:
            return render(request, "account/login.html", dict(form=login_form))
    else:
        return render(request, "account/login.html", dict(form=login_form))


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            tools_available = ToolsDone(user=new_user)
            tools_available.save()
            messages.success(request, "You have been registered sucessfully.")
            return redirect("login")
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      "account/register.html",
                      dict(user_form=user_form))


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


@login_required
def uploaded_files(request):
    if request.method == "POST":
        if 'upload' in request.POST:
            file_form = UploadFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                uploaded_path = file_form.cleaned_data["uploaded_path"]
                title = request.FILES['uploaded_path'].name
                file = File(title=title, uploaded_path=uploaded_path, user=request.user)
                try:
                    file.save()
                    messages.success(request, "Successfully added a file.")
                    return redirect("uploaded_files")
                except IntegrityError:
                    messages.error(request, "Duplicated filename! Please change name of your csv file")
                    return redirect("uploaded_files")
            else:
                messages.error(request, "Wrong file extension!")
                return redirect("uploaded_files")
        elif 'visualizations' in request.POST:
            title_index = request.POST.get("index_name")
            data = {"title": title_index, "timeFieldName": "@timestamp"}
            headers = {'Content-Type': 'application/json', }
            dataMapping = {"mappings": {"map": {
                "properties": {"FTHG": {"type": "integer"}, "HG": {"type": "integer"}, "FTAG": {"type": "integer"},
                               "AG": {"type": "integer"}, "HTHG": {"type": "integer"}, "HTAG": {"type": "integer"},
                               "Attendance": {"type": "long"}, "HS": {"type": "integer"}, "AS": {"type": "integer"},
                               "HST": {"type": "integer"}, "AST": {"type": "integer"}, "HHW": {"type": "integer"},
                               "AHW": {"type": "integer"}, "HC": {"type": "integer"}, "AC": {"type": "integer"},
                               "HF": {"type": "integer"}, "AF": {"type": "integer"}, "HO": {"type": "integer"},
                               "AO": {"type": "integer"}, "HY": {"type": "integer"}, "AY": {"type": "integer"},
                               "HR": {"type": "integer"}, "AR": {"type": "integer"}, "HBP": {"type": "integer"},
                               "ABP": {"type": "integer"}, "B365H": {"type": "float"}, "B365D": {"type": "float"},
                               "B365A": {"type": "float"}, "BSH": {"type": "float"}, "BSD": {"type": "float"},
                               "BSA": {"type": "float"}, "BWH": {"type": "float"}, "BWD": {"type": "float"},
                               "BWA": {"type": "float"}, "GBH": {"type": "float"}, "GBD": {"type": "float"},
                               "GBA": {"type": "float"}, "IWH": {"type": "float"}, "IWD": {"type": "float"},
                               "IWA": {"type": "float"}, "LBH": {"type": "float"}, "LBD": {"type": "float"},
                               "LBA": {"type": "float"}, "PSH": {"type": "float"}, "PH": {"type": "float"},
                               "PSD": {"type": "float"}, "PD": {"type": "float"}, "PSA": {"type": "float"},
                               "PA": {"type": "float"}, "SOH": {"type": "float"}, "SOD": {"type": "float"},
                               "SOA": {"type": "float"}, "SBH": {"type": "float"}, "SBD": {"type": "float"},
                               "SBA": {"type": "float"}, "SJH": {"type": "float"}, "SJD": {"type": "float"},
                               "SJA": {"type": "float"}, "SYH": {"type": "float"}, "SYD": {"type": "float"},
                               "SYA": {"type": "float"}, "VCH": {"type": "float"}, "VCD": {"type": "float"},
                               "VCA": {"type": "float"}, "WHH": {"type": "float"}, "WHD": {"type": "float"},
                               "WHA": {"type": "float"}, "BbOU": {"type": "integer"}, "BbMx>2.5": {"type": "float"},
                               "BbAv>2.5": {"type": "float"}, "BbMx<2.5": {"type": "float"},
                               "BbAv<2.5": {"type": "float"}, "GB>2.5": {"type": "float"}, "GB<2.5": {"type": "float"},
                               "B365>2.5": {"type": "float"}, "B365<2.5": {"type": "float"},
                               "Bb1X2": {"type": "integer"}, "BbMxH": {"type": "float"}, "BbAvH": {"type": "float"},
                               "BbMxD": {"type": "float"}, "BbAvD": {"type": "float"}, "BbMxA": {"type": "float"},
                               "BbAvA": {"type": "float"}, "MaxH": {"type": "float"}, "MaxD": {"type": "float"},
                               "MaxA": {"type": "float"}, "AvgH": {"type": "float"}, "AvgD": {"type": "float"},
                               "AvgA": {"type": "float"}, "BbAH": {"type": "integer"}, "BbAHh": {"type": "float"},
                               "BbMxAHH": {"type": "float"}, "BbAvAHH": {"type": "float"}, "BbMxAHA": {"type": "float"},
                               "BbAvAHA": {"type": "float"}, "GBAHH": {"type": "float"}, "GBAHA": {"type": "float"},
                               "GBAH": {"type": "float"}, "LBAHH": {"type": "float"}, "LBAHA": {"type": "float"},
                               "LBAH": {"type": "float"}, "B365AHH": {"type": "float"}, "B365AHA": {"type": "float"},
                               "B365AH": {"type": "float"}, "PSCH": {"type": "float"}, "PSCD": {"type": "float"},
                               "PSCA": {"type": "float"}, "Date": {"type": "date", "format": "dd/MM/yy"}}}}}
            requests.put('http://localhost:9200/' + title_index, headers=headers, json=dataMapping)
            dataReindex = {"source": {"index": title_index + '_tmp'}, "dest": {"index": title_index}}
            requests.post('http://localhost:9200/_reindex', headers=headers, json=dataReindex)
            requests.post('http://localhost:9200/.kibana' + str(request.user.id) + '/index-pattern/'
                          + title_index, json=data)
            requests.delete('http://localhost:9200/' + title_index + '_tmp')
            file = File.objects.get(id=request.POST.get('index_id'))
            file.visualisations = True
            file.save()
            for x in range(1,3):
                file = open('/home/bartek/workspace/pycharm/football_static/visualizations/visualization'+str(x), 'r')
                data = file.read()
                data = data.replace("tmp", request.POST.get('index_name'))
                requests.post('http://localhost:9200/.kibana' + str(request.user.id) + '/visualization', data=data)
            messages.success(request, "Your visualisations were created!")
            return redirect('uploaded_files')
        elif 'delete' in request.POST:
            file = File.objects.get(id=request.POST.get('index_id'))
            file.delete()
            title_index = request.POST.get("index_name")
            requests.delete('http://localhost:9200/' + title_index)
            requests.delete('http://localhost:9200/' + title_index + '_tmp')
            requests.delete('http://localhost:9200/.kibana' + str(request.user.id) + '/index-pattern/' + title_index)
            os.remove(os.path.join(settings.MEDIA_ROOT, request.POST.get("file_with_ext")))
            return redirect('uploaded_files')
        else:
            messages.error(request, "Errors occured!")
            return HttpResponseRedirect("")
    else:
        files = File.objects.filter(user=request.user)
        file_form = UploadFileForm()
        if not request.user.is_superuser:
            tool = ToolsDone.objects.get(user=request.user)
        else:
            tool = ToolsDone(isDone=True, user=request.user)
        return render(request, "uploaded_files.html", dict(file_form=file_form, files=files, tool=tool))


@login_required
def edit_user(request, user_id):
    if request.method == "POST":
        form = EditUserForm(request.POST)
        if form.is_valid():
            edited_user = User.objects.get(pk=form.cleaned_data["id"])
            edited_user.email = form.cleaned_data["email"]
            edited_user.first_name = form.cleaned_data["first_name"]
            edited_user.last_name = form.cleaned_data["last_name"]
            edited_user.save()
            messages.success(request, "User data has been updated successfully.")
            return redirect(form.cleaned_data["next"])
        else:
            user_to_edit = User.objects.get(pk=user_id)
            user_form = EditUserForm(instance=user_to_edit)
            messages.error(request, "Failed to update the user.")
            return render(request,
                          "edit_user.html",
                          dict(user_form=user_form))
    else:
        user_to_edit = User.objects.get(pk=user_id)
        user_form = EditUserForm(instance=user_to_edit)
        return render(request,
                      "edit_user.html",
                      dict(user_form=user_form))


def info(request):
    return render(request, "info.html")


@staff_member_required
def users(request):
    if request.method == "POST":
        tool = ToolsDone.objects.get(id=request.POST.get('tool_id'))
        if 'allow' in request.POST:
            tool.isDone = True
            tool.port = request.POST.get('port')
        else:
            tool.isDone = False
        tool.save()
        return redirect("users")
    else:
        all_users = User.objects.exclude(username="admin").order_by("id")
        all_tools_done = ToolsDone.objects.order_by("user_id")
        return render(request, "users.html", dict(users=all_users, tools=all_tools_done))


@staff_member_required
def users_files(request):
    files = File.objects.order_by("uploaded_at")
    return render(request, "users_files.html", dict(files=files))