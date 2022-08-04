from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util


def index(request):
    if request.method == "POST":  # search field is used
        q = request.POST.get('q').lower()  # get data from input field
        if util.get_entry(q) != None:  # if there is such page
            return render(request, "encyclopedia/viewer.html", {
                "name": q,
                "content": Markdown().convert(util.get_entry(q))
            })
        else:  # if no such page
            results = []
            for i in util.list_entries():
                if q in i.lower():
                    results.append(i)
            return render(request, "encyclopedia/search.html", {
            "entries": results,
            })
    else:  #GET
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def page(request, title):  # for url queries
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/Error.html", {
        "error": "No such page",
        "comment": "But you can create it"
        })
    return render(request, "encyclopedia/viewer.html", {
        "name": title,
        "content": Markdown().convert(util.get_entry(title))
    })

def new(request):
    if request.method == 'POST':  # fun fact - methods always should be in UPPERCASE
        title = request.POST.get("title")
        text = request.POST.get("newtext")
        for j in util.list_entries():  # check if file already exists
            if title.lower() == j.lower():  # check is case insensitive
                return render(request, "encyclopedia/Error.html", {
                "error": "This entry already exists",
                "comment": "But you can add to it"
                })
        f = open(f"entries/{title}.md", "w")  # if no such entry - create it
        f.write('#' + title + "\n" + text)
        f.close()
        return render(request, "encyclopedia/viewer.html", { # after submition - redirect to new entry's page 
            "name": title,
            "content": Markdown().convert(util.get_entry(title))
        })  
    else:
        return render(request, 'encyclopedia/new.html')

def edit(request):
    if request.method == "POST":
        if request.POST.get("edit-btn") == "edit":
            title = request.POST.get("title-to-edit")
            text = util.get_entry(title)
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "text": text,
            })
        title = request.POST.get("get-title")  # request can get only values from the FORM submitted, not from page (!)
        edited = request.POST.get("edittext")
        f = open(f"entries/{title}.md", "w")
        f.write(edited)
        f.close()
        return render(request, "encyclopedia/viewer.html", { # after submition - show new entry's page 
            "name": title,
            "content": Markdown().convert(util.get_entry(title))
        })
    """else:  # TODO: GET
        title = request.POST.get("get-title")
        text = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "text": text,
    })"""

def randomize(request):
    list = util.list_entries()
    page = random.choice(list)
    return render(request, "encyclopedia/viewer.html", {
        "name": page,
        "content": Markdown().convert(util.get_entry(page))
    })