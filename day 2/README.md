# Day 2 School X module assignment

В данном случае, мы не успели формально закончить работу с UI/UX оформлением задания, поэтому для проверки придётся немного повозиться.

## Для проверки определения по фото

1. Мы добавили добавили фотографии двух пользователей (папка `test`), которые в теории могут залогиниться как под своим, так и под чужим аккаунтом.
2. Вы скачиваете эти фотографии к себе на ПК.
3. Заходите на [Наш сайт](http://45.156.21.87:8080/), нажимаете кнопку `Войти`, а дальше внизу по ссылке [Войти по фото](http://80.249.146.230:8081/student/validate_identity), после чего вас перебросит на другой сайт.
4. Дальше вы вводите один из валидных логинов (`Ar4ikov` или `ToiletSandPaper`), а потом загружаете любое фото из тестовой папки (или любое другое фото).
5. Если алгоритму выданы валидные логины и он распознал ваше фото, как владельца аккаунта, то на следующей странице будет json-ответ с графой `password`. Если нет - то этой графы не будет.
6. Базы данных ещё не связаны, так как всё время было потрачено на алгоритм. WORK IN PROGRESS.

## Для создания нового профиля для проверки

1. Для создания нового профиля - мы используем на локальной машине скрипт `create_student.py`, где мы указываем данные учётной записи и фотографии в базе.
2. Иначе, пока, никак нового пользователя со стороны не добавить. WORK IN PROGRESS.

## Для сверки видео на схожесть

1. Заходите на [Наш второй сайт](http://80.249.146.230:8081/video/upload).
2. Укажите ваш **Email** и вставьте ссылку на Youtube-видео.
3. Если *такого* видео или *похожего на него*(попробуйте проверить на [дублирующихся видео Youtube](https://www.youtube.com/results?search_query=hello+hi+cat)) нет на сервере, то сервер сохранит его у себя. Если такое уже видео есть - то он напишет о том, что такое видео уже есть.
4. Так как проверка занимает достаточно много времени, то о результатах проверки мы сообщим вам на указанный вами *Email* сразу же, как только сервер закончит проверку.

<hr>

# Важнная ремарка! 

Наша модель (чтобы собрать весь код у себя) не может быть загружена на GitHub, так как у него ограничение на 100 МБ на один файл. Поэтому позже сюда будет прикреплена ссылка на облако для скачивания модели.