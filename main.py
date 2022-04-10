from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
  
        # setting title
        self.setWindowTitle("Python ")
  
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
  
        # calling method
        #self.UiComponents()

        # opening window in maximized size
        self.showMaximized()
  
        # showing all the widgets
        self.show()
  
    # method for widgets
    def UiComponents(self):
  
        # creating label
        label = QLabel("Label", self)
  
        # setting geometry to label
        label.setGeometry(100, 100, 120, 40)
  
        # adding border to label
        label.setStyleSheet("border : 2px solid black")
  
        
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(stylesheet)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())