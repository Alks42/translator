import sys
import webbrowser
import translator as tr
from PyQt6 import QtGui, QtCore, QtWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, x: int, y: int):
        super(MainWindow, self).__init__()
        self.resize(x, y)
        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, x, y))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Translator')
        # self.setWindowIcon(QtGui.QIcon('lsa.ico'))
        self.setAutoFillBackground(True)
        self.setCentralWidget(self.gridLayoutWidget)
        with open('style.css') as f:
            self.setStyleSheet(f.read())


class Settings(MainWindow):
    def __init__(self):
        super(Settings, self).__init__(400, 300)
        self.setFixedSize(300, 250)
        for x, i in enumerate(tr.options.items()):
            label = QtWidgets.QLabel(self.gridLayoutWidget)
            label.setText(f"   {i[0]}    ")
            self.gridLayout.addWidget(label, x, 0, 1, 1)
            if x <= 1:
                line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
                line_edit.setText(i[1])
                self.gridLayout.addWidget(line_edit, x, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
            elif x == 2:
                combo_box = QtWidgets.QComboBox(self.gridLayoutWidget)
                combo_box.addItems(['never', 'always'])
                combo_box.setPlaceholderText(i[1])
                self.gridLayout.addWidget(combo_box, x, 1, 1, 1)
            elif x <= 6:
                check_box = QtWidgets.QCheckBox(self.gridLayoutWidget)
                check_box.setChecked(i[1])
                self.gridLayout.addWidget(check_box, x, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                spin_box = QtWidgets.QSpinBox(self.gridLayoutWidget)
                spin_box.setMinimum(0)
                spin_box.setValue(i[1])
                self.gridLayout.addWidget(spin_box, x, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.ok_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ok_button.clicked.connect(self.save_settings)
        self.ok_button.setObjectName('ok')
        self.ok_button.setText('Ok')
        self.gridLayout.addWidget(self.ok_button, 11, 0, 1, 1)

        self.cansel_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.cansel_button.clicked.connect(lambda: self.close())
        self.cansel_button.setObjectName('cansel')
        self.cansel_button.setText('Cansel')
        self.gridLayout.addWidget(self.cansel_button, 11, 1, 1, 1)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setFocus()

    def save_settings(self):
        for x in range(1, self.gridLayout.count() - 2, 2):
            i = list(tr.options.items())[x // 2][0]
            w = self.gridLayout.itemAt(x).widget()
            if x <= 3:
                v = w.text()
            elif x == 5:
                v = w.currentText()
            elif x <= 13:
                v = w.isChecked()
            else:
                v = int(w.value())
            tr.options[i] = v
        tr.save_settings(tr.options)
        ui.populate_table()
        self.close()


class Ui_MainWindow(MainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__(800, 600)
        ###################################################################################
        # menu bar
        self.menu_bar = self.menuBar()

        self.menu_add = QtGui.QAction()
        self.menu_add.setText('Translate')
        self.menu_add.triggered.connect(self.show_frame)

        self.menu_collapse = QtGui.QAction()
        self.menu_collapse.setText('Collapse all')
        self.menu_collapse.triggered.connect(self.populate_table)

        self.menu_hide_left = QtGui.QAction()
        self.menu_hide_left.setText('Hide left')
        self.menu_hide_left.triggered.connect(lambda: self.hide_part('left', self.menu_hide_left))

        self.menu_hide_right = QtGui.QAction()
        self.menu_hide_right.setText('Hide right')
        self.menu_hide_right.triggered.connect(lambda: self.hide_part('right', self.menu_hide_right))

        self.settings = QtGui.QAction()
        self.settings.setText('Settings')
        self.open_settings = Settings()
        self.settings.triggered.connect(lambda: self.open_settings.show())

        self.help = QtGui.QAction()
        self.help.setText('Help')
        self.help.triggered.connect(lambda: webbrowser.open('https://github.com/Alks42'))

        self.menu_bar.addAction(self.menu_add)
        self.menu_bar.addAction(self.menu_collapse)
        self.menu_bar.addAction(self.menu_hide_left)
        self.menu_bar.addAction(self.menu_hide_right)
        self.menu_bar.addAction(self.settings)
        self.menu_bar.addAction(self.help)
        ###################################################################################
        # table with translations
        self.table_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.table_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom, self.table_frame)
        self.table_layout.setSpacing(0)
        self.table_layout.setContentsMargins(0, 0, 0, 0)
        self.table = QtWidgets.QTableWidget(self.table_frame)
        self.setup_table()
        self.table_layout.addWidget(self.table)
        self.populate_table()

        self.invisible_label = QtWidgets.QLabel(self.table_frame)
        self.invisible_label.setObjectName('invis')
        self.table_layout.addWidget(self.invisible_label)
        self.invisible_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)

        self.gridLayout.addWidget(self.table_frame, 0, 0, 1, 1)
        ###################################################################################
        # translation window
        self.tr_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.tr_frame.setFixedHeight(300)
        self.tr_layout = QtWidgets.QGridLayout(self.tr_frame)
        self.tr_layout.setSpacing(0)
        self.tr_layout.setContentsMargins(0, 0, 0, 0)
        self.tr_form = QtWidgets.QLineEdit(self.tr_frame)
        self.tr_form.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)

        self.tr_button = QtWidgets.QPushButton(self.tr_frame)
        self.process = Translate()
        self.tr_button.clicked.connect(lambda: self.translate() if self.tr_form.text() else None)
        self.tr_button.setObjectName('translate')
        self.tr_button.setText('Translate')

        self.tr_button_add = QtWidgets.QPushButton(self.tr_frame)
        self.translation = {}
        self.tr_button_add.clicked.connect(lambda: self.add_word(self.translation) if self.translation else None)
        self.tr_button_add.setObjectName('add_word')
        self.tr_button_add.setText('Add word')

        self.tr_button_edit = QtWidgets.QPushButton(self.tr_frame)
        self.edit = False
        self.tr_button_edit.clicked.connect(self.edit_word)
        self.tr_button_edit.setObjectName('edit')
        self.tr_button_edit.setText('Edit word')

        self.tr_scroll_area = QtWidgets.QScrollArea()
        self.tr_scroll_frame = QtWidgets.QFrame()
        self.tr_scroll_layout = QtWidgets.QGridLayout()

        self.tr_scroll_frame.setLayout(self.tr_scroll_layout)

        self.tr_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tr_scroll_area.setWidgetResizable(True)
        self.tr_scroll_area.setWidget(self.tr_scroll_frame)
        self.tr_scroll_area.setStyleSheet('background: white')

        self.tr_layout.addWidget(self.tr_form, 0, 0, 1, 5)
        self.tr_layout.addWidget(self.tr_button, 0, 5, 1, 1)
        self.tr_layout.addWidget(self.tr_scroll_area, 1, 0, 1, 6)
        self.tr_layout.addWidget(self.tr_button_add, 2, 0, 1, 3)
        self.tr_layout.addWidget(self.tr_button_edit, 2, 3, 1, 3)

        self.gridLayout.addWidget(self.tr_frame, 1, 0, 1, 1)
        ###################################################################################
        # shortcuts
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Up), self, lambda: self.manipulate_row('up'))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Down), self, lambda: self.manipulate_row('down'))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Delete), self, lambda: self.manipulate_row('delete'))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_F1), self, lambda: self.manipulate_row('select'))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Escape), self, lambda: self.manipulate_row('diselect'))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Return), self, lambda: self.manipulate_row('expand'))
        self.table.itemDoubleClicked.connect(lambda: self.manipulate_row('expand'))
        self.table.itemClicked.connect(self.table.setFocus)

        self.tr_frame.hide()
        self.table.setContentsMargins(0, 0, 0, 0)

    def setup_table(self):
        self.table.setColumnCount(2)
        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(["Word", "Translation"])

        self.table.setShowGrid(False)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.verticalScrollBar().setSingleStep(10)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)

    def populate_table(self):
        self.words = tr.get_words()
        self.menu_hide_right.setText("Hide right")
        self.menu_hide_left.setText("Hide left")
        # sorting often will break align
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.words))

        for row, key in enumerate(self.words):
            translation = ', '.join(self.words[key]['translation'][:tr.max_display])
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(translation))
            self.table.item(row, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.table.verticalHeader().setSectionResizeMode(row, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.table.selectRow(0)
        self.table.setFocus()
        self.table.setSortingEnabled(True)

    def translate(self):
        self.process.start()
        self.process.update.connect(self.update_tr_window)

    def update_tr_window(self, translation):
        def populate_layout(separator, string, indx, h):
            label_name = QtWidgets.QLabel()
            label_name.setObjectName('meaning')
            label_name.setText(separator)
            label_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            self.tr_scroll_layout.addWidget(label_name, indx, 0, 1, 1)

            text = QtWidgets.QTextEdit()
            text.setPlainText(string)
            text.setReadOnly(True)
            text.setStyleSheet("border: 0px solid white")
            text.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

            font_metrics = QtGui.QFontMetrics(QtGui.QFont('Times New Roman', 16))
            height = font_metrics.size(0, string).height()
            text.setFixedHeight(height + h)

            text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.tr_scroll_layout.addWidget(text, indx, 1, 1, 1)

        # clear layout
        while self.tr_scroll_layout.itemAt(0):
            self.tr_scroll_layout.itemAt(0).widget().setParent(None)
        self.manipulate_row('diselect')

        self.translation = translation
        self.edit = False
        display = list(self.translation.values())[0]
        x = 0
        for key in display:
            if display[key]:
                label = QtWidgets.QLabel()
                label.setObjectName('translation')
                label.setText(key.capitalize() + ':')
                label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
                self.tr_scroll_layout.addWidget(label, x, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignTop)

                if key != 'meanings':
                    string = ', '.join(display[key])
                    populate_layout('\t', string, x + 1, 15 if len(string) < 109 else 70)
                else:
                    for k, meanings in display['meanings'].items():
                        if display['meanings'][k]:
                            populate_layout(f'   {k}:', '\n'.join(meanings), x + 1, 20)
                            x += 1
                x += 2
        invis_label = QtWidgets.QLabel()
        invis_label.setMinimumHeight(0)
        invis_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.tr_scroll_layout.addWidget(invis_label, x, 1, 1, 2)

    def add_word(self, translation):
        if self.edit:
            word = list(translation.keys())[0]
            for i in range(self.tr_scroll_layout.rowCount()):
                if self.tr_scroll_layout.itemAtPosition(i, 0):
                    try:
                        key = self.tr_scroll_layout.itemAtPosition(i, 0).widget().text()[:-1].strip()
                        if key != 'Meanings' and not key.islower():
                            w = self.tr_scroll_layout.itemAtPosition(i + 1, 1).widget().toPlainText().strip().lower()
                            translation[word][key.lower()] = w.split(', ') if w else []
                        elif key == 'Meanings':
                            translation[word]['meanings'] = {}
                        else:
                            w = self.tr_scroll_layout.itemAtPosition(i, 1).widget().toPlainText().strip()
                            translation[word]['meanings'][key] = w.split('\n') if w else []
                    except AttributeError:
                        pass
        r = tr.add_word(translation)
        if r:
            self.populate_table()
        else:
            QtWidgets.QMessageBox.information(self, "Already in", 'Word is already added.',
                                              QtWidgets.QMessageBox.StandardButton.Ok)
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).text() == list(translation.keys())[0]: self.table.selectRow(i)

    def edit_word(self):
        for i in range(self.tr_scroll_layout.rowCount()):
            try:
                w = self.tr_scroll_layout.itemAtPosition(i, 1).widget()
                w.setReadOnly(False)
                w.setStyleSheet("border: 2px solid black")
            except AttributeError:
                pass
        self.edit = True

    def hide_part(self, part, button):
        def hide_show(x, color, button, string):
            [self.table.item(i, x).setForeground(QtGui.QColor.fromString(color)) for i in range(self.table.rowCount())]
            button.setText(string)

        self.table.clearSelection()
        if button.text() == f'Hide {part}':
            hide_show(0 if part == 'left' else 1, 'white', button, f'Show {part}')
        else:
            hide_show(0 if part == 'left' else 1, 'black', button, f'Hide {part}')

    def manipulate_row(self, command):
        if command == 'up':
            self.table.selectRow(self.table.currentIndex().row() - 1)
        elif command == 'down':
            self.table.selectRow(self.table.currentIndex().row() + 1)
        elif command == 'delete':
            if self.table.item(self.table.currentRow(), 0) and self.table.hasFocus():
                for i in self.table.selectionModel().selectedRows():
                    word = self.table.item(i.row(), 0)
                    if word:
                        tr.delete_word(word.text())
                        self.table.hideRow(i.row())
                self.table.clearSelection()
        elif command == 'select':
            self.table.selectAll()
        elif command == 'diselect':
            self.table.clearSelection()
        else:
            if self.table.item(self.table.currentRow(), 0) and self.table.hasFocus():
                self.table.setSortingEnabled(False)
                for i in self.table.selectionModel().selectedRows():
                    p = self.words[self.table.item(i.row(), 0).text()]
                    new_string = ''
                    if not self.table.item(i.row(), 1).text().startswith('Translation:'):
                        for key in p:
                            if p[key]:
                                if key != 'meanings':
                                    new_string += f"{key.capitalize()}:\n{', '.join(p[key])}\n\n"
                                else:
                                    new_string += f"Meanings:\n"
                                    for k, meanings in p['meanings'].items():
                                        if meanings: new_string += f"{k}:\n" + '\n'.join(meanings) + "\n\n"

                    else:
                        new_string = ', '.join(p['translation'][:tr.max_display]) + '\n\n'
                    self.table.setItem(i.row(), 1, QtWidgets.QTableWidgetItem(new_string[:-2]))
                    self.table.item(i.row(), 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.table.verticalHeader().setSectionResizeMode(i.row(),
                                                                     QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                self.table.setSortingEnabled(True)

    def show_frame(self):
        if self.tr_frame.isHidden():
            self.tr_frame.show()
        else:
            self.tr_frame.hide()

    def closeEvent(self, event):
        app.exit()


class Translate(QtCore.QThread):
    update = QtCore.pyqtSignal(object)

    def run(self):
        if tr.connection():
            self.update.emit({ui.tr_form.text().lower(): tr.translate(ui.tr_form.text().lower())})


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec())
