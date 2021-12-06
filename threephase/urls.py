from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_participant/<str:participant_name>', views.add_participant, name='add_participant'),
    path('add_value/<str:key>/<str:value>/<str:prepared_value>', views.add_value, name='add_value'),
    path('delete_value', views.delete_value, name='delte_value'), 
    path('update_name', views.update_name, name='update_name'),
    path('prepare/<str:key>', views.prepare, name='prepare'),
    path('prepared/<str:name>', views.prepared, name='prepared'),
    path('Agree/<str:name>', views.Agree, name='Agree'),
    path('Disagree/<str:name>', views.Disagree, name='Disagree'),
    path('pre_commit', views.pre_commit, name='pre_commit'),
    path('pre_committed/<str:name>', views.pre_committed, name='pre_committed'),
    path('commit', views.commit, name='commit'),
]
