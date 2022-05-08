from django.http.response import HttpResponse
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import re
from random import choice
import markdown2
import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert_to_HTML(title):

    entry = util.get_entry(title)
    html = markdown.markdown(entry) if entry else None
    return html

def entry(request, title):
    entryPage = util.get_entry(title)
    if entryPage is None:
        return render(request, "encyclopedia/nonExistingEntry.html",{
            "entryTitle": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": convert_to_HTML(title),
            "entryTitle": title
        } )





def editPage(request): 
	#This function is called after we press the edit button on the template and renders a page with a form.
	#In order to know what we are editing, we first find the title of the page where editing was requested.
	if request.method == 'POST':
		#Because we are changing the state of the system, we use POST.
		input_title = request.POST['title']
		#Get the information by using request.POST['title'] from the hidden input named title.
		text = util.get_entry(input_title)
		#We want to initiate the form with the latest text that under this page and we pass it into the page as a variable.
		#We don't turn this into html because the user uses markdown to change it.

		return render(request, "encyclopedia/editPage.html",{
			"entry": text,
			"entryTitle": input_title
		})



def search(request):
    
    # Saves search string from form
    q = request.GET['q']
    # Checks if there is an entry
    content = util.get_entry(q)

    # If an entry exists, return the page
    if content:
        return HttpResponseRedirect(reverse('wiki_entry', args=[q]))
    
    # If not, show possible pages
    else:
        entries = util.list_entries()
        possibilities = []
        string = re.compile("(?i)(" + q + ")")
        for entry in entries:
            if string.search(entry):
                possibilities.append(entry)
                
        # Shows possible pages (ie pages where that substring is present) or "no results found"
        return render(request, "encyclopedia/search.html", {
            "string": q,
            "possibilities": possibilities
        })