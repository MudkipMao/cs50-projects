from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown

from . import util
from random import randrange


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
    num_range = len(all_articles)
    chosen_num = randrange(num_range)
    article_name = all_articles[chosen_num]
    article_markdown = util.get_entry(article_name)
    return render(request, "encyclopedia/article.html", {
        "article_name": article_name,
        "article_body": getHTMLfromMarkdown(article_markdown)
    })

