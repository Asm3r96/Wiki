from django.shortcuts import render
#module which renders a page
from markdown2 import Markdown
#importing "Markdown" from markdown2 which converts markdown to html
markdowner = Markdown ()
from . import util
# . is basically meaning from the same file directory import this module
import markdown
#converts markdown into html
import random
# this random module will help us randomly choose between the entries.

def index(request):
	return render(request,"encyclopedia/index.html",{
		"entries": util.list_entries()
		})
"""This is the home page and renders the index page and
	 gives the page the list of entries that are created by util.list_entries. 
	 """

def convert_to_HTML(title):
	entry = util.get_entry(title)
	html = markdown.markdown(entry) if entry else None
	return html
# convert Markdown to HTML using Markdown

def entry(request,title):
	#gets the page from util
	entryPage = util.get_entry(title)
	#checks if entrypage exists or not
	if entryPage is None:
		#if we don't find the page will show the user the nonExistingEntry Page and give him the option to add the page. 
		return render(request, "encyclopedia/nonExistingEntry.html",{
			"entryTitle": title 
			})
	#if the page does exist, we will then render the page and convert the entry into html.
	else: 
		return render(request, "encyclopedia/entry.html", {
			"entry": convert_to_HTML(title),
			"entryTitle": title
			}) 

def search(request):
	# to find and go to a page using the searchbar

	if request.method == 'GET':
		#here we check if the for is in the form of get. The difference between GET and POST is that in GET you are trying to read information and that's it, 
		#while in POST you try and change the state of the system. GET is good for search forms, while POST is sometimes good for passwords when coupled with the csrf token.
		input = request.GET.get('q')
		#we get the input and then we get the input by the name of the input.
		html = convert_to_HTML(input)
		#The entries are called from util and are later used to check if the entry exists or not
		entries = util.list_entries()
		#We define the list outside so that the list doesn't empty itself after each iteration. Forgot that initially
		search_pages = []

		for entry in entries:
			if input.upper() in entry.upper():
			#css.upper=CSS, CSS
			#Here if the entry is somewhat similar or is included in the the word of the entry, e.g. cs is included in css:
			#then we put the pages into this array and render a search page that contains this array.
				#By doing this the user knows what pages were similar.
				search_pages.append(entry)

		for entry in entries:
			#Here we check if the entry is already in entries by going through all of the entries in entries
			if input.upper() == entry.upper():
				#we make sure the function works for different kinds of capitalization
				return render(request, "encyclopedia/entry.html",{
					#we then render the page called encyclopedia/entry.html if the entry exists and give the page the variables such as the page in html form and the title.
					"entry": html,
					"entryTitle": input
				})
			elif search_pages != []:
				
				return render(request, "encyclopedia/search.html",{
					"entries": search_pages
					})
			else:
				return render(request, "encyclopedia/nonExistingEntry.html",{
					"entryTitle": input
					})

		

def newPage(request):
	return render(request, "encyclopedia/newPage.html")

def save(request):
	if request.method == 'POST':
		input_title = request.POST['title']
		input_text = request.POST['text']
		entries = util.list_entries()
		html = convert_to_HTML(input_title)
		Already_exist_true = "false"
		for entry in entries:
			if input_title.upper() == entry.upper():
				Already_exist_true = "true"
				
		if Already_exist_true == "true":
			return render(request, "encyclopedia/already_exist.html",{
				"entry":html,
				"entryTitle":input_title
				})

		else:
			util.save_entry(input_title, input_text)
		
			return render(request, "encyclopedia/entry.html", {
				"entry": convert_to_HTML(input_title),
				"entryTitle": input_title
			})


def randomPage(request):
	#This function generates a random page
	entries = util.list_entries()
	#Gets a list of entries
	randEntry = random.choice(entries)
	#We get a random entry from the random.choice function that chooses from an array
	html = convert_to_HTML(randEntry)
	#find the html and we render the page.
	return render(request, "encyclopedia/entry.html",{
		"entry": html,
		"entryTitle":randEntry
		})

def editPage(request): 
	if request.method == 'POST':
		input_title = request.POST['title']
		text = util.get_entry(input_title)
		
		return render(request, "encyclopedia/editPage.html",{
			"entry": text,
			"entryTitle": input_title
		})

def saveEdit(request):
	if request.method == 'POST':
		entryTitle = request.POST['title']
		entry = request.POST['text']
		util.save_entry(entryTitle, entry)
		html = convert_to_HTML(entryTitle)
		return render (request, "encyclopedia/entry.html",{
			"entry": html,
			"entryTitle": entryTitle
			})
