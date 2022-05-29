import subprocess
import threading

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, request, jsonify, abort, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from webargs.flaskparser import parser
from flask_restful_swagger_2 import Api
from flask_apispec.extension import FlaskApiSpec
from flask import g
import uuid


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='VEND-TASK',
            version='v1',
            openapi_version="2.0.2",
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
    })


    # """ config db """
    from app.config.models.config_model import Config

    @app.before_first_request
    def first_request():
        if Config.exists():
            return
        try:
            Config.create_table(wait=True)
        except Exception as e:
            print(str(e))
        abort(400,'server database failed to initialize')

    @app.after_request
    def after_request(response):
        return response

    @app.teardown_request
    def shutdown_session(exception=None):
        return 500

    """Configure RESTful views routing"""
    api = Api(app)

    docs = FlaskApiSpec(app)

    from app.product.views.product_view import ProductView
    from app.order.views.order_view import OrderView
    from app.ultilities.auth.views.auth import Auth

    api.add_resource(ProductView, '/<string:tenant_id>/api/1.0/products')
    api.add_resource(OrderView, '/<string:tenant_id>/api/1.0/sales')
    api.add_resource(Auth, '/login/<string:tenant_id>/oauth2/token')

    docs.register(ProductView)
    docs.register(OrderView)

    """Configure base routes."""

    @app.route('/', methods=['GET'])
    def home():
        args = request.args
        out = {
            'home': "Base Flask App: OpenAPI Specification Enter here"
        }
        if args:
            out = {**out, **args}
        return out, 200, {'Content-Type': 'text/plain'}

    @parser.error_handler
    def handle_request_parsing_error(error, req, schema, status_code, headers):
        abort(status_code, str(error.messages))

    @app.errorhandler(400)
    def bad_request(error):
        error = vars(error)

        message = "The browser (or proxy) sent a request that this server could not understand."

        if error.get("description"):
            if error.get("description").get('message'):
                message = error["description"]["message"]

        out = {'code': 400, 'message': message}

        response = make_response(jsonify(out), 400)
        return response

    @app.errorhandler(401)
    def unauthorized(error):
        error = vars(error)

        message = "The server could not verify that you are authorized to" \
                  " access the URL requested. You either supplied the wrong" \
                  " credentials (e.g. a bad password), or your browser " \
                  "doesn't understand how to supply the credentials required."

        if error.get("description"):
            if error.get("description").get('message'):
                message = error["description"]["message"]

        out = {'code': 401, 'message': message}

        response = make_response(jsonify(out), 401)
        return response

    @app.errorhandler(403)
    def forbidden(error):
        error = vars(error)

        message = "You don't have the permission to access the requested " \
                  "resource. It is either read-protected or not readable by " \
                  "the server."

        if error.get("description"):
            if error.get("description").get('message'):
                message = error["description"]["message"]

        out = {'code': 403, 'message': message}

        response = make_response(jsonify(out), 403)
        return response

    @app.errorhandler(404)
    def not_found(error):
        error = vars(error)

        message = "The requested URL was not found on the server. If you" \
                  " entered the URL manually please check your spelling and" \
                  " try again."

        if error.get("description"):
            if error.get("description").get('message'):
                message = error["description"]["message"]

        out = {'code': 404, 'message': message}

        response = make_response(jsonify(out), 404)
        return response

    @app.errorhandler(405)
    def method_not_allowed(error):
        error = vars(error)

        message = "The method is not allowed for the requested URL."

        if error.get("description"):
            if error.get("description").get('message'):
                message = error["description"]["message"]

        out = {'code': 405, 'message': message}

        response = make_response(jsonify(out), 405)
        return response

    @app.errorhandler(500)
    def internal_server(error):
        error = vars(error)

        message = "The server encountered an internal error and was unable" \
                  " to complete your request. Either the server is" \
                  " overloaded or there is an error in the application."

        if error.get("description"):
            if error.get("description").get('message'):
                message = error["description"]["message"]

        out = {'code': 500, 'message': message}

        response = make_response(jsonify(out), 500)
        return response

    @app.errorhandler(503)
    def service_unavailable(error):
        error = vars(error)

        message = "The server is temporarily unable to service your" \
                  " request due to maintenance downtime or capacity" \
                  " problems. Please try again later."

        if error.get("description"):
            if error.get("description").get('message'):
                message = error["description"]["message"]

        out = {'code': 503, 'message': message}

        response = make_response(jsonify(out), 503)
        return response

    @app.errorhandler(504)
    def gateway_timeout(error):
        error = vars(error)

        message = "The connection to an upstream server timed out."

        if error.get("description"):
            if error.get("description").get('message'):
                message = error["description"]["message"]

        out = {'code': 504, 'message': message}

        response = make_response(jsonify(out), 504)
        return response

    @app.before_request
    def before_request(*args, **kwargs):
        print('before request', g.__dict__)
        g.event_hash = str(uuid.uuid4())
        print('current request', g.__dict__)

    return app