## Лабораторная работа №4

### Тема: СИСТЕМА УПРАВЛЕНИЯ БАЗОЙ ДАННЫХ ДЕТЕЙ С ОПФР

#### CD

![](https://bitbucket.org/dejkunelena/trpo/raw/07e471995208bf714a4f8664d1759e33a5df5ef7/media/cd.png)

#### SD

USE CASE: Авторизация

![](https://bitbucket.org/dejkunelena/trpo/raw/07e471995208bf714a4f8664d1759e33a5df5ef7/media/sd_1.png)

USE CASE: Заполнение личной карточки ребенка

![](https://bitbucket.org/dejkunelena/trpo/raw/07e471995208bf714a4f8664d1759e33a5df5ef7/media/sd_2.png)

USE CASE: Формирование статистики по критериям

![](https://bitbucket.org/dejkunelena/trpo/raw/07e471995208bf714a4f8664d1759e33a5df5ef7/media/sd_3.png)


#### DDL



``` sql
CREATE TABLE 'Locaion' (
	'id' INT NOT NULL AUTO_INCREMENT,
	'region' VARCHAR(150) NOT NULL,
	'area' VARCHAR(150) NOT NULL,
	'city' VARCHAR(150) NOT NULL,
	'isCity' BOOLEAN(150) NOT NULL,
	PRIMARY KEY ('id')
);

CREATE TABLE 'Institution' (
	'id' INT NOT NULL AUTO_INCREMENT,
	'parentId' INT NOT NULL AUTO_INCREMENT,
	'locationId' INT NOT NULL AUTO_INCREMENT,
	'name' VARCHAR(255) NOT NULL,
	'type' INT NOT NULL,
	'userId' INT NOT NULL,
	PRIMARY KEY ('id')
);

CREATE TABLE 'User' (
	'id' INT NOT NULL AUTO_INCREMENT,
	'login' VARCHAR(255) NOT NULL UNIQUE,
	'password' VARCHAR(150) NOT NULL,
	'email' VARCHAR(150) NOT NULL UNIQUE,
	'instId' INT(150) NOT NULL UNIQUE,
	PRIMARY KEY ('id')
);

CREATE TABLE 'User' (
	'id' INT NOT NULL AUTO_INCREMENT,
	'first_name' VARCHAR(150) NOT NULL,
	'last_name' VARCHAR(150) NOT NULL,
	'middle_name' VARCHAR(150) NOT NULL,
	'isMan' BOOLEAN NOT NULL,
	'birthday' DATE NOT NULL,
	'instId' INT NOT NULL,
	'address' VARCHAR(255) NOT NULL,
	'class_or_course' INT NOT NULL,
	'disability' INT NOT NULL,
	'is_needs_help' BOOLEAN NOT NULL,
	'type_of_help_in_center' INT NOT NULL,
	'type_of_help_in_school' INT NOT NULL,
	'city' INT NOT NULL,
	PRIMARY KEY ('id')
);

ALTER TABLE 'Institution' ADD CONSTRAINT 'Institution_fk0' FOREIGN KEY ('parentId') REFERENCES 'Locaion'('id');

ALTER TABLE 'Institution' ADD CONSTRAINT 'Institution_fk1' FOREIGN KEY ('locationId') REFERENCES 'Institution'('id');

ALTER TABLE 'Institution' ADD CONSTRAINT 'Institution_fk2' FOREIGN KEY ('userId') REFERENCES 'User'('id');

ALTER TABLE 'User' ADD CONSTRAINT 'User_fk0' FOREIGN KEY ('instId') REFERENCES 'Institution'('id');

ALTER TABLE 'User' ADD CONSTRAINT 'User_fk0' FOREIGN KEY ('instId') REFERENCES 'Institution'('id');
```

#### Диаграмма классов

![](https://bitbucket.org/dejkunelena/trpo/raw/12c77a2e366ff6243fc94d9a5d094756fb2212fb/media/diagram.png)



#### Демонстрация работы программы 

##### Основной интерфейс программы

![](https://bitbucket.org/dejkunelena/trpo/raw/12c77a2e366ff6243fc94d9a5d094756fb2212fb/media/lab5_1.png)


##### Создание карточки

![](https://bitbucket.org/dejkunelena/trpo/raw/12c77a2e366ff6243fc94d9a5d094756fb2212fb/media/lab5_2.png)

##### Отображение статистики 

![](https://bitbucket.org/dejkunelena/trpo/raw/12c77a2e366ff6243fc94d9a5d094756fb2212fb/media/lab5_3.png)

##### Формирование критериев отчета

![](https://bitbucket.org/dejkunelena/trpo/raw/12c77a2e366ff6243fc94d9a5d094756fb2212fb/media/lab5_4.png)

##### Пример вывода отчета 
![](https://bitbucket.org/dejkunelena/trpo/raw/12c77a2e366ff6243fc94d9a5d094756fb2212fb/media/lab5_5.png)

##### Выбор настроек учетной записи

![](https://bitbucket.org/dejkunelena/trpo/raw/12c77a2e366ff6243fc94d9a5d094756fb2212fb/media/lab5_6.png)


