from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
import datetime
from datetime import date
from io import BytesIO
from django.template.loader import get_template, render_to_string
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings
from django.shortcuts import render, redirect
import random
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


from evangelisation.utils import (get_stat_evang_person_infos, month_name, month_evang, month_numer,
    get_personne_evang_all_by__year, get_personne_evang_all_by_jour_and_mois_and_year, get_personne_evang_all_by_mois_and_year,
    get_personne_evang_by_jour_and_mois_and_year, get_personne_evang_by_mois_and_year, get_personne_evang_by_year,
    get_personne_total, get_stat_oui_jesus_by_mois)
from evangelisation.models import Evangelisation, Person



import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



@login_required(login_url="user_login")
def generate_pdf(request, orientation, annee=None):
    context = dict()
    all_evang = None
    image_src = os.path.join(BASE_DIR, 'static//images_root')
    context['image_src'] = image_src

    if annee:
        all_evang = get_personne_evang_all_by__year(annee)
        context['annee'] = annee
    else:
        all_evang = get_personne_evang_all_by__year(date.today().year)
        context['annee'] = date.today().year

    if orientation == 'paysage':
        context['orientation'] = 'paysage'
    else:
        context['orientation'] = 'portrait'

    total = get_personne_total(all_evang)
    liste_oui_by_mois = get_stat_oui_jesus_by_mois(all_evang)
    for mois in liste_oui_by_mois:
        if mois['mois']=='Février':
            mois['mois'] = 'Fevrier'
        context[f"{mois['mois']}_oui"] = int(mois['oui_JESUS'])
    #===========+++END++++
    context['total'] = total
    context['all_evang'] = all_evang

    report_name = f"rapport-evangelisation{annee}-n°{random.randint(1, 1000)}"
    template_path = 'pages/pdf-report.html'

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={report_name}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('il y\'a certains erreurs <pre>' + html + '</pre>')
    return response


@login_required(login_url="user_login")
def rapport_app_index(request):
    stat = None
    all_evang = []
    total = {}
    context = dict()
    search = False
    liste_mois = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    if ('jour' and 'mois' and 'annee') in request.GET:
        jour = request.GET['jour']
        mois = request.GET['mois']
        annee = request.GET['annee']
        
        if jour == '----' and mois != '----' and annee != '----':
            context = get_stat_evang_person_infos(mois=month_numer(mois), year=annee)
            all_evang = get_personne_evang_all_by_mois_and_year(mois, annee)
            total = get_personne_total(all_evang)
            context['total'] = total
            context['search'] = True
            context['all_evang'] = all_evang
            context['annee'] = annee
        elif jour != '----' and mois != '----' and annee != '----':
            context = get_stat_evang_person_infos(jour=jour, mois=month_numer(mois), year=annee)
            all_evang = get_personne_evang_all_by_jour_and_mois_and_year(jour, mois, annee)
            total = get_personne_total(all_evang)
            context['total'] = total
            context['search'] = True
            context['jour'] = jour
            context['annee'] = annee
            context['all_evang'] = all_evang
        elif jour == '----' and mois == '----' and annee != '----':
            context = get_stat_evang_person_infos(year=annee)
            all_evang = get_personne_evang_all_by__year(annee)
            total = get_personne_total(all_evang)
            liste_oui_by_mois = get_stat_oui_jesus_by_mois(all_evang)
            for mois in liste_oui_by_mois:
                if mois['mois']=='Février':
                    mois['mois'] = 'Fevrier'
                context[f"{mois['mois']}_oui"] = int(mois['oui_JESUS'])
            context['total'] = total
            context['search'] = True
            context['annee'] = annee
            context['all_evang'] = all_evang
        elif jour == '----' and mois == '----' and annee == '----':
            try:
                context = get_stat_evang_person_infos(jour='----', mois='----', year='----')
                if context:
                    pass
                else:
                    context['error'] = True
            except ValueError:
                context['error'] = True
        elif jour != '----' and mois == '----' and annee == '----':
            try:
                context = get_stat_evang_person_infos(jour=jour, mois=mois, year=annee)
                if context:
                    pass
                else:
                    context['error'] = True
            except ValueError:
                context['error'] = True
        elif jour != '----' and mois != '----' and annee == '----':
            try:
                context = get_stat_evang_person_infos(jour=jour, mois=mois, year=annee)
                if context:
                    pass
                else:
                    context['error'] = True
                    context['jour'] = jour
            except ValueError:
                context['error'] = True
        elif jour == '----' and mois != '----' and annee == '----':
            try:
                context = get_stat_evang_person_infos(jour='----', mois=month_numer(mois), year='----')
                if context:
                    pass
                else:
                    context['error'] = True
            except ValueError:
                context['error'] = True
        elif jour != '----' and mois == '----' and annee != '----':
            try:
                context = get_stat_evang_person_infos(jour='----', mois=month_numer(mois), year='----')
                if context:
                    print(context)
                else:
                    context['error'] = True
            except ValueError:
                context['error'] = True
    else:
        context = get_stat_evang_person_infos(autre=date.today().year)
        if context:
            pass
        else: 
            context['not_stat'] = True
        all_evang = get_personne_evang_all_by__year(date.today().year)
        total = get_personne_total(all_evang)
        liste_oui_by_mois = get_stat_oui_jesus_by_mois(all_evang)
        for mois in liste_oui_by_mois:
                if mois['mois']=='Février':
                    mois['mois'] = 'Fevrier'
                context[f"{mois['mois']}_oui"] = int(mois['oui_JESUS'])
            #===========+++END++++
        context['total'] = total
        context['annee'] = date.today().year
        context['all'] = True
        context['all_evang'] = all_evang
    context['select_link'] = 'rapport'
    return render(request, 'pages/rapport/index.html', context)



@login_required(login_url="user_login")
def rapport_app_detail(request, pk, annee):
    data = dict()
    context = dict()
    modal_evang = list()
    nbre_dja = 0
    nbre_oui = 0
    nbre_non = 0
    nbre_ras = 0
    evangs_mois = Evangelisation.objects.filter(day__month=pk, day__year=annee)
    for evang in evangs_mois:
        nbre_oui = len(evang.personnes.filter(accepte_jesus='oui'))
        nbre_dja = len(evang.personnes.filter(accepte_jesus='déjà'))
        nbre_non = len(evang.personnes.filter(accepte_jesus='non'))
        nbre_ras = len(evang.personnes.filter(accepte_jesus='ras'))
        total = len(evang.personnes.all())
        modal_evang.append({
            'evang': evang,
            'nbre_oui': nbre_oui,
            'nbre_dja': nbre_dja,
            'nbre_non': nbre_non,
            'nbre_ras': nbre_ras,
            'total': total,
        })
    mois = month_name(pk)
    html_table = render_to_string('pages/rapport/modal-rapport-detail.html', {
        'mois': mois,
        'annee': annee,
        'modal_evang': modal_evang,
    })
    data['html_table'] = html_table

    return JsonResponse(data, safe=False)





















