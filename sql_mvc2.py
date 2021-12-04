"""
   QSqlQueryModel - a read-only data model for sql queries.

   QSqlTableModel - an editable data model for reading and writing records in a single table.

   QSqlRelationalTableModel - an editable data model for reading and writing records in a relational table.

  Once you've connected one of these models to a physical database table or query,
  you can use them to populate views.
  Views provide delegate objects that allow u to modify the data directly in the view.

  The model connected to the view will automatically update the data in your database and
  reflect any changes to the view.

  NB: U don't have to update the data in your database manually. The model will do that for you.

"""
import sys

from PyQt6.QtSql import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


def createConnection():
    conn = QSqlDatabase.addDatabase("QPSQL")
    conn.setPort(5433)
    conn.setHostName("localhost")
    # conn.setPassword("1234")
    conn.setPort(5433)
    # conn.setUserName("postgres")
    conn.setDatabaseName("Student")
    if not conn.open("postgres", "1234"):
        QMessageBox.critical(QMessageBox(), "Error", "Error: %s" % conn.lastError().text())
        return False
    return True


class Student(QWidget):
    def __init__(self):
        super(Student, self).__init__()
        self.setWindowTitle("QTableView Example")
        self.resize(450, 450)

        self.lay = QVBoxLayout(self)

        lay3 = QVBoxLayout(self)
        lblName = QLabel()
        lblName.setText("Firstname")
        lay3.addWidget(lblName)

        self.txtName = QLineEdit()
        lay3.addWidget(self.txtName)

        lblSname = QLabel()
        lblSname.setText("Lastname")
        lay3.addWidget(lblSname)

        self.txtSname = QLineEdit()
        lay3.addWidget(self.txtSname)

        lblPassword = QLabel()
        lblPassword.setText("Password")
        lay3.addWidget(lblPassword)

        self.txtPwd = QLineEdit()
        self.txtPwd.setEchoMode(QLineEdit.EchoMode.Password)
        lay3.addWidget(self.txtPwd)

        lblEmail = QLabel()
        lblEmail.setText("Email")
        lay3.addWidget(lblEmail)

        self.txtEmail = QLineEdit()
        lay3.addWidget(self.txtEmail)

        createConnection()
        self.model = QSqlTableModel(self)
        self.model.setTable('details.school_details')
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.select()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "First Name")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Last Name")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Password")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "Email")
        # self.model.removeColumn(0)

        # Load the data from the database and populates the model
        # self.model.setFilter("id<=4")  # WHERE clause without "WHERE" keyword. Show the first 4 records

        # Sort the record
        self.model.sort(1, Qt.SortOrder.DescendingOrder)

        # number of rows in the models
        self.rows = self.model.rowCount()
        print(self.rows)

        # Set up the view
        self.view = QTableView()
        self.view.setSortingEnabled(True)
        self.view.setModel(self.model)
        self.view.setColumnHidden(0, True)
        self.view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.view.resizeColumnsToContents()

        self.selection = self.view.selectionModel()
        self.selection.selectionChanged.connect(self.getSelectedRow)
        # self.selection.selectionChanged()

        lay2 = QHBoxLayout(self)

        btn = QPushButton("Create", self)
        btn.clicked.connect(self.insertData)
        btn2 = QPushButton("Update", self)
        btn2.clicked.connect(self.updateData)
        btn3 = QPushButton("Delete", self)
        btn3.clicked.connect(self.deleteData)
        lay2.addWidget(btn)
        lay2.addWidget(btn2)
        lay2.addWidget(btn3)

        print(self.view.currentIndex().row())
        print(self.model.columnCount())

        print(self.model.index(1, 2).data())

        self.lay.addLayout(lay3)
        self.lay.addWidget(self.view)
        self.lay.addLayout(lay2)
        self.setLayout(self.lay)

    def insertData(self):
        try:

            self.model.insertRows(self.rows, 1)
            self.model.setData(self.model.index(self.rows, 1), self.txtName.text())
            self.model.setData(self.model.index(self.rows, 2), self.txtSname.text())
            self.model.setData(self.model.index(self.rows, 3), self.txtPwd.text())
            self.model.setData(self.model.index(self.rows, 4), self.txtEmail.text())
            self.model.submitAll()
            self.rows += 1
        except (Exception, QSqlError) as e:
            self.model.revertAll()
            QSqlDatabase.database().rollback()
            print("Error: " + str(e))

    def updateData(self):
        if self.view.currentIndex().row() > -1:
            record = self.model.record(self.view.currentIndex().row())
            print(record.value('firstname'))
            record.setValue("firstname", self.txtName.text())
            record.setValue("lastname", self.txtSname.text())
            record.setValue("password", self.txtPwd.text())
            record.setValue("email", self.txtEmail.text())
            self.model.setRecord(self.view.currentIndex().row(), record)
            self.model.submitAll()

        else:
            QMessageBox.information(QMessageBox(), "Message", "Select a row to update")

    def deleteData(self):
        print(self.view.currentIndex().row())
        if self.view.currentIndex().row() > -1:
            self.model.removeRow(self.view.currentIndex().row())
            self.rows -= 1
            self.model.submitAll()
        else:
            QMessageBox.information(QMessageBox(), "Message", "Please select a row you'd like to delete")

    def getSelectedRow(self):
        # print(self.selection.hasSelection())
        # selectedRow = self.selection.selectedRows()
        row = self.view.selectionModel().currentIndex().row()
        # data = selectedRow.index()
        # print(row, " ", selectedRow)
        fname = self.model.data(self.model.index(row, 1))
        lname = self.model.data(self.model.index(row, 2))
        password = self.model.data(self.model.index(row, 3))
        email = self.model.data(self.model.index(row, 4))
        self.txtName.setText(str(fname))
        self.txtSname.setText(str(lname))
        self.txtPwd.setText(str(password))
        self.txtEmail.setText(str(email))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    # if not createConnection():
    #     sys.exit(1)
    win = Student()
    win.show()
    sys.exit(app.exec())
