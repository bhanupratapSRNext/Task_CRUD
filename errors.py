from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": {"code": "bad_request", "message": str(e)}}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": {"code": "unauthorized", "message": str(e)}}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": {"code": "forbidden", "message": str(e)}}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": {"code": "not_found", "message": str(e)}}), 404

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({"error": {"code": "unprocessable", "message": str(e)}}), 422