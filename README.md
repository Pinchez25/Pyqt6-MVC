# Pyqt6-MVC
This project makes use of Qt MVC to get data from database and display in QTableView and also has CRUD operations

#### Clone this repository or download it and unzip
#### To run the file, create a database and table with fields Id, firstname, lastname, password and email (Exactly as written NOTE the casing, Id is autoincrement)
#### Since qt doesn't offer mysql driver you can build your own or use another database. In this project i use QPSQL driver for postgresql database.
#### Replace the details for database driver, database name,table, username, password with your own.
### conn = QSqlDatabase.addDatabase("QPSQL"), see docs for more drivers
### conn.setDatabaseName("your own database name")
### if not conn.open("your username", "your password")
### self.model.setTable('your table name')



#### That's it.Run the application.
#### Thanks!
