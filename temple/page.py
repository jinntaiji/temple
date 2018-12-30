import re

"""

Temple: Page
    Stores the page classes

"""

class Page:
    """
    Page class:
        A standard class used for pages. Stores the pages'
        information in the value dict and includes function
        for parsing template.
    """
    def __init__(self, values, template):
        self.values = {
            'template': open("app/templates/{}.html".format(template), 'r').read()
        }
        self.values.update(values)
        self.parsed = ""
        self.html = ""

    def to_template(self):
        self.html = self.values['template']
        self.values['params'] = re.findall('\|(.*?)\|', self.html)
        for param in self.values['params']:
            self.html = self.html.replace(
                "|{}|".format(param),
                self.values[param]
            )
        return self.html


class Post(Page):
    """
    Specific Post Class:
        A specific class used for posts. Includes a basic
        markdown parser and the ID (address) of each
        post. Each post should be stored in a custom group
        in order to be repeated.
    """
    def __init__(self, values, template, markdown):
        super().__init__(values, template)
        self.markdown = list(filter(None, open("app/posts/{}".format(markdown)).read().split("\n")))
        self.values.update({
            'id': markdown[:-3]
        })
        self.parse_markdown()

    def parse_markdown(self):
        self.values.update({
            'title': self.markdown[0].replace("#"*self.markdown[0].count("#"), "").strip(),
            'date': self.markdown[1].replace("#"*self.markdown[1].count("#"), "").strip(),
            'desc': self.markdown[2],
            'content': ""
        })
        for line in range(len(self.markdown)):
            if self.markdown[line][0] == "#":
                self.values['content'] += "<h{}>{}</h{}>".format(self.markdown[line].count("#"), self.markdown[line].replace("#"*self.markdown[line].count("#"), "").strip(), self.markdown[line].count("#"))
            elif self.markdown[line][0] == "!":
                self.values['content'] += "<img src=\"{}\" alt=\"{}\">".format(re.search('\((.*?)\)', self.markdown[line]).group(1), re.search('\[(.*?)\]', self.markdown[line]).group(1))
            elif self.markdown[line][0] == "-":
                if self.markdown[line-1][0] != "-":
                    self.values['content'] += "<ul>"
                self.values['content'] += "<li>{}</li>".format(self.markdown[line][1:].strip())
                if self.markdown[line+1][0] != "-":
                    self.values['content'] += "</ul>"
            else:
                if re.search("\[", self.markdown[line]):
                    for i in range(0, self.markdown[line].count("[")):
                        self.markdown[line] = self.markdown[line].replace(
                            "[" + re.search('\[(.*?)\)', self.markdown[line]).group(1) + ")",
                            "<a href=\"{}\">{}</a>".format(
                                re.search('\((.*?)\)', self.markdown[line]).group(1),
                                re.search('\[(.*?)\]', self.markdown[line]).group(1)
                            )
                        )
                if re.search("\*\*", self.markdown[line]):
                    for i in re.findall('\*\*(.*?)\*\*', self.markdown[line]): self.markdown[line] = self.markdown[line].replace("**{}**".format(i), "<strong>{}</strong>".format(i))
                elif re.search("\_\_", self.markdown[line]):
                    for i in re.findall("\_\_(.*?)\_\_", self.markdown[line]): self.markdown[line] = self.markdown[line].replace("__{}__".format(i), "<strong>{}</strong>".format(i))
                elif re.search("\*", self.markdown[line]):
                    for i in re.findall("\*(.*?)\*", self.markdown[line]): self.markdown[line] = self.markdown[line].replace("*{}*".format(i), "<em>{}</em>".format(i))
                elif re.search("\_", self.markdown[line]):
                    for i in re.findall("\_(.*?)\_", self.markdown[line]): self.markdown[line] = self.markdown[line].replace("_{}_".format(i), "<em>{}</em>".format(i))
                self.values['content'] += "<p>{}</p>".format(self.markdown[line])
