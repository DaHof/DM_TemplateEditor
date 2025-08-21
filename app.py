import os
from flask import Flask, request, jsonify, render_template
from jinja2 import Template
import requests

app = Flask(__name__)

# store user-defined Jinja templates separately from Flask's template folder
USER_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'template_store')
os.makedirs(USER_TEMPLATE_DIR, exist_ok=True)


def save_template(template_id: str, content: str) -> str:
    """Save a template file to disk and return its path."""
    path = os.path.join(USER_TEMPLATE_DIR, f"{template_id}.j2")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def load_template(template_id: str) -> Template:
    """Load a template by id."""
    path = os.path.join(USER_TEMPLATE_DIR, f"{template_id}.j2")
    with open(path, encoding='utf-8') as f:
        return Template(f.read())


@app.route('/template', methods=['POST'])
def upload_template():
    """Upload a template with a template_id and content."""
    data = request.get_json(force=True)
    template_id = data['template_id']
    content = data['content']
    save_template(template_id, content)
    return jsonify({'status': 'saved'}), 201


@app.route('/editor')
def editor_page():
    """Simple web page to create templates."""
    return render_template('editor.html')


def _render(template: Template, record: dict) -> str:
    return template.render(record)


def send_to_external(content: str, external_url: str) -> None:
    """Send generated output to an external system via POST."""
    try:
        response = requests.post(external_url, json={'content': content}, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        app.logger.error('Failed to send to external system: %s', exc)


@app.route('/render', methods=['POST'])
def render_record():
    """Render a single record against a template."""
    data = request.get_json(force=True)
    template_id = data['template_id']
    record = data['record']
    external_url = data.get('external_url')

    template = load_template(template_id)
    rendered = _render(template, record)

    if external_url:
        send_to_external(rendered, external_url)

    return jsonify({'result': rendered})


@app.route('/batch', methods=['POST'])
def render_batch():
    """Render multiple records against a template."""
    data = request.get_json(force=True)
    template_id = data['template_id']
    records = data['records']
    external_url = data.get('external_url')

    template = load_template(template_id)
    results = []
    for record in records:
        rendered = _render(template, record)
        results.append(rendered)
        if external_url:
            send_to_external(rendered, external_url)

    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
