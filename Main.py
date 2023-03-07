# ScriptReader
# June Knauth (github.com/knauth), 20230214

import sys
import Parser
import People
import Spoken
import pyttsx3 as tts
import os

from PyQt6.QtCore import Qt
from PyQt6 import QtGui
from PyQt6.QtWidgets import (QApplication, QDialog, QFileDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox,
                             QFormLayout, QLabel, QLineEdit, QCheckBox, QTextEdit, QMessageBox)

class MainApp(QDialog):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)

        self.setWindowTitle("ScriptReader")
        self.setWindowIcon(QtGui.QIcon('icons/autism.jpg'))
        mainLayout = QVBoxLayout()
        self.createPDFButton()
        self.createParDisplay()
        self.createNavButtons()

        mainLayout.addWidget(self.PDFButton)
        mainLayout.addWidget(self.parGroupBox)
        mainLayout.addLayout(self.navButtons)

        self.setLayout(mainLayout)

    def createPDFButton(self):
        self.PDFButton = QPushButton("Select Input PDF")
        self.PDFButton.clicked.connect(self.getPDFData)

    def getPDFData(self):
        pdf_dialog = PDFDialog()
        pdf_dialog.exec()
        self.parsedPDF = pdf_dialog.ParsedPDF

        self.parPosition = 0
        self.parCount = len(self.parsedPDF.segments)
        self.updateParagraphDisplay()

    def updateParagraphDisplay(self):
        seg = self.parsedPDF.segments[self.parPosition]
        self.displaySpeakerLine.setText(seg.speaker)
        self.displayToneLine.setText(seg.tone)
        self.displayContentText.setText(seg.content)
        self.displayParagraphInfo.setText(f"Paragraph {self.parPosition + 1}/{self.parCount}")

    def nextParagraph(self):
        if self.parPosition + 1 < self.parCount:
            self.parPosition += 1
        self.updateParagraphDisplay()

    def prevParagraph(self):
        if self.parPosition != 0:
            self.parPosition -= 1
        self.updateParagraphDisplay()

    def createNavButtons(self):
        self.navButtons = QHBoxLayout()

        nextButton = QPushButton("Next")
        nextButton.clicked.connect(self.nextParagraph)

        prevButton = QPushButton("Prev")
        prevButton.clicked.connect(self.prevParagraph)

        self.navButtons.addWidget(prevButton)
        self.navButtons.addStretch()
        self.navButtons.addWidget(nextButton)

    def createParDisplay(self):
        self.parGroupBox = QGroupBox() # Box for pretty border and label
        layout = QFormLayout() # QForm layout within the box
        # Setup display boxes
        self.displayParagraphInfo = QLabel("No PDF Loaded")

        self.displaySpeakerLine = QLineEdit()
        self.displaySpeakerLine.setText("Mortimer")

        self.displayToneLine = QLineEdit()
        self.displayToneLine.setText("Chirpy")

        self.displayContentText = QTextEdit()
        self.displayContentText.setText("I am so happy to be saying placeholder text!")

        # Show input boxes
        layout.addWidget(self.displayParagraphInfo)
        layout.addRow(QLabel("Speaker:"), self.displaySpeakerLine)
        layout.addRow(QLabel("Tone:"), self.displayToneLine)
        layout.addRow(QLabel("Content:"), self.displayContentText)

        self.parGroupBox.setLayout(layout)

class PDFDialog(QDialog):
    def __init__(self, parent=None):
        super(PDFDialog, self).__init__(parent)

        self.setWindowTitle("PDF Input Dialog")
        mainLayout = QFormLayout()

        # Setup PDF Options
        self.setPageRangeBool = QCheckBox()
        self.setPageRangeBool.setChecked(True)

        self.editFirstPageLine = QLineEdit()
        self.editFirstPageLine.setText("16")

        self.editLastPageLine = QLineEdit()
        self.editLastPageLine.setText("17")

        self.editLineDelimLine = QLineEdit()
        self.editLineDelimLine.setText("\n\n")

        self.editSpeakDelimLine = QLineEdit()
        self.editSpeakDelimLine.setText(":")

        self.editToneDelimLine = QLineEdit()
        self.editToneDelimLine.setText(",")

        # Show input boxes
        mainLayout.addRow(QLabel("Use Page Range"), self.setPageRangeBool)
        mainLayout.addRow(QLabel("First Page"), self.editFirstPageLine)
        mainLayout.addRow(QLabel("Last Page"), self.editLastPageLine)
        mainLayout.addRow(QLabel("Pararaph Delimiter"), self.editLineDelimLine)
        mainLayout.addRow(QLabel("Speaker Delimiter"), self.editSpeakDelimLine)
        mainLayout.addRow(QLabel("Tone Delimiter"), self.editToneDelimLine)

        # Setup Select Button
        self.labelSelectedPDF = QLabel("No PDF Selected")
        PDFSelectButton = QPushButton("Select Input PDF")
        PDFSelectButton.clicked.connect(self.getPDFFilename)

        # Show Select Button
        mainLayout.addRow(self.labelSelectedPDF)
        mainLayout.addRow(PDFSelectButton)

        # Setup/Show Parse Button
        PDFParseButton = QPushButton("Parse PDF")
        PDFParseButton.clicked.connect(self.parsePDF)
        mainLayout.addRow(PDFParseButton)

        self.setLayout(mainLayout)

    def parsePDF(self):
        if self.transformCheckInputs():
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            try:
                if self.UsePageRange:
                    self.ParsedPDF = Parser.Parser(self.PDFFile, self.FirstPage, self.LastPage,
                                     self.ParDelim, self.SpeakDelim, self.ToneDelim)

                else:
                    self.ParsedPDF = Parser.Parser(self.PDFFile, None, None,
                                     self.ParDelim, self.SpeakDelim, self.ToneDelim)

                QApplication.restoreOverrideCursor()
                self.close()
            except Exception as e:
                self.showErrorDialog("Couldn't parse PDF")
                print(e)

    def transformCheckInputs(self):
        try:
            self.UsePageRange = bool(self.setPageRangeBool.isChecked())
            if self.UsePageRange:
                self.FirstPage = int(self.editFirstPageLine.text())
                self.LastPage = int(self.editLastPageLine.text())
            self.ParDelim = str(self.editLineDelimLine.text())
            self.SpeakDelim = str(self.editSpeakDelimLine.text())
            self.ToneDelim = str(self.editToneDelimLine.text())

            self.PDFFile = str(self.inputPDFFile)

            assert self.PDFFile != ''
        except Exception as e:
           self.showErrorDialog("Input error- check to make sure inputs are correct and you have selected a file.")
           print(e)
           return False

        return True

    def getPDFFilename(self):
        self.labelSelectedPDF.setText("No PDF Selected")
        self.inputPDFFile = QFileDialog.getOpenFileName(self, 'Open PDF',
            os.getcwd(), "PDF Files (*.pdf)")[0]
        self.labelSelectedPDF.setText(self.inputPDFFile)

    def showErrorDialog(self, text):
       msg = QMessageBox()

       msg.setText(text)
       msg.setWindowTitle("Error")

       msg.exec()

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('fusion')

    win = MainApp()
    win.show()
    app.exec()
