"""Script to run app."""


from app import app
print("FLASK_ENV:", app.config.get("ENV"))
print("DEBUG:", app.config.get("DEBUG"))