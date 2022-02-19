from django.urls import path

from backup import views




app_name="backup"

urlpatterns = [
    path('', views.backup_index_app, name='backup_index_app'),
    path('exportaton', views.backup_export_app, name='backup_export_app'),
    path('importaton', views.backup_import_app, name='backup_import_app'),
]