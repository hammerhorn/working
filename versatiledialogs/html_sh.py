#!/usr/bin/env python
#coding=utf8
"""html shell"""
import os
import subprocess

from web import form

from versatiledialogs.shell import Shellib
from versatiledialogs.terminal import Terminal

# make setters for attributes

DEFAULT_BROWSER = 'google-chrome'

class HtmlShell(Shellib):
    """
    analagous to the other shell options
    """
    def __init__(
            self, title='class <cjh.html_sh>', location='./untitled.html', bgcolor='',
            color=''):
        super(HtmlShell, self).__init__()
        self.title = title
        self.filename = location
        self.color_info = bgcolor, color
        self.content = ''
        self.template = """<!DOCTYPE html>
    <html lang="en">
      <head>
        <title>{}</title>
        <meta charset="UTF-8" http-equiv=REFRESH CONTENT="10; URL={}">
      </head>
      <body style="background-color:{}; color:{}">
        <h1>{}</h1>
        <hr>
        {}
      </body>
    </html>"""
        #if set('<>') & set(title):
        self.html_str = self.template.format(
            title, location, bgcolor, color, title.replace('<', '&lt;').replace('>', '&gt;'), self.content)
        self.write_html_file()

    def __str__(self):
        return self.html_str

    def write_html_file(self, new_html=None):
        """write html to the stored filename"""
        if new_html is not None:
            self.html_str = new_html
        fhandler = open(self.filename, 'w')
        fhandler.write(self.html_str)
        fhandler.close()


    def open_file_in_browser(self, web_browser=DEFAULT_BROWSER):
        """open the stored filename in the default browser"""
        if Terminal.os_name == 'nt':
            out_str = "now opening '{}{}' in your browser".format(
                os.getcwd(), self.filename)
            proc = subprocess.Popen('{} {}'.format(
                web_browser, self.filename), shell=True)
            proc.wait()
        else:
            out_str = "now opening '{}/{}' in your browser".format(
                os.getcwd(), self.filename)
            proc = subprocess.Popen('{} {}/{} > /dev/null&'.format(
                web_browser, os.getcwd(), self.filename), shell=True)
            proc.wait()
        Terminal.output(out_str)

    def output(self, output_str):
        self.content += output_str
        self.html_str = self.template.format(
            self.title, self.filename, self.color_info[0], self.color_info[1],
            self.title.replace('<', '&lt;').replace('>', '&gt;'), self.content)
        self.write_html_file()

    def outputf(self, output_str):
        self.output('<pre>{}</pre>'.format(output_str))

    def input(self, prompt):
        get_txt = form.Form(form.Textbox('input_form', description=prompt), form.Button('OK'))
        f = get_txt()
        snippet = f.render()
        self.content += snippet
        self.html_str = self.template.format(
            self.title, self.filename, self.color_info[0], self.color_info[1],
            self.title.replace('<', '&lt;').replace('>', '&gt;'), self.content)
        self.write_html_file()

    def message(self):
        pass

    def welcome(self):
        pass

#    <form>
#      <input type="text" name="some_data">
#      in.
#      <input type="submit" value="Submit">
#    </form>
#
#<!--    <p>Note that the form itself is not visible.</p>
#
#    <p>Also note that the default width of a text input field is 20 characters.
#     </p>
#    <form>
#      <input type="radio" name="gender" value="male" checked> Male<br>
#      <input type="radio" name="gender" value="female"> Female<br>
#      <input type="radio" name="gender" value="other"> Other
#    </form>
#    Try it Yourself »
#    <form action="action_page.php">
#      First name:<br>
#      <input type="text" name="firstname" value="Mickey"><br>
#      Last name:<br>
#      <input type="text" name="lastname" value="Mouse"><br><br>
#
#      </form> -->
#  </body>
#  </html>
