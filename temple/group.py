import re

class Group:
    def __init__(self, values, template):
        self.values = {
            'template': open("app/templates/{}.html".format(template)).read()
        }
        self.values.update(values)
        self.vars = re.findall('\|(.*?)\|', self.values['template'])
        self.pages = []
        self.html = ""
        self.temp = ""

    def add_page(self, page):
        self.pages.append(page)

    def to_html(self):
        for page in self.pages:
            self.temp = self.values['template']
            for var in self.vars:
                self.temp = self.temp.replace(
                    "|{}|".format(var),
                    page.values[var]
                )
            self.html += self.temp
        return self.html
