MY IDEA (determine feasibility)

Develop a URL shortener application for parasmittal.com (my personal website).
If a URL is "caught" by the Nginx webserver serving static files, like /index.html, it should go the files.
Otherwise, it should be passed to this Python web application, which will resolve it.
There should be an admin panel, say at /urlshorteneradmin, where I (with a password), can edit shortened links.
This is just some tuples (short, long), where short is the short URL, and long is the URL it redirects to.

Non goals for the MVP:
- analytics
- complex auth (because this will be used by a single user which is me)

There is already a personal website called parasonepage at https://parasmittal.com. For this idea to be feasible, I do not want to interfere with it.
This will likely be deployed on the same virtual machine hosting parasonepage.

The database may be a SQLite file for simplicity.

For the sake of learning and curiosity, I do not want to use a production web framework like Flask, Django or FastAPI.
I believe this can be implemented with just WSGI or ASGI.

I use uv, rather than pip or similar Python tools.
