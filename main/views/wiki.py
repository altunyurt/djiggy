# ~*~ coding:utf-8 ~*~

""" 
    Main wiki functions are defined here. 

    naming convention: 
        function+class names are in camelCase format
        variable names, class+instance methods are in under_scores
"""

from djtemps import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages 
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from main.models import Page, Revision, ActionLog
from main.forms import PageRevisionForm, RevertRevisionForm
from main.messages import action_messages
from utils.helpers import reverse_lazy, markdown_to_html, show_diff
from utils.decorators import requires_login


__all__ = ["create_page", "edit_page", "view_page", "show_similar_pages",
          "preview_page", "list_revisions", "revert_page_to_revision", "show_diffs", 
           "search", "recent_changes"]

@requires_login("login", _("Login required to be able to edit pages"))
def create_page(request, page_title):
    if request.method == "POST":
        form = PageRevisionForm(request.POST)
        if form.is_valid():
            page, created = Page.objects.get_or_create(title=page_title)
            form.save(page)
            messages.success(request, action_messages.get("page_created"))
            return HttpResponseRedirect(reverse_lazy("view_page", args=[page_title]))

    else: 
        form = PageRevisionForm()
    return render_to_response("wiki/create_or_edit_page.jinja", locals())
    

@requires_login("login", _("Login required to be able to edit pages"))
def edit_page(request, page_title):
    page = get_object_or_404(Page, title=page_title)
    current_revision = page.current
    form = PageRevisionForm(initial=current_revision.to_dict())

    if request.method == "POST":
        """ do not allow any other changes """
        form = PageRevisionForm(request.POST,
                        initial=current_revision.to_dict())
        
        if form.is_valid():
            form.save(page)
            messages.success(request, action_messages.get("page_updated"))
            return HttpResponseRedirect(reverse_lazy("view_page", args=[page_title]))

    return render_to_response("wiki/create_or_edit_page.jinja", locals())


def view_page(request, page_title):
    page = get_object_or_404(Page, title=page_title)
    return render_to_response("wiki/view_page.jinja", locals())


def show_similar_pages(request, page_title):
    """ This is a fallback method, that is executed upon Http404 exceptions 
    that will list the pages named similarly to the page_title """

    pages = Page.objects.get_similar_pages(page_title)
    return render_to_response("wiki/show_similar_pages.jinja", locals())


def preview_page(request):
    """ simple post/get view, returns the output of markdown parser """
    return HttpResponse(markdown_to_html(request.POST.get("content")))
    

def list_revisions(request, page_title):
    """ list revisions of given page """
    page = get_object_or_404(Page.objects.select_related("revision", "revision__user"), 
                             title=page_title)
    revisions = page.revisions.values("user__first_name", 
                                      "user__last_name", 
                                      "user__id",
                                     "datetime", "id")
    return render_to_response("wiki/list_revisions.jinja", locals())


@requires_login("login", _("Login required to be able to edit pages"))
def revert_page_to_revision(request, page_title, revision_id):
    page = get_object_or_404(Page, title=page_title)
    revision = get_object_or_404(Revision, page=page, id=revision_id)
    
    if request.method == "POST":
        form = RevertRevisionForm(request.POST)
        if form.is_valid():
            form.save(page, revision)
            messages.success(request, action_messages.get("page_reverted") % revision.datetime)
            return HttpResponseRedirect(reverse_lazy("view_page", args=[page_title]))
    else:
        form = RevertRevisionForm()
    return render_to_response("wiki/revert_page_to_revision.jinja", locals())


def show_diffs(request, page_title):
    """ show diffs of revisions of given page """
    rev1 = request.GET.get("revision_1")
    rev2 = request.GET.get("revision_2")
    if rev1 == rev2:
        messages.warning(request, _("Please chose two different revisions"))
    else:
        revision1 = get_object_or_404(Revision, page__title=page_title, id=rev1)
        revision2 = get_object_or_404(Revision, page__title=page_title, id=rev2)
        diff = show_diff(revision1.content_html, revision2.content_html)
    return render_to_response("wiki/show_diff.jinja", locals())


def search(request):
    query_string = request.GET.get("q", "")
    results = Page.objects.filter(Q(title__icontains=query_string) | Q(revision__content__icontains=query_string))
    return render_to_response("wiki/search.jinja", locals())


def recent_changes(request):
    actions = ActionLog.objects.all()
    return render_to_response("wiki/recent_changes.jinja", locals())
