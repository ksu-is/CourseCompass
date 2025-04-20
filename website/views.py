from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return "<h1 style='color: green;'>Hello from localhost!</h1>"
