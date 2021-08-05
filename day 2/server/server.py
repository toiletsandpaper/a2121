import typing as t

from flask import Flask, request, jsonify, render_template
from server.response_scheme import Errors, ResponseScheme
from os import path


class StudentSimilarity(Flask):
    def __init__(self, import_name: str, static_url_path: t.Optional[str] = None,
                 static_folder: t.Optional[str] = "static", static_host: t.Optional[str] = None,
                 host_matching: bool = False, subdomain_matching: bool = False,
                 template_folder: t.Optional[str] = "templates", instance_path: t.Optional[str] = None,
                 instance_relative_config: bool = False, root_path: t.Optional[str] = None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching,
                         template_folder, instance_path, instance_relative_config, root_path)

        uploads_path = path.join(path.dirname(__file__), "../uploads")
        photos_path = path.join(uploads_path, "photos")
        videos_path = path.join(uploads_path, "videos")

        student_files = path.join(path.dirname(__file__), "../student_files")
        student_photos = path.join(student_files, "photos")
        student_videos = path.join(student_files, "videos")

        self.routes()

    @staticmethod
    def data_processing():
        data = request.args.to_dict() or request.json or request.data or request.form or {}

        return data

    def routes(self):
        @self.route("/", methods=["GET"])
        def index():
            return ResponseScheme.success({"text_message": "Hello, Archipelag 2021!"})

        @self.route("/student/upload_photo", methods=["GET", "POST"])
        def student_upload_photo():
            data = self.data_processing()

            # GET обработка, UI/UX -----------------------
            if request.method == "GET":
                return render_template("upload_photo.html", title="Upload_photo")

            # POST обработка -----------------------------
            if "student_id" not in data:
                return ResponseScheme.error(error_body={"params": ["student_id"]}, error=Errors.NOT_ENOUGH_PARAMS)

            if "photo" not in data:
                return ResponseScheme.error(error_body={"params": ["photo"]}, error=Errors.NOT_ENOUGH_PARAMS)

    def run(self, host: t.Optional[str] = None, port: t.Optional[int] = None, debug: t.Optional[bool] = None,
            load_dotenv: bool = True, **options: t.Any) -> None:

        super().run(host, port, debug, load_dotenv, threaded=True, **options)
