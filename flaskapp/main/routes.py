from flask import Blueprint, render_template, request, make_response


main = Blueprint('main', __name__)


# We will not be using global app variable here in @app.route
# to creates routes anymore.
# Instead we are going to create route specifically for this user's blueprint.
# And then register these with the application later.


# To the function href="{{ url_for('users.login') }} we are passing the name of the function, not the route.

# This is decorator. Additional fuctionality to exisitng functions.
# app.route will handle all of the complicated backend stuff and simply allow us to write a function that returns information that will be shown on our website for this specific route.
@main.route('/')
@main.route('/home')
def home():
    response = make_response(render_template(
        'home.html.j2', title='Master Thesis Flask'))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    # return response
    return render_template('home.html', title='Master Thesis Flask')
