from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_participant/<str:participant_name>', views.add_participant, name='add_participant'),
    path('add_value/<str:key>/<str:value>', views.add_value, name='add_value'),
    path('update_value', views.update_value, name='update_value'),
    path('prepare/<str:key>', views.prepare, name='prepare'),
    path('prepared/<str:name>', views.prepared, name='prepared'),
    path('commit', views.commit, name='commit'),
]
# update_value function could change the name of key and participant_name