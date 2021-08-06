import json
import os
import typing as t
from random import choice

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from server.response_scheme import Errors, ResponseScheme
from os import path
from re import match
from uuid import uuid4 as uuid
from server.database_preload import *
from student_model.normalization import ImagePreparation
from student_model.model import StudentSiameseModel
from video_model.video import VideoProcessing


class StudentSimilarity(Flask):
    def __init__(self, import_name: str, secret_token: str, static_url_path: t.Optional[str] = None,
                 static_folder: t.Optional[str] = "static", static_host: t.Optional[str] = None,
                 host_matching: bool = False, subdomain_matching: bool = False,
                 template_folder: t.Optional[str] = "templates", instance_path: t.Optional[str] = None,
                 instance_relative_config: bool = False, root_path: t.Optional[str] = None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching,
                         template_folder, instance_path, instance_relative_config, root_path)

        self.secret_token = secret_token
        self.secret_key = "!TOP_SECRET_KEY"

        self.uploads_path = path.normpath(path.join(path.dirname(__file__), "../", "uploads/"))
        self.photos_path = path.join(self.uploads_path, "photos/")
        self.videos_path = path.join(self.uploads_path, "videos/")

        self.student_files = path.normpath(path.join(path.dirname(__file__), "../student_files/"))
        self.student_photos = path.join(self.student_files, "photos/")
        self.student_videos = path.join(self.student_files, "videos/")

        self.image_preparation = ImagePreparation(self.photos_path, self.student_photos)
        self.model = StudentSiameseModel()
        self.model.build_model()

        self.create_folders()
        self.routes()

    def create_folders(self):
        if not path.isdir(self.uploads_path):
            os.mkdir(self.uploads_path)

        if not path.isdir(self.photos_path):
            os.mkdir(self.photos_path)

        if not path.isdir(self.videos_path):
            os.mkdir(self.videos_path)

        if not path.isdir(self.student_files):
            os.mkdir(self.student_files)

        if not path.isdir(self.student_photos):
            os.mkdir(self.student_photos)

        if not path.isdir(self.student_videos):
            os.mkdir(self.student_videos)

    @staticmethod
    def data_processing():
        data = request.args.to_dict() or request.json or request.data or request.form or {}

        return data

    def routes(self):
        @self.route("/", methods=["GET"])
        def index():
            return ResponseScheme.success({"text_message": "Hello, Archipelag 2021!"})

        @self.route("/video/upload", methods=["GET", "POST"])
        def video_upload():
            data = self.data_processing()
            print(data)

            # GET обработка, UI/UX -----------------------
            if request.method == "GET":
                return render_template("upload_video.html", title="Upload_photo")

            # POST обработка -----------------------------
            if "access_token" not in data:
                return ResponseScheme.error(error=Errors.ACCESS_DENIED)

            if data["access_token"] != self.secret_token:
                return ResponseScheme.error(error=Errors.ACCESS_DENIED)

            if "email" not in data:
                return ResponseScheme.error(error=Errors.NOT_ENOUGH_PARAMS)

            if "video_link" not in data:
                return ResponseScheme.error(error=Errors.NOT_ENOUGH_PARAMS)

            video_thread = VideoProcessing(data["video_link"], data["email"], self.videos_path)
            video_thread.start()

            return ResponseScheme.success({
                "video_link": data["video_link"]
            })

        @self.route("/student/create_identity", methods=["GET", "POST"])
        def student_create_identity():
            data = self.data_processing()
            print(data)

            # GET обработка, UI/UX -----------------------
            if request.method == "GET":
                return render_template("create_student.html", title="Upload_photo")

            # POST обработка -----------------------------
            if "access_token" not in data:
                return ResponseScheme.error(error=Errors.ACCESS_DENIED)

            if data["access_token"] != self.secret_token:
                return ResponseScheme.error(error=Errors.ACCESS_DENIED)

            if "username" not in data:
                return ResponseScheme.error(error=Errors.NOT_ENOUGH_PARAMS)

            if "password" not in data:
                return ResponseScheme.error(error=Errors.NOT_ENOUGH_PARAMS)

            if not request.files:
                return ResponseScheme.error(error=Errors.ACCESS_DENIED)

            old_student = database.select_all("students", cls=Object, where=f"""`username` = '{data["username"]}'""")
            if old_student:
                return ResponseScheme.error(error=Errors.ALREADY_EXISTS)

            file = request.files[
                [x for x in request.files if match(r""".*\.(png|jpg|jpeg)""", request.files[x].filename)][0]]

            os.mkdir(path.join(self.student_photos, data["username"]))

            filename = str(uuid()).replace("-", "")
            filepath = f"{path.join(self.student_photos, data['username'])}/{filename}.jpg"
            file.save(filepath)

            student_identity = Object()
            student_identity.username = data["username"]
            student_identity.password = data["password"]
            student_identity.photos = json.dumps([filename + ".jpg"])

            database.insert_into("students", student_identity)

            return ResponseScheme.success({
                "username": data["username"],
                "photos": [filename + ".jpg"]
            })

        @self.route("/student/validate_identity", methods=["GET", "POST"])
        def student_validate_identity():
            data = self.data_processing()
            print(data)

            # GET обработка, UI/UX -----------------------
            if request.method == "GET":
                return render_template("upload_photo.html", title="Upload_photo")

            # POST обработка -----------------------------
            if "access_token" not in data:
                return ResponseScheme.error(error=Errors.ACCESS_DENIED)

            if data["access_token"] != self.secret_token:
                return ResponseScheme.error(error=Errors.ACCESS_DENIED)

            if "username" not in data:
                return ResponseScheme.error(error_body={"params": ["username"]}, error=Errors.NOT_ENOUGH_PARAMS)

            old_student = database.select_all("students", cls=Object, where=f"""`username` = '{data["username"]}'""")

            if not old_student:
                return ResponseScheme.error(error=Errors.NOT_FOUND)

            if not request.files:
                print(23244343643)
                return ResponseScheme.error(error=Errors.ACCESS_DENIED)

            file = request.files[[x for x in request.files if match(r""".*\.(png|jpg|jpeg)""", request.files[x].filename)][0]]

            other_students = database.select_all("students", cls=Object, where=f"""`username` != '{data["username"]}'""")
            random_student = choice(other_students)

            old_student_photo = choice(json.loads(old_student[0].photos))
            random_student_photo = choice(json.loads(random_student.photos))

            filename = str(uuid()).replace("-", "")
            print(filename)
            file.save(f"{self.photos_path}/{filename}.jpg")

            x_arrays = self.image_preparation.get_photos_set(old_student[0].username, random_student.username, filename + ".jpg")
            prediction = self.model.predict(*x_arrays)

            response = {"username": data["username"], "is_similar": prediction}
            if prediction is True:
                response["password"] = old_student[0].password

            return ResponseScheme.success(response)

    def run(self, host: t.Optional[str] = None, port: t.Optional[int] = None, debug: t.Optional[bool] = None,
            load_dotenv: bool = True, **options: t.Any) -> None:

        super().run(host, port, debug, load_dotenv, threaded=True, **options)
