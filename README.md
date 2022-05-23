[![Continuous Integration & Delivery](https://github.com/amgfrthsp/company_mentions/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/amgfrthsp/company_mentions/actions/workflows/ci-cd.yml)

# Мисс Сентимент

<details>
<summary>ПП ВШЭ ФКН ПМИ</summary>

Программный проект на тему **«Сбор и анализ информации об упоминании компаний в социальных сетях»**.

Выполнили студентки ВШЭ ФКН ПМИ **Груздева Марина Евгеньевна**, группа БПМИ205 и **Семенова-Звенигородская София Андреевна**, группа БПМИ201.
Руководитель проекта — **Казаков Евгений Александрович**, Software Engineer at Meta.
</details>

[@ms_sentiment_bot](https://t.me/ms_sentiment_bot) — telegram-бот, который не только присылает упоминания компаний или брендов в Meduza, Twitter и Панорама, но и анализирует их контекст 🙂😐🙁.


## Запуск

Чтобы запустить у себя локально точно такого же бота, нужно
1. Создать бота у [@BotFather](https://t.me/BotFather) и получить API Token.
2. Зарегистрировать приложение на [Twitter Developer Platform](https://developer.twitter.com/en/docs/twitter-api) и получить Bearer Token.
3. Установить [docker](https://docs.docker.com/get-docker/) и [docker-compose](https://docs.docker.com/compose/install/).
4. Скачать готовые docker-образы `docker-compose pull`
5. Запустить `TELEGRAM_BOT_TOKEN="123..." TWITTER_BEARER_TOKEN="AAA..." docker-compose up`