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

### Configuration
Set the following environment variables to configure access to the editor:
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` – credentials for the login form (defaults `admin` / `admin`).
- `SECRET_KEY` – Flask secret key used for sessions.

### Template Editor
Start the server and visit [http://localhost:5000/login](http://localhost:5000/login) to sign in with the credentials defined in `ADMIN_USERNAME`/`ADMIN_PASSWORD` (defaults `admin`/`admin`).
After logging in, open [http://localhost:5000/editor](http://localhost:5000/editor) to create or update templates. Templates are stored as `.j2` files under `template_store/` with optional metadata files containing campaign and Canva design IDs.

The editor includes a Canva design button. Replace `YOUR_CANVA_APP_ID` in `templates/editor.html` with your Canva app ID to enable design creation. The resulting `designId` is saved alongside the template metadata.

The page also provides **Test Render** and **Test Batch** buttons. Enter sample record JSON and click a button to preview how the template renders for a single record or a small batch directly in the browser.

## API
### `POST /template`
Upload a template.
```json
{
  "template_id": "welcome",
  "content": "Hello {{ name }}!",
  "campaign_id": "spring_sale", // optional
  "design_id": "CANVA_DESIGN_ID" // optional

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
