# Docker
1. Собрать образ
    
    `docker build -t notification .`
    
    `docker build --build-arg some_variable_name=a_value`
    `some_variable_name - ARG в dockerfile `

2. Запустить образ
    `docker run -it -d --name notification -p 127.0.0.1:8000:8080 notification`
    
    `docker run -d --name notification -p 80:80 -e MODULE_NAME="app.main"  notification`
    
    Запустить docker-image и задать **имя хоста** контейнера:

    `docker run -h имяхоста -it ubuntu bash`

    `-it` - сеаснс в интерактивном режиме
    `bash` - открывает bash
     при выходе контейнер останавливается
    
3. Проверить запущен ли контейнер и узнать CONTAINERID: 

    `docker -ps`
    
4. Проверить логи:

    `docker logs -f CONTAINERID`
    
5. Остановить контейнер: 
    
    `docker stop CONTAINERID`

6. Удалить остановленные контейнеры: 

    `docker rm -v $(docker ps -aq -f status=exited)`
    
7. Удаить все images

    `docker rmi -f $(docker images -a -q)`

8. Инфо о контейнере:

    `docker inspect имяконтейнера`

    `docker inspect имяконтейнера | grep IPAddress`

9. Список изменений в работающем контейнере:

    `docker diff имяконтейнера`


10. Получение, запуск (в фоне) и проброс.

    `docker run -d -p 8000:8080 bitnami/apache`

    `bitnami/apache` - имя образа
    `-d` - запустить в фоновом режиме
    `-p портНаХостМашине:ПортВнутриКонтерйнера`
    
# Docker-compose

1. Собрать проект

    `docker-compose build`

2. Запустить проект

    `docker-compose up`
    
3. Остановить и удалить контейнер и image

`docker-compose rm -f -s bot && docker rmi investhelperbe_bot`
