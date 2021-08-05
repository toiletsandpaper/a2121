import smtplib
from threading import Thread
import subprocess as sp
from video_model.fmss import fmss
from os import listdir, path


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
        return f"""
        Уважаемый пользователь!
        Ваш видеопоток, размещенный по адресу {video_link} был успешно загружен на сервер!
        
        С уважением,
        Команда School X DSTU
        """

    @staticmethod
    def failed_text(video_link):
        return f"""
            Уважаемый пользователь!
            Ваш видеопоток, размещенный по адресу {video_link} не был загружен на сервер!
            Наш алгоритм заметил схожесть данного видеоряда с уже имеющимся на сервере!

            С уважением,
            Команда School X DSTU
            """


    def send_email_feedback(self, text, video_link):
        text = text
        message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(self.school_x_email,
                                                               self.email,
                                                               "Обработка и загрузка Вашего видеопотока",
                                                               text)
        server = smtplib.SMTP_SSL('smtp.yandex.com')
        server.set_debuglevel(1)
        server.ehlo(self.school_x_email)
        server.login(self.school_x_email, self.school_x_password)
        server.auth_plain()
        server.sendmail(self.school_x_email, self.email, message)
        server.quit()

        return True

    def run(self):
        process = sp.Popen([f"""youtube-dl -o "%(id)s.%(ext)s" --format mp4 {self.video_link}"""], shell=True,
                                stderr=sp.PIPE, stdout=sp.PIPE, stdin=sp.PIPE, cwd=self.upload_videos)

        response, error = process.communicate()
        filename = response

        for video in listdir(self.upload_videos):
            if path.isdir(video):
                continue

            similarity = fmss(self.upload_videos, filename, video)

            if similarity > 0.5:
                self.send_email_feedback(video_link=self.video_link, text=self.failed_text(self.video_link))
                break

        self.send_email_feedback(video_link=self.video_link, text=self.success_text(self.video_link))



