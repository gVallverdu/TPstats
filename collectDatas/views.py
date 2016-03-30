from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from . import models
from . import forms

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import FigureCanvasPdf
from . import plot
# Create your views here.

# shortcuts


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
    canvas.print_png(response)
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
    canvas.print_pdf(response)
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


def load_csv():
    csv = np.loadtxt("grid.csv", delimiter=",", skiprows=1, unpack=True)
    with open("grid.csv", "r") as f:
        heads = [h.strip() for h in f.readline().split(",")]

    datas = dict()
    for head, values in zip(heads, csv):
        datas[head] = values

    return datas


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
