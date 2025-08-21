# DM_TemplateEditor

A simple Flask service for generating creative assets based on Jinja2 templates.
Templates and records are provided via HTTP API calls. The rendered output can
be batched and optionally sent to an external system.

## Features
- Upload and store templates containing Jinja2 variables
- Render single records or batches of records against templates
- Optional webhook to forward rendered content to external systems
- Ready for deployment to Heroku using `gunicorn`

## Requirements
Python 3.10+

## Installation
```bash
pip install -r requirements.txt
```

## Running Locally
```bash
python app.py
```
The server listens on port `5000` by default.

### Template Editor
Open [http://localhost:5000/editor](http://localhost:5000/editor) in a browser to create or update templates using a simple web form. Templates are stored as `.j2` files under `template_store/`.

## API
### `POST /template`
Upload a template.
```json
{
  "template_id": "welcome",
  "content": "Hello {{ name }}!"
}
```

Templates saved through the editor use this same endpoint behind the scenes.

### `POST /render`
Render a single record.
```json
{
  "template_id": "welcome",
  "record": {"name": "Alice"},
  "external_url": "https://example.com/webhook" // optional
}
```

### `POST /batch`
Render multiple records.
```json
{
  "template_id": "welcome",
  "records": [{"name": "Alice"}, {"name": "Bob"}],
  "external_url": "https://example.com/webhook" // optional
}
```

Each rendered result is also POSTed to `external_url` when provided.

## Deploying to Heroku
Create an app and push this repository. Heroku uses `Procfile` to start the
application with `gunicorn`.

```bash
heroku create my-app
heroku git:remote -a my-app
heroku buildpacks:set heroku/python
git push heroku main
```
