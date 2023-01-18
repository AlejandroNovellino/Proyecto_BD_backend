from flask import jsonify, url_for
# jasper reports imports
import os
from platform import python_version
from pyreportjasper import PyReportJasper

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://ucarecdn.com/3a0e7d8b-25f3-4e2f-add2-016064b04075/rigobaby.jpg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your proyect by following the <a href="https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/_QUICK_START.md" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"

# Reports ---------------------------------------------------------------------------------------------------------------------------
def generateReport(file_name, db_table, clave=None, carrera=None):

    JDBC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jarDriver')
    REPORTS_INPUT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reportsSchema')
    REPORTS_OUTPUT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/reports')

    input_file = os.path.join(REPORTS_INPUT_DIR, file_name+'.jrxml')
    output_file = os.path.join(REPORTS_OUTPUT_DIR, file_name)

    conn = {
        'driver': 'postgres',
        'username': 'postgres',
        'password': '1224',
        'host': 'localhost',
        'database': 'BD_app',
        'schema': db_table,
        'port': '5432',
        'jdbc_driver' : 'org.postgresql.Driver',
        'jdbc_dir': JDBC_DIR
    }
    pyreportjasper = PyReportJasper()
    pyreportjasper.config(
        input_file,
        output_file,
        db_connection=conn,
        output_formats=["pdf"],
        parameters={
            'python_version': python_version(),
            'clave': clave,
            'carrera': carrera
            },
        locale='en_US'
    )
    pyreportjasper.process_report()

    return output_file
