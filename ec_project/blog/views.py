from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import QueryForm
import json
import urllib.request
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, EmotionOptions
from .languages import ISO639_2
from urllib.request import urlopen
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image

def home(request):

    # if this is a POST request we need to process the form data
    form = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryForm(request.POST)

        # check whether it's valid:
        if form.is_valid():

            dirty_text = form.cleaned_data['query_text']
            query_format = form.cleaned_data['text_format']
            service = NaturalLanguageUnderstandingV1(
                version='2018-03-16',
                ## url is optional, and defaults to the URL below. Use the correct URL for your region.
                # url='https://gateway.watsonplatform.net/natural-language-understanding/api',
                username='7bbd9db3-0045-4031-b3ae-37e74060d817',
                password='HJk6qs544aYT')
            if query_format == "Plaintext":
                form = service.analyze(text=dirty_text, features=Features(keywords=KeywordsOptions(limit=3),
                                                                          concepts=ConceptsOptions(limit=3),
                                                                          entities=EntitiesOptions(
                                                                              limit=3), emotion=EmotionOptions())).get_result()
            else:
                form = service.analyze(url=dirty_text, features=Features(keywords=KeywordsOptions(limit=3),
                                                                         concepts=ConceptsOptions(limit=3),
                                                                         entities=EntitiesOptions(
                                                                             limit=3), emotion=EmotionOptions())).get_result()
                #with urlopen(dirty_text) as dirty_text:
                 #   dirty_text = dirty_text.decode("UTF-8").readlines()
            #print(type(dirty_text))
            #print(dirty_text)
            par = []
            first_sent = []
            str1 = ""
            char_counter = 0
            if query_format == "Plaintext":
                for c in dirty_text:
                    char_counter = char_counter+1

                    if c != '\n' and char_counter != len(dirty_text):
                        str1 = str1 + c
                    else:
                        par.append(str1)
                        str1 = ""
                for p in par:
                    str2 = ""
                    for c in p:
                        if c == '.' or c == '?' or c == '!':
                            first_sent.append(str2)
                            break
                        else:
                            str2 = str2 + c

            lang = form["language"]
            expanded_lang = ISO639_2[lang]
            keywords = form["keywords"]
            emotions = form["emotion"]["document"]["emotion"]
            for k,v in emotions.items():
                if emotions[k] >= 0.10:
                    emotions[k] = str(v*100)[0:2]+"%"
                else:
                    emotions[k] = str(v*100)[0:1]+"%"
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
            people = []
            places =[]
            org =[]
            for e in entities:
                if e["type"] == "Location":
                    places.append(e["text"])
                if e["type"] == "Person":
                    people.append(e["text"])
                if e["type"] == "Organization":
                    org.append(e["text"])
            subscription_key = "f85c6c69245e45cdac3a65408bf362ed"
            search_term = words[0]
            client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
            image_results = client.images.search(query=search_term)

            image_url = []
            if image_results.value:
                first_image_result = image_results.value[0]
                image_url.append(first_image_result.content_url)
            else:
                image_url.append("")

            height = []
            width = []
            image = Image.open(urllib.request.urlopen(image_url[0]))
            w, h = image.size
            height.append(400*h/w)

            final_form= {"language":expanded_lang,
                         "keywords":words,
                         "concepts":concept_links,
                         "first_sentences":first_sent,
                         "image_url":image_url,
                         "emotions":emotions,
                         "people": people,
                         "places": places,
                         "orgs": org,
                         "height": height}
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
    else:
        form = QueryForm()
        final_form ={'form': form}
        # if a GET (or any other method) we'll create a blank form



    return render(request, 'blog/results.html',final_form)


def contact(request):
    return render(request, 'blog/contact.html')

def about(request):
    return render(request, 'blog/about.html')
