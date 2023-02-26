from django.shortcuts import render

from . import util
import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convertmdtohtml(entrytitle):
    content = util.get_entry(entrytitle)
    Markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return Markdowner.convert(content)

def entry(request, title):
    entrytext=convertmdtohtml(title)
    if entrytext==None:
        return render(request,"encyclopedia/error.html", {"message":"This entry does not exist"})
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "entry":entrytext
        })
    
def search(request):
    if request.method == "POST":
        query=request.POST['q']
        querycontentinhtml=convertmdtohtml(query)
        if querycontentinhtml is not None:
            return render(request,"encyclopedia/entry.html",{"title":query,"entry":querycontentinhtml})
        else:
            allentries=util.list_entries()
            recommendations=[]
            for entry in allentries:
                if query.lower() in entry.lower():
                    recommendations+=[entry]
            return render(request,"encyclopedia/search.html",{"recommendations":recommendations})
        

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newentry.html")
    else:
        title=request.POST['title']
        content=request.POST['content']
        existetitle=util.get_entry(title)
        if existetitle is not None:
            return render(request, "encyclopedia/error.html",{"message":"this title already exists for an entry"})
        else:
            htmlcontent=convertmdtohtml(title)
            util.save_entry(title,content)
            return render(request, "encyclopedia/entry.html",{"title":title,"content":htmlcontent})