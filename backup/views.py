from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import datetime


from evangelisation.models import Participant, Evangelisation, Site, Person, Suivi, Profile



def backup_index_app(request):
	context = dict()
	context['backup'] = True
	context['select_link'] = 'backup'
	return render(request, 'pages/backups/index.html', context)

#=====================================================================
#======================EXPORT DATA
def backup_export_app(request):
	pass



def backup_import_app(request):
    pass








