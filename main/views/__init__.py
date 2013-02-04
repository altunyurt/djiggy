# ~*~ coding:utf-8 ~*~

""" wiki komutları wikiCamelCase şeklinde isimlendiriliyor 
    değişkenler ise değişken_adı
"""

from djtemps import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages 
from django.shortcuts import get_object_or_404

from main.models import Page
from main.forms import PageForm 
from utils.helpers import reverse_lazy, markdown_to_html

def index(request):
    return render_to_response("index.jinja", locals())


def wikiCreatePage(request, page_title):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page, created = Page.objects.get_or_create(title=page_title)
            if not created:
                messages.warning(request, _("""Seems that the page '%s' already exists, therefore you are redirected to
                                  that page""" % page_title))
                return HttpResponseRedirect(reverse_lazy("wikiShowPage", args=[page_title]))

            page.update(content=form.cleaned_data)
            messages.success(request, _("""Page '%s' created successfuly"""))
            return HttpResponseRedirect(reverse_lazy("wikiShowPage", args=[page_title]))

    else: 
        form = PageForm()
    return render_to_response("wiki/createOrEditPage.jinja", locals())
    

def wikiEditPage(request, page_title):
    page = get_object_or_404(Page, title=page_title)
    form = PageForm(instance=page)

    if request.method == "POST":
        """ do not allow any other changes """
        form = PageForm({"content": request.POST.get("content")}, instance=page)
        if form.is_valid():
            page = form.save()
            messages.success(request, _("""Page updated"""))
            return HttpResponseRedirect(reverse_lazy("wikiShowPage", args=[page_title]))

    return render_to_response("wiki/createOrEditPage.jinja", locals())


def wikiShowPage(request, page_title):
    page = get_object_or_404(Page, title=page_title)
    return render_to_response("wiki/showPage.jinja", locals())


def wikiShowSimilarPages(request, page_title):
    """ This is a fallback method, that is executed upon Http404 exceptions 
    that will list the pages named similarly to the page_title """

    pages = Page.objects.get_similar_pages(page_title)
    return render_to_response("wiki/showSimilarPages.jinja", locals())


def wikiPreviewPage(request):
    """ simple post/get view, returns the output of markdown parser """
    return HttpResponse(markdown_to_html(request.POST.get("content")))
    
