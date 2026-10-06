# DJANGO CHECKLIST FOR BUILDING OUR APPLICATION

1. Create Virtual Environment
2. Install Django

3. Create the requirements.txt file to hold the packages and their versions

4. Start Django config project 

5. Start two django apps: accounts, blog

6. Create templates folder to organize your templates 
7. Create static folder to hold your static assets (css, js, images)
8. Register your apps in the config.settings.py
9. Add template directory in settings.py
TEMPLATES = {
	DIRS: [BASE_DIR / "templates"]
}

10. Setup static file/media (uploads) serving in development
within the urls.py in settings.py
if setting.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=setting.MEDIA_ROOT)