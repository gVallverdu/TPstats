from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # experiments :
    url(r'^experiment/(?P<exp_id>\d+)$', views.detail_experiment, name="detail_experiment"),
    url(r'^experiment/new/$', views.new_experiment, name="new_experiment"),
    url(r'^experiment/delete/(?P<exp_id>\d+)$', views.delete_experiment, name="delete_experiment"),
    url(r'^experiment/edit/(?P<exp_id>\d+)$', views.edit_experiment, name="edit_experiment"),
    url(r'^experiment/download/(?P<exp_id>\d+)$', views.download_exp_data, name="download_exp_data"),
    url(r'^experiment/plot/(?P<exp_id>\d+)/type(?P<plottype>.+)$',
        views.plot_experiment, name="plot_experiment"),
    url(r'^experiment/downloadplot/(?P<exp_id>\d+)/type(?P<plottype>.+)$',
        views.download_plot_experiment, name="download_plot_experiment"),
    # measures
    url(r'^measures/manage/(?P<exp_id>\d+)$', views.manage_measures, name="manage_measures"),
    url(r'^measure/new/exp(?P<exp_id>\d+)/glassware(?P<glass_id>\d+)$',
        views.new_measure, name="new_measure"),
    url(r'^measure/delete/(?P<measure_id>\d+)$', views.delete_measure, name="delete_measure"),
    # login
    url(r'^login/$', auth_views.login, name="login"),
    url(r'^logout/$', auth_views.logout, {"next_page": "home"}, name="logout"),
    # lecture notes
    url(r'^lecture_notes/$', views.notes, name='notes'),
]
