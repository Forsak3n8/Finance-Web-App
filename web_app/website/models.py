import pymysql
from sqlalchemy import create_engine
import pandas as pd

class db_helper:
    # initalize datebase login information
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.autocommit = False
        self.database = 'finance_data'
        print('Database login loaded')

    # initalize function for database connection
    def __connect__(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, autocommit=self.autocommit)
        self.cur = self.con.cursor()
    
    # secondary connection for after database creation
    def __connect_to_finance__(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, autocommit=self.autocommit)
        self.cur = self.con.cursor()

    # disconnects from database
    def __disconnect__(self):
        self.con.close()

    # account query to populate dynamic table in /accounts route
    def accounts_query(self, sql):
        try:
            self.__connect_to_finance__()

            if self.con.open == True:
                self.cur.execute(sql)
                results = self.cur.fetchall()
                self.__disconnect__()
                print('Accounts query success')
                return results
        
            elif self.con.open == False:
                print('Accounts query connection issue')
            
        except pymysql.Error as e:
            print("Accounts query failed with exception: %d: %s" %(e.args[0], e.args[1]))

    # account query to delete or edit account in database
    def account_change_query(self, sql):
        try:
            self.__connect_to_finance__()

            if self.con.open == True:
                self.cur.execute(sql)
                self.con.commit()
                self.__disconnect__()
                print('Account table change success')

            elif self.con.open == False:
                print('Account table change connection issue')

        except pymysql.Error as e:
            print("Account table change failed with exception: %d: %s" %(e.args[0], e.args[1]))


    # creates database if connection is valid and database does not already exist
    def create_database(self):
        sql = 'CREATE DATABASE IF NOT EXISTS finance_data'
        
        try:
            self.__connect__()

            if self.con.open == True:
                self.cur.execute(sql)
                self.con.commit()
                self.__disconnect__()
                print('Database created')

            elif self.con.open == False:
                print('Database creation connection issue')

        except pymysql.Error as e:
            print("Database creation failed with exception: %d: %s" %(e.args[0], e.args[1]))

    # creates tables in database if connection is valid and tables do not already exist
    def create_tables(self):
        date = "CREATE TABLE IF NOT EXISTS date(short_date date, weekday_name varchar(9) NOT NULL, day_month int(11) NOT NULL, month_name varchar(9) NOT NULL, quarter int(11) NOT NULL, year int(11) NOT NULL, weekday_number int(11) NOT NULL, month_number int(11) NOT NULL, PRIMARY KEY (short_date))"
        accounts = "CREATE TABLE IF NOT EXISTS accounts(account_id int(11) NOT NULL AUTO_INCREMENT, account_type varchar(45) NOT NULL, account_description varchar(200) NOT NULL, PRIMARY KEY (account_id))"
        category = "CREATE TABLE IF NOT EXISTS category(category_id int(11) NOT NULL, category_description varchar(100) NOT NULL, category_essential tinyint(4) NOT NULL, PRIMARY KEY (category_id))"
        transaction_type = "CREATE TABLE IF NOT EXISTS transaction_type(transaction_type_id int(11) NOT NULL AUTO_INCREMENT, transaction_type_description varchar(70) NOT NULL, transaction_is_purchase tinyint(4) NOT NULL, PRIMARY KEY (transaction_type_id))"
        transaction_facts = "CREATE TABLE IF NOT EXISTS transaction_facts(transaction_id int(11) NOT NULL AUTO_INCREMENT, account_id int(11) NOT NULL, transaction_type_id int(11) NOT NULL, category_id int(11) NOT NULL, short_date date NOT NULL, transaction_description varchar(100) NOT NULL, transaction_amount decimal(10,0) NOT NULL, PRIMARY KEY (transaction_id), FOREIGN KEY (account_id) REFERENCES accounts(account_id), FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(transaction_type_id), FOREIGN KEY (category_id) REFERENCES category(category_id), FOREIGN KEY (short_date) REFERENCES date(short_date))"
        category_null = "INSERT IGNORE INTO category VALUES(-1, 'NOT A PURCHASE', 0)"
        
        try:
            self.__connect_to_finance__()

            if self.con.open == True:
                self.cur.execute(date)
                self.cur.execute(accounts)
                self.cur.execute(category)
                self.cur.execute(transaction_type)
                self.cur.execute(transaction_facts)
                self.cur.execute(category_null)
                self.con.commit()
                self.__disconnect__()
                print('Tables created')

            elif self.con.open == False:
                print('Table creation connection issue')

        except pymysql.Error as e:
            print("Table creation failed with exception: %d: %s" %(e.args[0], e.args[1]))

    # creates daterange with pandas and loads data into created tables if connection is valid and data does not already exist
    def create_daterange(self):

        start_date = '2023-1-1'
        end_date = '2024-12-31'

        insert = "INSERT IGNORE INTO date SELECT * FROM tempdatetable"
        drop = "DROP TABLE tempdatetable"

        daterange = pd.date_range(start=start_date, end=end_date, freq='D')
        datetable_df = pd.DataFrame(columns=['short_date', 'weekday_name', 'day_month', 'month_name', 'quarter', 'year', 'weekday_number', 'month_number'])
        datetable_df['short_date'] = pd.to_datetime(datetable_df['short_date'])
        datetable_df['day_month'] = datetable_df['day_month'].astype(int)
        datetable_df['quarter'] = datetable_df['quarter'].astype(int)
        datetable_df['year'] = datetable_df['year'].astype(int)
        datetable_df['weekday_number'] = datetable_df['weekday_number'].astype(int)
        datetable_df['month_number'] = datetable_df['month_number'].astype(int)
        datetable_df['short_date'] = daterange
        datetable_df['weekday_name'] = daterange.day_name()
        datetable_df['day_month'] = daterange.day
        datetable_df['month_name'] = daterange.month_name()
        datetable_df['quarter'] = daterange.quarter
        datetable_df['year'] = daterange.year
        datetable_df['weekday_number'] = daterange.weekday + 1
        datetable_df['month_number'] = daterange.month

        tempcon = create_engine("mysql+mysqlconnector://root:@localhost:3306/finance_data")

        try:
            self.__connect_to_finance__()

            if self.con.open == True:
                datetable_df.to_sql('tempdatetable', con=tempcon, if_exists ='replace', index=False)
                tempcon.dispose()
                self.cur.execute(insert)
                self.cur.execute(drop)
                self.con.commit()
                self.__disconnect__()
                print('Daterange created')

            elif self.con.open == False:
                print('Daterange creation connection issue')

        except pymysql.Error as e:
            print("Daterange creation failed with exception: %d: %s" %(e.args[0], e.args[1]))