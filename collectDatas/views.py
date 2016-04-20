# shortcuts
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from . import models
from . import forms

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import FigureCanvasPdf
from . import plot
# Create your views here.


def gather_measures(exp):
    """ gather all measures of one experiments and return a dict """
    glasswares = models.Glassware.objects.all()

    # collect datas from database
    data = dict()
    ndatamax = -1
    for g in glasswares:
        measures = models.Measure.objects.filter(experiment=exp, glassware=g)
        if len(measures) != 0:
            ndatamax = max(len(measures), ndatamax)
            data[g.get_glassware_display()] = [m.value for m in measures]

    return data, ndatamax


def home(request):
    exps = models.Experiment.objects.all().order_by("-date")
    return render(request, 'collectDatas/home.html', {"exps": exps})


def notes(request):
    return render(request, 'collectDatas/notes.html')


@login_required
def new_experiment(request):
    if request.method == "POST":
        form = forms.ExperimentForm(request.POST)
        if form.is_valid():
            exp = form.save()
            return redirect("collectDatas.views.home")
    else:
        form = forms.ExperimentForm()
    return render(request, "collectDatas/new_exp.html", {"form": form})


@login_required
def delete_experiment(request, exp_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    exp.delete()
    return redirect("collectDatas.views.home")


@login_required
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
    data, ndatamax = gather_measures(exp)

    # add needed values to have homogeneous lengths and compute statistic
    stats = dict()
    for glassware, measures in data.items():
        Q1, median, Q3 = np.percentile(measures, [25, 50, 75])
        stats[glassware] = {
            "count": len(measures),
            "ave": np.mean(measures),
            "std": np.std(measures),
            "min": np.min(measures),
            "max": np.max(measures),
            "Q1": Q1,
            "Q3": Q3,
            "median": median
        }
        measures += (ndatamax - len(measures)) * [0.]
        data[glassware] = measures

    # convert to html tab
    htmldata = pd.DataFrame(data).to_html(float_format="%6.2f", index=False, classes="table")
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

    # stat table
    items = ["count", "ave", "std", "min", "Q1", "median", "Q3", "max"]
    htmlstats = "<table class='table'>\n"
    htmlstats += "  <thead>\n"
    htmlstats += "    <tr>\n"
    htmlstats += "      <td></td>\n"
    for glassware in stats:
        htmlstats += "    <th>%s</th>\n" % glassware
    htmlstats += "    </tr>\n"
    htmlstats += "  </thead>\n"
    htmlstats += "  <tbody>\n"
    for item in items:
        htmlstats += "    <tr>\n"
        htmlstats += "      <th>%s</th>\n" % item
        for glassware in stats:
            htmlstats += "      <td>%6.2f</td>\n" % stats[glassware][item]
        htmlstats += "    </tr>\n"
    htmlstats += "  </tbody>\n"
    htmlstats += "</table>\n"

    context = {"exp": exp, "htmldata": htmldata, "htmlstats": htmlstats}
    return render(request, 'collectDatas/experiment.html', context)


def plot_experiment(request, exp_id, plottype="box"):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    data, ndatamax = gather_measures(exp)

    fig = plt.Figure()
    if plottype == "box":
        ax = fig.add_subplot(111)
        ax = plot.make_box_plot(ax, data)
    else:
        fig = plot.make_hist_plot(fig, data)

    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_figure(response)
    return response


def download_plot_experiment(request, exp_id, plottype="box"):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    data, ndatamax = gather_measures(exp)

    fig = plt.Figure()
    if plottype == "box":
        ax = fig.add_subplot(111)
        ax = plot.make_box_plot(ax, data)
    else:
        fig = plot.make_hist_plot(fig, data)

    filename = "%s.pdf" % exp.name.replace(" ", "_")

    canvas = FigureCanvasPdf(fig)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    canvas.print_figure(response)
    return response


def download_exp_data(request, exp_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    data, ndatamax = gather_measures(exp)

    # add needed values to have homogeneous lengths
    for glassware, measures in data.items():
        measures += (ndatamax - len(measures)) * [0.]
        data[glassware] = measures

    csvfile = pd.DataFrame(data).to_csv(index=False)

    response = HttpResponse(csvfile, content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % exp.name.replace(" ", "_")

    return response

#
# Views about measure
#


def manage_measures(request, exp_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    glasswares = models.Glassware.objects.all()

    # collect datas from database
    data = dict()
    for glassware in glasswares:
        measures = models.Measure.objects.filter(experiment=exp, glassware=glassware)
        if len(measures) != 0:
            data[glassware] = measures.order_by("-date")

    context = {"exp": exp, "data": data, "glasswares": glasswares}
    return render(request, 'collectDatas/manage_measures.html', context)


def new_measure(request, exp_id, glass_id):
    exp = get_object_or_404(models.Experiment, pk=exp_id)
    glassware = get_object_or_404(models.Glassware, pk=glass_id)

    MeasureFormSet = formset_factory(forms.MeasureForm, extra=5)

    if request.method == "POST":
        formset = MeasureFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if "value" in form.cleaned_data:
                    measure = form.save(commit=False)
                    measure.experiment = exp
                    measure.glassware = glassware
                    measure.save()
            return redirect("collectDatas.views.manage_measures", exp_id=exp_id)
    else:
        formset = MeasureFormSet()
    context = {"formset": formset, "exp": exp, "glassware": glassware}
    return render(request, "collectDatas/new_measure.html", context)


@login_required
def delete_measure(request, measure_id):
    measure = get_object_or_404(models.Measure, pk=measure_id)
    exp_id = measure.experiment.id
    measure.delete()
    return redirect("collectDatas.views.manage_measures", exp_id=exp_id)
