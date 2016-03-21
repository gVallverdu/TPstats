from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from . import models
from . import forms

import pandas as pd
# Create your views here.


def home(request):
    exps = models.Experiment.objects.all()
    return render(request, 'collectDatas/home.html', {"exps": exps})


def new_experiment(request):
    if request.method == "POST":
        form = forms.ExperimentForm(request.POST)
        if form.is_valid():
            exp = form.save()
            return redirect("collectDatas.views.home")
    else:
        form = forms.ExperimentForm()
    return render(request, "collectDatas/new_exp.html", {"form": form})


def edit_experiment(request, exp_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    if request.method == "POST":
        form = forms.ExperimentForm(request.POST, instance=exp)
        if form.is_valid():
            exp = form.save()
            return redirect("collectDatas.views.home")
    else:
        form = forms.ExperimentForm(instance=exp)
    context = {'form': form, "exp": exp}
    return render(request, "collectDatas/new_exp.html", context)


def detail_experiment(request, exp_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    glasswares = models.Glassware.objects.all()

    # collect datas from database
    data = dict()
    ndatamax = 0
    for g in glasswares:
        measures = models.Measure.objects.filter(experiment=exp, glassware=g)
        if len(measures) != 0:
            ndatamax = max(len(measures), ndatamax)
            data[g.get_glassware_display()] = [m.value for m in measures]

    # add needed values to have homogeneous lengths
    for glassware, measures in data.items():
        measures += (ndatamax - len(measures)) * [0.]
        data[glassware] = measures

    # convert to html tab
    # htmldata = "<table class='table'>\n"
    # htmldata += "  <thead>\n"
    # htmldata += "    <tr>\n"
    #
    # for glassware in data:
    #     htmldata += "      <th>%s</th>\n" % glassware
    # htmldata += "    </tr>\n"
    # htmldata += "  </thead>\n"
    # htmldata += "  <tbody>\n"
    #
    # for i in range(ndatamax):
    #     htmldata += "    <tr>\n"
    #     for glassware in data:
    #         if data[glassware][i] < 0.:
    #             val = " "
    #         else:
    #             val = "%6.2f" % data[glassware][i]
    #         htmldata += "      <td>%s</td>\n" % val
    #     htmldata += "    </tr>\n"
    # htmldata += "  </tbody>\n"
    # htmldata += "</table>\n"

    htmldata = pd.DataFrame(data).to_html(float_format="%6.2f", index=False, classes="table")

    context = {"exp": exp, "htmldata": htmldata}
    return render(request, 'collectDatas/experiment.html', context)


def download_exp_data(request, exp_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    glasswares = models.Glassware.objects.all()

    # collect datas from database
    data = dict()
    ndatamax = 0
    for g in glasswares:
        measures = models.Measure.objects.filter(experiment=exp, glassware=g)
        if len(measures) != 0:
            ndatamax = max(len(measures), ndatamax)
            data[g.get_glassware_display()] = [m.value for m in measures]

    # add needed values to have homogeneous lengths
    for glassware, measures in data.items():
        measures += (ndatamax - len(measures)) * [0.]
        data[glassware] = measures

    csvfile = pd.DataFrame(data).to_csv(index=False)

    response = HttpResponse(csvfile, content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % exp.name.replace(" ", "_")

    return response


def delete_experiment(request, exp_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    exp.delete()
    return redirect("collectDatas.views.home")


def manage_measures(request, exp_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    glasswares = models.Glassware.objects.all()

    # collect datas from database
    datas = dict()
    for glassware in glasswares:
        measures = models.Measure.objects.filter(experiment=exp, glassware=glassware)
        if len(measures) != 0:
            datas[glassware] = measures.order_by("-date")

    if request.method == "POST":
        return redirect("collectDatas.views.detail_experiment", exp_id=exp_id)

    else:
        # add needed values to have homogeneous lengths

        context = {"exp": exp, "datas": datas}
    return render(request, 'collectDatas/manage_measures.html', context)


def new_measure(request, exp_id, glass_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    glassware = get_object_or_404(models.Glassware, pk=glass_id)

    if request.method == "POST":
        form = forms.MeasureForm(request.POST)
        if form.is_valid():
            measure = form.save(commit=False)
            measure.experiment = exp
            measure.glassware = glassware
            measure.save()
            return redirect("collectDatas.views.manage_measures", exp_id=exp_id)
    else:
        form = forms.MeasureForm()
    context = {"form": form, "exp": exp, "glassware": glassware}
    return render(request, "collectDatas/new_measure.html", context)


def delete_measure(request, measure_id):
    measure = get_object_or_404(models.Measure, pk=measure_id)
    exp_id = measure.experiment.id
    measure.delete()
    return redirect("collectDatas.views.manage_measures", exp_id=exp_id)
