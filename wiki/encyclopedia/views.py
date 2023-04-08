from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random

def convert(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "Home"
    })

def wiki(request, title):
    if convert(title) == None:
        return render(request, "encyclopedia/err.html",{
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/wiki.html",{
            "title": title,
            "content": convert(title)
        })

def search(request):
    if request.method == 'POST':
        search_en = request.POST['q']
        if convert(search_en) is not None:
            return wiki(request, search_en)
        elif convert(search_en.upper()) is not None:
            return wiki(request, search_en.upper())
        elif convert(search_en.capitalize()) is not None:
            return wiki(request, search_en.capitalize())
        else:
            svakientry = util.list_entries()
            rec = []
            for entry in svakientry:
                if search_en.lower() in entry.lower():
                    rec.append(entry)
            return render(request, "encyclopedia/search.html",{
            "rec": rec
        })

def rendoom(request):
    page_namesList = util.list_entries()
    page_name = random.choice(page_namesList)
    return wiki(request, page_name)

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else :
        title2 = request.POST['title']
        content = request.POST['M_content']
        if util.get_entry(title2) is not None or util.get_entry(title2.upper()) or util.get_entry(title2.capitalize()):
            return render(request, "encyclopedia/err.html", {
                "message": "Page already exists"
            })
        else: 
            util.save_entry(title2, content)
            return wiki(request, title2)

def edit(request):
    if request.method == 'POST':
        title = request.POST['en_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['M_content']
        util.save_entry(title, content)
        return wiki(request, title)