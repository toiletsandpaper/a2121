import os
import smtplib
from threading import Thread
import subprocess as sp
from time import sleep

from video_model.fmss import fmss
from os import listdir, path
from uuid import uuid4 as uuid


class VideoProcessing(Thread):
    def __init__(self, video_link, email, upload_videos):
        super().__init__()

        self.upload_videos = upload_videos
        self.name = "VideoProcessing"
        self.video_link = video_link
        self.email = email

        self.school_x_email = "SchoolX.Ar4ikov@yandex.ru"
        self.school_x_password = "W4Hfx0t2Cte8"
        self.school_x_port = 465

    @staticmethod
    def success_text(video_link):
        return f"Successful upload!\nVideo link: {video_link}\n\nBest regards\nTeam School X DSTU"

    @staticmethod
    def failed_text(video_link):
        return f"Failed upload! That video is similiar to another video on this server\nVideo link: {video_link}\n\nBest regards\nTeam School X DSTU"

    def send_email_feedback(self, text):
        text = text
        message = "\n".join([
            f"From: {self.school_x_email}",
            f"To: {self.email}",
            "Subject: About processing your video",
            "",
            text
        ])
        server = smtplib.SMTP_SSL('smtp.yandex.com')
        server.ehlo(self.school_x_email)
        server.login(self.school_x_email, self.school_x_password)
        server.auth_plain()
        server.sendmail(self.school_x_email, [self.email], message)
        server.quit()

        return True

    def run(self):
        # process = sp.Popen([f"""youtube-dl -o "uploads/videos/%(id)s.%(ext)s" --format mp4 {self.video_link}"""], shell=True,
        #                         stderr=sp.PIPE, stdout=sp.PIPE, stdin=sp.PIPE)
        #
        # response, error = process.communicate()
        # filename = response.decode()
        #
        # sleep(10)
        # print('------------')

        filename = str(uuid())
        os.system(f"""youtube-dl -o "uploads/videos/{filename}.%(ext)s" --format mp4 {self.video_link}""")

        sleep(10)

        for video in listdir("uploads/videos/"):
            if path.isdir(video):
                continue

            similarity = fmss(self.upload_videos, filename, video)
            #print(similarity)

            if similarity > 0.5:
                self.send_email_feedback(text=self.failed_text(self.video_link))
                break

        self.send_email_feedback(text=self.success_text(self.video_link))



