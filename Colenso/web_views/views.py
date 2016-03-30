from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from form import SearchForm, RefinedSearchForm
from Crypto.Cipher import XOR
import base64
from models import Search
import urllib

import BaseXClient

from django.views.decorators.csrf import csrf_exempt

from lxml import etree


doc_id_key = "This is a rather awful secret."


def encrypt(plaintext):
    cipher = XOR.new(doc_id_key)
    return base64.b64encode(cipher.encrypt(plaintext))[:-2]


def decrypt(ciphertext):
    cipher = XOR.new(doc_id_key)
    return cipher.decrypt(base64.b64decode(ciphertext + "=="))


@csrf_exempt
def index(request):
    args = {}
    args['form'] = SearchForm()
    return render(request, "index.html", args)


@csrf_exempt
def search(request):
    print request.path
    refined_form = RefinedSearchForm(request.GET)
    form = SearchForm(request.GET)
    if refined_form.is_valid():
        print "I'M MORE REFINED THAN YOU BITCHES!!"
        redirect("/")

    elif form.is_valid():
        session = BaseXClient.Session("localhost", 1984, "admin", "admin")
        print form.data['search']

        search_obj = Search.objects.create(
            ip_address=request.META['REMOTE_ADDR'],
            search=form.data['search']
        )
        search_obj.save()

        if form.data['search'] == "test_case_1":
            results = [
                {
                    'element': '<name type="person" key="http://wtap.vuw.ac.nz/eats/entity/70546/">McLean</name>"',
                    'doc': encrypt("Colenso/McLean/private_letters/PrLMcL-0024.xml"),
                    'title': "1868 November 6: McLean to Colenso",
                    "author": "McLean"
                }
            ]
            context = {
                'search': form.data["search"],
                'results': results,
                'clean': True,
            }
            search_obj.succuessful =  True
            search_obj.save()
            template = loader.get_template("results.html")
            return HttpResponse(template.render(context))

        # first lets try doing a text search:
        try:
            if form.data['search'][0] == '"':
                cleaned = []
                cleaning = ''
                term = False
                op = ''
                for char in form.data["search"]:
                    if char == '"':
                        if term:
                            term = False
                            cleaning = cleaning + char
                            cleaned.append(cleaning + " ")
                            cleaning = ''
                        else:
                            term = True
                            cleaning = cleaning + char
                            if op:
                                op = op.replace("and", "ftand")
                                op = op.replace("or", "ftor")
                                op = op.replace("not", "ftnot")
                                cleaned.append(op + " ")
                    elif term:
                        cleaning = cleaning + char
                    else:
                        op = op + char
                query = ''
                print query
                for value in cleaned:
                    query = query + value
                input = (
                    'XQUERY declare namespace tei= "http://www.tei-c.org/ns/1.0"; ' +
                    'ft:mark(db:open("Colenso")[. contains text ' + query + ' using wildcards])'
                )
                results = session.execute(input)
            else:
                input = (
                    "XQUERY declare namespace tei= 'http://www.tei-c.org/ns/1.0'; " +
                    "ft:mark(db:open('Colenso')[. contains text '" + form.data['search'] + "'])"
                )
                results = session.execute(input)

            split_results = []
            last = 0
            for i, char in enumerate(results):
                if char == "/":
                    if results[i+1:i+5] == "TEI>":
                        print results[i+1:i+5]
                        result = results[last:i+5]
                        parsed = etree.fromstring(result)
                        result = etree.tostring(
                            parsed, pretty_print=True
                        )
                        split_results.append(result)
                        last = i+5
            context = {
                'search': form.data["search"],
                'results': split_results,
                'clean': False,
                'split': True,
            }
            search_obj.succuessful =  True
            search_obj.save()
            template = loader.get_template("results.html")
            return HttpResponse(template.render(context))
        except IOError:
            pass

        # now since text search has failed, try an xquery search
        input = (
            "XQUERY declare namespace tei= 'http://www.tei-c.org/ns/1.0'; " +
            "db:open('Colenso') " +
            form.data['search'])
        try:
            results = session.execute(input)
            context = {
                'search': form.data["search"],
                'results': results,
            }
            search_obj.succuessful =  True
            search_obj.save()
        except IOError:
            print "ERROR!!!"
            context = {
                'error': True,
            }

        template = loader.get_template("results.html")
        return HttpResponse(template.render(context))
    else:
        return redirect("/")


def letter_detail(request, l_id):
    session = BaseXClient.Session("localhost", 1984, "admin", "admin")
    try:
        input = ("XQUERY doc('" + decrypt(l_id + "==") + "')")
        results = session.execute(input)

        parsed = etree.fromstring(results)

        context = {'results': etree.tostring(parsed, pretty_print=True)}
        template = loader.get_template("detail.html")
        return HttpResponse(template.render(context))
    except Exception:
        template = loader.get_template("404.html")
        return HttpResponse(template.render({}))


def search_history(request):
    history = Search.objects.order_by("date")
    for search in history:
        search.url = "/search/?search=" + urllib.quote_plus(search.search)
    context = {'history': history}
    template = loader.get_template("history.html")
    return HttpResponse(template.render(context))


def my_search_history(request,):
    history = Search.objects.order_by(
        "date"
    ).filter(ip_address__exact=request.META['REMOTE_ADDR'])
    for search in history:
        search.url = "/search/?search=" + urllib.quote_plus(search.search)
    context = {'history': history}
    template = loader.get_template("history.html")
    return HttpResponse(template.render(context))
