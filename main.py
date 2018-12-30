import os
import temple

global_vars = {
    'name': 'Hamzah Shahrin'
}

posts = temple.group.Group(global_vars, "posts_template")
for file in os.listdir("app/posts"):
    post = temple.page.Post(global_vars, "template", file)
    site_page = open("app/static/{}.html".format(file[:-3]), 'w+').write(
        post.to_template())
    posts.add_page(post)

global_vars['posts'] = posts.to_html()
index = temple.page.Page(global_vars, "index_template")
index_page = open("app/static/index.html", 'w+').write(
    index.to_template())
