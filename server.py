from flask import Flask, render_template, request, redirect, url_for
from jinja2 import Template
from main import by_link, by_name


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def process_data():
    # Backend processing logic here
    # You can access data from the frontend using request.form or request.json
    query = request.form.get('query')
    if query[0:8] == "https://":
        song_id, song_title = by_link(query)
    else:
        song_id, song_title = by_name(query)

    # Load the template from a file
    with open('templates/result.html', 'r') as template_file:
        template_content = template_file.read()

    # Create a Jinja2 Template object
    template = Template(template_content)

    # Define your Python variables
    track_id = song_id
    track_title = song_title
    song_id_name = zip(track_id, track_title)

    # Render the template with variables
    rendered_html = template.render(song_id_name=song_id_name)
    return rendered_html




if __name__ == '__main__':
    app.run(debug=True)
