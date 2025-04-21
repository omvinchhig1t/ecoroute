from flask import Blueprint, request, jsonify, render_template, json
from services.google_maps import get_directions
import pprint
# Create Blueprint
api_routes = Blueprint("api_routes", __name__)

@api_routes.route("/get_directions", methods=["GET"])
def handle_get_directions():
    try:
        source = request.args.get("source")
        destination = request.args.get("destination")

        if not source or not destination:
            return jsonify({"error": "Missing source or destination"}), 400

        directions = get_directions(source, destination)
        return jsonify({"route": directions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_routes.route("/show_map")
def show_map():
    try:
        source = request.args.get("source")
        destination = request.args.get("destination")
        # source = "Mumbai"
        # destination = "Pune"
        if not source or not destination:
                return jsonify({"error": "Missing source or destination"}), 400
        route_data = get_directions(source, destination)
        # Pretty print in terminal
        return render_template("map.html", route_data=json.dumps(route_data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
