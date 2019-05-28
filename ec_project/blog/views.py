from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import QueryForm
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions
from .languages import ISO639_2

def landing(request):

    # if this is a POST request we need to process the form data
    form = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            dirty_text = form.cleaned_data['query_text']
            service = NaturalLanguageUnderstandingV1(
            version='2018-03-16',
            ## url is optional, and defaults to the URL below. Use the correct URL for your region.
            # url='https://gateway.watsonplatform.net/natural-language-understanding/api',
            username='7bbd9db3-0045-4031-b3ae-37e74060d817',
            password='HJk6qs544aYT')

            form= service.analyze(text=dirty_text,features=Features( keywords=KeywordsOptions(limit=3), concepts=ConceptsOptions(limit=3), entities=EntitiesOptions(limit=3))).get_result()
            lang = form["language"]
            expanded_lang = ISO639_2[lang]
            keywords = form["keywords"]
            words = {}
            count = 0
            for keyword in keywords:
                words[count] = keyword["text"]
                count = count+1
            concepts = form["concepts"]
            concept_links ={}
            for c in concepts:
                concept_links[c["text"]] = c["dbpedia_resource"]
            entities = form["entities"]
            entities_dict = {}
            count =0
            for e in entities:
                entities_dict[count] = e["text"]
                count = count+1
            final_form= {"language":expanded_lang, "keywords":words, "concepts":concept_links, "entities":entities_dict}
            print(form)
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
    else:
        form = QueryForm()
        final_form ={'form': form}
        # if a GET (or any other method) we'll create a blank form



    return render(request, 'blog/landing.html',final_form)

def notes(request):
    return render(request, 'blog/notes.html')

def homeworks(request):
    return render(request, 'blog/homeworks.html')

def learning(request):
    return render(request, 'blog/learning.html')
