import json

from chameleon import PageTemplate
import six


BIGTABLE_ZPT = (
    """\
<table xmlns="http://www.w3.org/1999/xhtml"
xmlns:tal="http://xml.zope.org/namespaces/tal">
<tr tal:repeat="row python: options['table']">
<td tal:repeat="c python: row.values()">
<span tal:define="d python: c + 1"
tal:attributes="class python: 'column-' + %s(d)"
tal:content="python: d" />
</td>
</tr>
</table>"""
    % six.text_type.__name__
)


def function_handler(function_input):
    #payload = json.loads(function_input["payload"].decode("utf-8"))
    payload = json.loads(bytes(function_input["payload"]).decode("utf-8"))
    num_of_rows = int(payload["nrow"])  # 10
    num_of_cols = int(payload["ncol"])  # 15

    data = {}
    for i in range(num_of_cols):
        data[str(i)] = i

    table = [data for _ in range(num_of_rows)]
    options = {"table": table}

    tmpl = PageTemplate(BIGTABLE_ZPT)
    data = tmpl.render(options=options)

    return {"len(result)": len(data)}
