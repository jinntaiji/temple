import os
import temple

"""

Main File

"""

# Global Variables go here.
global_vars = {
    'name': 'Jinn Taiji'
}

# Creates a new group
posts = temple.group.Group(global_vars, "posts_template")
for file in os.listdir("app/posts"):
    # Initialise a post
    post = temple.page.Post(global_vars, "template", file)
    # Write the HTML to a file
    site_page = open("app/static/{}.html".format(file[:-3]), 'w+').write(
        post.to_template())
    # Add the post to a group
    posts.add_page(post)

# Add the group to the global variables
global_vars['posts'] = posts.to_html()

# Initialise the index page
index = temple.page.Page(global_vars, "index_template")

# Write the HTML of the index page to a file
index_page = open("app/static/index.html", 'w+').write(
    index.to_template())
