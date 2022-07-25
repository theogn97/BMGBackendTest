import json

from flask import Flask, jsonify, request, abort
from flask_restx import Api, Resource, fields


flask_app = Flask(__name__)
app = Api(
    app=flask_app,
    version="1.0.0",
    title="BMG Backend Test",
    description="Submission for BMG Backend Service API Test by Theo Gunawan",
)

service_apis = app.namespace("services", description="Service APIs Submission")


def read_json_file():
    f = open("./static/shows_homeland.json", "r")
    show_data = json.loads(f.read())
    f.close()

    return show_data


body_model = app.model("RequestBody", {"summary": fields.String})


@service_apis.route("/<string:name>")
class GetEpisodeByName(Resource):
    def get(self, name):
        """Get specific episodes using partial episode name"""
        show_data = read_json_file()
        episodes = show_data["_embedded"]["episodes"]

        data = []

        for episode in episodes:
            if name.lower() in episode["name"].lower():
                data.append(episode)

        return jsonify({"status": 200, "message_status": "success", "data": data})


@service_apis.route("/<int:id>")
class UpdateEpisodeSummaryById(Resource):
    @service_apis.doc(body=body_model)
    def patch(self, id):
        """Update an episode's summary given an episode's ID"""
        show_data = read_json_file()
        episodes = show_data["_embedded"]["episodes"]
        request_data = request.get_json()
        summary = request_data.get("summary")

        updated_episodes = []

        output = {}

        for episode in episodes:
            if id == episode["id"]:
                episode["summary"] = "<p>" + str(summary) + "</p>"
                output = episode
            updated_episodes.append(episode)

        return jsonify({"status": 200, "message_status": "success", "data": output})


if __name__ == "__main__":
    app.run(debug=True)
