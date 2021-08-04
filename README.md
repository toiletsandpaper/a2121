# a2121
Repo of School X team (DSTU) for Archipelag2121 F-S Team Challenge

## Инструкция к использованию приложения:
 1. Перейдите по ссылке https://console.aws.amazon.com/cloud9/ide/ca437448a3004726b8385c4192fda7d9 (к сожалению, сервер может иногда выключаться из-за отсутсвия памяти, и через неопределённое количество времени включаться, а аналогов для запуска по HTTPS предоставлено не было) и залогиньтесь под root-user с данными lii291001@gmail.com:A2121_PASSWORD
 2. Затем перейдите по https://ca437448a3004726b8385c4192fda7d9.vfs.cloud9.us-east-1.amazonaws.com/ (если ничего нет, то в консоли внизу запустите `python manage.py runserver` и ещё раз перейдите по ссылке ранее)
 3. Зарегистрируйте пользователя под доменами @gmail.com или @yandex.ru (желательно @gmail.com, так как будет выдан root-аккаунт под этим доменом). Все они представляют собой домены 3-х условных вузов, чтобы каждый ВУЗ разделял свои планы на одном и том же сервере. Поэтому, будучи админом с @yandex.ru - вы сможете редактировать только @yandex.ru учеников.
 4. Вам на почту придёт письмо активации профиля, которое нужно обязательно принять. Для этого мы настроили SMTP от Яндекса.
 5. После входа, вам нужно будет ввести имя и фамилию студента, а так же выбрать группу. Для @gmail.com создана всего одна группа, для @yandex.ru две группы. Все они представляют собой определенные студенческие группы, которые в дальнейшем будут получать расписание по этим группам.
 6. Далее, под учётной записью админа `root:12345` нужно будет создать новую дисциплину, затем новый учебно-временной блок, который будет запускаться, а затем объявить дисциплины (последний пункт), где нужно будет выставить время начала и конца занятия. Все эти пункты делаются через `Админ Панель Заведения`
 7. Там же, root может создавать юзерам их привелегии, превращая их в учителей. (Сам же root - супер-юзер)
 8. Так же в меню можно делать и просматривать объявления для всех студентов.
 9. Для обратной связи - в футере есть кнопка "Контакты", где можно отправить сообщение администратору.
<hr>
Лицензия **aion** - *MIT*, она же лежит на их [GitHub](https://github.com/jeffhow/aion) и в папке `aion` 

Для обратной связи, если AWS всё ещё не запускается - свяжитесь с @toiletsandpaper
