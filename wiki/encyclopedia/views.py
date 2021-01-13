from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms

from . import util
from random import choice


class SearchForm(forms.Form):
    search = forms.CharField(label="q")


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


def search(request):
    query = request.GET.get('q').lower()
    all_articles = [x.lower() for x in util.list_entries()]
    if query in all_articles:
        return redirect('encyclopedia:article', article_name=query)

    all_articles = [x for x in all_articles if query in x]
    return HttpResponse(f"matches are {all_articles}")
