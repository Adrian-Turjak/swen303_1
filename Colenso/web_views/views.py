from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from form import (
    SearchForm, RefinedSearchForm, AddLetterForm, ReplaceLetterForm)
from Crypto.Cipher import XOR
import base64
from models import Search
import urllib

import BaseXClient

from django.views.decorators.csrf import csrf_exempt

from lxml import etree


salt = "This is a rather awful secret."


def encrypt(plaintext):
    cipher = XOR.new(salt)
    return base64.b64encode(cipher.encrypt(plaintext))[:-2]


def decrypt(ciphertext):
    cipher = XOR.new(salt)
    return cipher.decrypt(base64.b64decode(ciphertext + "=="))


def index(request):
    return render(request, "index.html")

def large_search(request):
    return render(request, "large_search.html")


@csrf_exempt
def search(request):
    print request.path
    refined_form = RefinedSearchForm(request.GET)
    form = SearchForm(request.GET)
    if refined_form.is_valid():
        print "I'M MORE REFINED THAN YOU BITCHES!!"
        context = {
                'results': "refined",
            }

        template = loader.get_template("results.html")
        return HttpResponse(template.render(context))

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
                    'element': (
                        '<name type="person" ' +
                        'key="http://wtap.vuw.ac.nz/eats/entity/70546/">' +
                        'McLean</name>'
                    ),
                    'doc': encrypt(
                        "Colenso/McLean/private_letters/PrLMcL-0021.xml"),
                    'title': "1868 August 6: McLean to Colenso",
                    "author": "McLean"
                },
                {
                    'element': (
                        '<name type="person" ' +
                        'key="http://wtap.vuw.ac.nz/eats/entity/70546/">' +
                        'McLean</name>'
                    ),
                    'doc': encrypt(
                        "Colenso/McLean/private_letters/PrLMcL-0023.xml"),
                    'title': "1868 October 16: McLean to Colenso",
                    "author": "McLean"
                },
                {
                    'element': (
                        '<name type="person" ' +
                        'key="http://wtap.vuw.ac.nz/eats/entity/70546/">' +
                        'McLean</name>'
                    ),
                    'doc': encrypt(
                        "Colenso/McLean/private_letters/PrLMcL-0024.xml"),
                    'title': "1868 November 6: McLean to Colenso",
                    "author": "McLean"
                }
            ]
            context = {
                'search': form.data["search"],
                'results': results,
                'clean': True,
            }
            search_obj.successful = True
            search_obj.save()
            template = loader.get_template("results.html")
            return HttpResponse(template.render(context))

        # first lets try doing a text search:
        try:
            if form.data['search'][0] == '"':
                print "Trying logical search"
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
                print "Trying raw text search"
                input = (
                    "XQUERY declare namespace tei= 'http://www.tei-c.org/ns/1.0'; " +
                    "ft:mark(db:open('Colenso')[. contains text '" + form.data['search'] + "'])"
                )
                results = session.execute(input)

            if results:
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
                search_obj.successful = True
                search_obj.save()
                template = loader.get_template("results.html")
                return HttpResponse(template.render(context))
        except IOError:
            print "ERROR!!!"
            pass

        # now since text search has failed, try an xquery search
        print "Trying xquery search"
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
            search_obj.successful = True
            search_obj.save()
        except IOError:
            print "ERROR!!!"
            context = {
                'results': False,
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

        context = {
            'results': etree.tostring(parsed, pretty_print=True),
            'id': l_id
        }
        template = loader.get_template("detail.html")
        return HttpResponse(template.render(context))
    except Exception:
        template = loader.get_template("404.html")
        return HttpResponse(template.render({}))


@csrf_exempt
def edit_letter(request, l_id):
    if request.method == 'POST':
        form = ReplaceLetterForm(request.POST)
        if not form.is_valid():
            print "here?"
            return render(request, "add_letter.html")

        session = BaseXClient.Session("localhost", 1984, "admin", "admin")
        try:
            session.execute("open Colenso")
            cleaned = str(' '.join(form.data['xml'].split()))
            print decrypt(l_id + "==")
            session.replace(decrypt(l_id + "=="), cleaned)

            return redirect("/letters/" + l_id)
        except Exception:
            template = loader.get_template("404.html")
            return HttpResponse(template.render({}))
    else:
        print "here?"
        try:
            session = BaseXClient.Session("localhost", 1984, "admin", "admin")
            input = ("XQUERY doc('" + decrypt(l_id + "==") + "')")
            results = session.execute(input)

            parsed = etree.fromstring(results)

            context = {'results': etree.tostring(parsed, pretty_print=True)}
            template = loader.get_template("edit_letter.html")
            return HttpResponse(template.render(context))
        except Exception:
            template = loader.get_template("404.html")
            return HttpResponse(template.render({}))


@csrf_exempt
def add_letter(request):
    if request.method == 'POST':
        form = AddLetterForm(request.POST)
        if not form.is_valid():
            print "here?"
            return render(request, "add_letter.html")

        session = BaseXClient.Session("localhost", 1984, "admin", "admin")
        try:
            session.execute("open Colenso")
            cleaned = str(' '.join(form.data['xml'].split()))
            session.add(form.data['doc_uri'], form.data['xml'])

            parsed = etree.fromstring(cleaned)

            context = {'results': etree.tostring(parsed, pretty_print=True)}
            template = loader.get_template("detail.html")
            return HttpResponse(template.render(context))
        except Exception:
            raise
            template = loader.get_template("404.html")
            return HttpResponse(template.render({}))
    else:
        return render(request, "add_letter.html")


def search_history(request):
    history = Search.objects.order_by("-date")
    for search in history:
        search.url = "/search/?search=" + urllib.quote_plus(search.search)
    context = {'history': history}
    template = loader.get_template("history.html")
    return HttpResponse(template.render(context))


def my_search_history(request,):
    history = Search.objects.order_by(
        "-date"
    ).filter(ip_address__exact=request.META['REMOTE_ADDR'])
    for search in history:
        search.url = "/search/?search=" + urllib.quote_plus(search.search)
    context = {'history': history}
    template = loader.get_template("history.html")
    return HttpResponse(template.render(context))
