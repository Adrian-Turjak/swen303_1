from django import forms
# from lxml import etree


class SearchForm(forms.Form):
    search = forms.CharField(required=True)


class RefinedSearchForm(forms.Form):
    search = forms.CharField(required=True)
    refined_search = forms.CharField(required=True)


class AddLetterForm(forms.Form):
    doc_uri = forms.CharField(required=True)
    xml = forms.CharField(required=True)


class ReplaceLetterForm(forms.Form):
    xml = forms.CharField(required=True)

    def clean_xml(self):
        data = self.cleaned_data['xml']
        # NOTE! This is where schema validation would go if I was able to find the
        # blasted schema file somewhere. You'd think it would be on the TEI github,
        # but it wasn't named in any sensible way...

        # schema_root = etree.XML(
        #     '''
        #     <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        #         <xsd:element name="a" type="xsd:integer"/>
        #     </xsd:schema>
        #     '''
        # )
        # schema = etree.XMLSchema(schema_root)

        # parser = etree.XMLParser(schema = schema)
        # root = etree.fromstring(data, parser)
        # if "fred@example.com" not in data:
        #     raise forms.ValidationError("You have forgotten about Fred!")

        # # Always return the cleaned data, whether you have changed it or
        # # not.
        return data
