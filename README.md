# Приложение QRKot

## Описание проекта

Создать приложение для Благотворительного фонда поддержки котиков **QRKot**

### Проекты

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу *First In, First Out*: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.


### Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

### Пользователи

Целевые проекты создаются администраторами сайта.

Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.

Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

В приложении три модели: 
* Пользователи
* Проекты
* Пожертвования

## Инструкция по развёртыванию проекта

* клонировать проект на компьютер `git clone git@github.com:Vediusse/cat_charity_fund.git`
* создание виртуального окружения `python3 -m venv venv`
* запуск виртуального окружения `. venv/bin/activate`
* установить зависимости из файла requirements.txt `pip install -r requirements.txt`
* запуск сервера `uvicorn main:app`
* запуск сервера с автоматическим рестартом `uvicorn main:app --reload`
* инициализируем Alembic в проекте `alembic init --template async alembic`
* создание файла миграции `alembic revision --autogenerate -m "migration name"`
* применение миграций `alembic upgrade head`
* отмена миграций `alembic downgrade`


###Пользователи

Все настройки пользователей возьмите из проекта по бронированию переговорок.
* Используйте библиотеку FastAPI Users.
* В настройках укажите транспорт Bearer и стратегию JWT.
* Подключите роутеры Auth Router, Register Router, Users Router.
* Не изменяйте базовую модель пользователя.
* Установите запрет на удаление пользователей: эндпоинт удаления пользователя переопределите на deprecated.

###Проекты

Создайте модель CharityProject, свяжите её с таблицей `charityproject` в базе данных

Столбцы таблицы `charityproject`:
* `id` — первичный ключ
* `name` — уникальное название проекта, обязательное строковое поле; допустимая длина строки — от 1 до 100 символов включительно
* `description` — описание, обязательное поле, текст; не менее одного символа
* `full_amount` — требуемая сумма, целочисленное поле; больше 0
* `invested_amount` — внесённая сумма, целочисленное поле; значение по умолчанию — 0
* `fully_invested` — булево значение, указывающее на то, собрана ли нужная сумма для проекта (закрыт ли проект); значение по умолчанию — False
* `create_date` — дата создания проекта, тип DateTime, должно добавляться автоматически в момент создания проекта
* `close_date` — дата закрытия проекта, DateTime, проставляется автоматически в момент набора нужной суммы

## Пожертвования

Создайте модель Donation, свяжите её с таблицей `donation` в базе данных

Столбцы таблицы `donation`:
* `id` — первичный ключ
* `user_id` — id пользователя, сделавшего пожертвование. Foreign Key на поле user.id из таблицы пользователей
* `comment` — необязательное текстовое поле
* `full_amount` — сумма пожертвования, целочисленное поле; больше 0
* `invested_amount` — сумма из пожертвования, которая распределена по проектам; значение по умолчанию равно 0
* `fully_invested` — булево значение, указывающее на то, все ли деньги из пожертвования были переведены в тот или иной проект; по умолчанию равно False
* `create_date` — дата пожертвования; тип DateTime; добавляется автоматически в момент поступления пожертвования
* `close_date` — дата, когда вся сумма пожертвования была распределена по проектам; тип DateTime; добавляется автоматически в момент выполнения условия


## Права пользователей

Любой посетитель сайта (в том числе неавторизованный) может посмотреть список всех проектов

Суперпользователь может: 
* создавать проекты
* удалять проекты, в которые не было внесено средств
* изменять название и описание существующего проекта, устанавливать для него новую требуемую сумму (но не меньше уже внесённой)

Никто не может менять через API размер внесённых средств, удалять или модифицировать закрытые проекты, изменять даты создания и закрытия проектов

Любой зарегистрированный пользователь может сделать пожертвование

## Документация 

[alt text](http://127.0.0.1/docs)



