from django.shortcuts import render, redirect

from app01 import models


def dept(request):
    data_list = models.Department.objects.order_by('id')
    return render(request, 'dept.html', {'data_list': data_list})


def dept_add(request):
    if request.method == "GET":
        return render(request, 'dept_add.html')
    if request.method == "POST":
        name = request.POST.get("name")
        models.Department.objects.create(Name=name)
        return redirect("/dept/")


def dept_del(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/dept/')


def dept_edit(request, nid):
    if request.method == "GET":
        row_obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'dept_edit.html', {'row_obj': row_obj})
    name = request.POST.get("Name")
    models.Department.objects.filter(id=nid).update(Name=name)
    return redirect("/dept/")
