import Constants
import sys
import openai 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox
)

openai.api_key = Constants.API_KEY

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init__ui()
    
    def init__ui(self):
        #Create widgets
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap('robot.png').scaled(150,150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)

        self.input_label = QLabel('What is on your mind?')
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Type it here...')
        self.answer_label = QLabel('Answer')
        self.answer_field = QTextEdit()
        self.answer_field.setReadOnly(True)
        self.submit_button = QPushButton('Submit')
        self.submit_button.selfStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                }
            QPushButton:hover{
                background-color: #3eBe41;
            }      
            """
        )
        self.popular_questions_group = QGroupBox('Popular Questions')
        self.popular_questions_layout = QVBoxLayout()
        self.popular_questions = ["What is Machine Learning?", "How do I become an ML engineer?", "What are some popular ML tools?"]
        self.question_buttons = []

        #Create a layout 
        layout = QVBoxLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        #add logo
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        #add input field
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)
        layout.addLayout(input_layout)

        #Add answer field
        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_field)

        #add populae quesrion button
        for question in self.popular_questions:
            button = QPushButton(question)
            button.setStyleSheet(
                """
                QPushButton{
                    background-color:#FFFFFF;
                    border: 2px solid #00AEFF;
                    color: #00AEFF;
                    padding: 10px 20px;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                    QPushButton:hover{
                        background-color: #00AEFF;
                        color: #FFFFFF;
                    }
                """
            )
            button.clicked.connect(lambda _, q=question:self.input_field.setText(q))
            self.popular_questions_layout.addWidget(button)
            self.question_buttons.append(button)
        self.popular_questions_group.setLayout(self.popular_questions_layout)
        layout.addWidget(self.popular_questions_group)

        #Set the layout
        self.setLayout(layout)

        #set window properties
        self.setWindowTitle('Machine Learning Advice Bot')
        self.setGeometry(200,200,600,600)

        #Connect submit to the function which queries openai API
        self.submit_button.clicked.connect(self.get_answer)

    def get_answer(self):
        question = self.input_field.text()

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [{"role":"user","content":"You are a machine learning engineer expert. Answer the following question in a concise way or with bullet points."},
                        {"role":"user","content":f'{question}'}],
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature = 0.7
        )

        answer = completion.choices[0].message.content

        self.answer_field.setText(answer)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

