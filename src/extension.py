import flask
from flask_apispec.extension import FlaskApiSpec

class PatchedFlaskApiSpec(FlaskApiSpec):
    """Patches bug in FlaskApiSpec. 
    Fixes basePath property when generating routes when application is not hosted on /
    https://github.com/jmcarp/flask-apispec/pull/125
    """

    def fix_base_path(self):
        """Lazily set OpenAPI basePath for each request.
        This is to reflect the path root the application is running under.
        c.f. SCRIPT_NAME https://www.python.org/dev/peps/pep-0333/#environ-variables
        """
        if not flask.has_request_context():
            # not in request
            return
        if not flask.request.script_root:
            # not running under different root
            return
        self.spec.options['basePath'] = flask.request.script_root

    def swagger_json(self):
        self.fix_base_path()
        return flask.jsonify(self.spec.to_dict())