from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms

from . import util
from random import choice


class NewArticleForm(forms.Form):
    title = forms.CharField(label="Article Name")
    article_body = forms.CharField(widget=forms.Textarea, label="Article Body")


class EditArticleForm(forms.Form):
    article_name = forms.CharField(widget=forms.HiddenInput)
    article_body = forms.CharField(widget=forms.Textarea, label=False)


def getHTMLfromMarkdown(article_markdown):
    markdowner = Markdown()
    article_body = markdowner.convert(article_markdown)
    return article_body


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def article(request, article_name):
    article_markdown = util.get_entry(article_name)
    # Return error if article's markdown doesn't exist
    if article_markdown is None:
        return HttpResponse("Article cannot be found!")

    # Format the markdown file into proper HTML
    return render(request, "encyclopedia/article.html", {
        "article_name": article_name,
        "article_body": getHTMLfromMarkdown(article_markdown)
    })


def random(request):
    all_articles = util.list_entries()
    selected_page = choice(all_articles)
    return redirect('encyclopedia:article', article_name=selected_page)


def create(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            article_title = form.cleaned_data["title"]
            article_body = form.cleaned_data["article_body"]
            util.save_entry(article_title, article_body)
            return redirect('encyclopedia:article', article_name=article_title)
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": NewArticleForm()
    })


def search(request):
    query = request.GET.get('q').lower()
    all_articles = [x.lower() for x in util.list_entries()]
    if query in all_articles:
        return redirect('encyclopedia:article', article_name=query)

    matching_articles = [x for x in util.list_entries() if query in x.lower()]
    return render(request, "encyclopedia/search.html", {
        "results": matching_articles
    })


def edit(request):
    if request.method == "POST":
        form = EditArticleForm(request.POST)
        if form.is_valid():
            article_name = form.cleaned_data["article_name"]
            article_body = form.cleaned_data["article_body"]
            util.save_entry(article_name, article_body)
            return redirect('encyclopedia:article', article_name=article_name)
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    elif request.method == "GET":
        article_name = request.GET.get('an')
        article_body = util.get_entry(article_name)
        return render(request, "encyclopedia/edit.html", {
            "form": EditArticleForm({
                "article_name": article_name,
                "article_body": article_body
            }),
            "article_name": article_name,
            "article_body": article_body
        })
    else:
        redirect('encyclopedia:index')
