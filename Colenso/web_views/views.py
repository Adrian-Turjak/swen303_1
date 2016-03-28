from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.core.context_processors import csrf
from form import SearchForm
from Crypto.Cipher import XOR
import base64


import BaseXClient

from django.views.decorators.csrf import csrf_exempt

from lxml import etree


doc_id_key = "This is a rather awful secret."


def encrypt(plaintext):
    cipher = XOR.new(doc_id_key)
    return base64.b64encode(cipher.encrypt(plaintext))


def decrypt(ciphertext):
    cipher = XOR.new(doc_id_key)
    return cipher.decrypt(base64.b64decode(ciphertext))


@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        print "here"
        if form.is_valid():
            session = BaseXClient.Session("localhost", 1984, "admin", "admin")
            print form.data['xquery']

            if form.data['xquery'] == "test_case_1":
                print encrypt("Colenso/McLean/private_letters/PrLMcL-0024.xml")
                print encrypt("Cole")
                results = [
                    {
                        'element': '<name type="person" key="http://wtap.vuw.ac.nz/eats/entity/70546/">McLean</name>"',
                        'doc': encrypt("Colenso/McLean/private_letters/PrLMcL-0024.xml"),
                        'title': "1868 November 6: McLean to Colenso",
                        "author": "McLean"
                    }
                ]
                context = {
                    'results': results,
                    'clean': True,
                }
                template = loader.get_template("results.html")
                return HttpResponse(template.render(context))

            # first lets try doing a text search:
            try:
                if form.data['xquery'][0] == '"':
                    cleaned = []
                    cleaning = ''
                    term = False
                    op = ''
                    for char in form.data["xquery"]:
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
                        "ft:mark(db:open('Colenso')[. contains text '" + form.data['xquery'] + "'])"
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
                    'results': split_results,
                    'clean': False,
                    'split': True,
                }
                template = loader.get_template("results.html")
                return HttpResponse(template.render(context))
            except IOError:
                pass

            input = (
                "XQUERY declare namespace tei= 'http://www.tei-c.org/ns/1.0'; " +
                "db:open('Colenso') " +
                form.data['xquery'])
            try:
                results = session.execute(input)
                context = {
                    'results': results,
                }
            except IOError:
                print "ERROR!!!"
                context = {
                    'error': True,
                }
            
            template = loader.get_template("results.html")
            return HttpResponse(template.render(context))
    else:
        args = {}
        args['form'] = SearchForm()
        print args
        return render(request, "index.html", args)
    return render(request, "index.html")


def letter_detail(request, l_id):
    session = BaseXClient.Session("localhost", 1984, "admin", "admin")
    try:
        input = ("XQUERY doc('" + decrypt(l_id + "==") + "')")
        results = session.execute(input)

        parsed = etree.fromstring(results)

        context = {'results': etree.tostring(parsed, pretty_print = True)}
        template = loader.get_template("detail.html")
        return HttpResponse(template.render(context))
    except Exception:
        template = loader.get_template("404.html")
        return HttpResponse(template.render({}))
