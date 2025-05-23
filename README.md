
# Django Polyglot App - Manage your .po files in the cloud
This project is still under development. We decided to opensource our project to get more contributors from the Django community.
It works together with the dj-polyglot library: https://github.com/Thutmose3/dj-polyglot-lib that contains some python management commands to help push your translations to this translation service.

You can use our hosted solution at https://dj-polyglot.com. Or host it yourself.

![DJ POlyglot UI](static/images/dj-polyglot-ui.png)


## Description
This is the UI for DJ-POlyglot. It is a Django application that allows the management translation strings. It has an API that will receive strings, and provides a nice UI to manage and translate them.

## Getting Started
``` bash
pip install -r _requirements/local.txt
python manage.py migrate
python manage.py runserver
```

# .env file example
```env
SECRET_KEY=CHANGE_ME
DJANGO_SETTINGS_MODULE=settings.settings.local
DEBUG=True
DEEPL_KEY=PUT_YOUT_API_KEY_HERE
```

## Tailwind CSS Setup
```bash
npm install flowbite
npx tailwindcss init tailwind.config.js
npx tailwindcss -i ./static/src/input_dj_polyglot_app.css -o ./static/src/output_dj_polyglot_app.css --watch
```