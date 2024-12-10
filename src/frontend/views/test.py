from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QStyledItemDelegate,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem


class CustomDelegate(QStyledItemDelegate):
    """Custom delegate to handle widget rendering for each ListView row."""
    
    def createEditor(self, parent, option, index):
        # Create a custom widget with a label and input field
        container = QWidget(parent)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(f"Item {index.row() + 1}:", container)
        input_field = QLineEdit(container)
        input_field.setPlaceholderText("Enter value")

        # Attach the layout to the container
        layout.addWidget(label)
        layout.addWidget(input_field)

        # Store the input field for later access
        container.input_field = input_field
        return container

    def setEditorData(self, editor, index):
        # Set existing data (if any) to the input field
        value = index.data(Qt.ItemDataRole.DisplayRole)
        editor.input_field.setText(value or "")

    def setModelData(self, editor, model, index):
        # Save the input field's value back to the model
        value = editor.input_field.text()
        model.setData(index, value, Qt.ItemDataRole.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ListViewWidget(QWidget):
    """Main widget containing the ListView."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ListView with Label and Input")

        # Layout for the main widget
        layout = QVBoxLayout(self)
        
        # Add a ListView
        self.list_view = QListView(self)
        self.model = QStandardItemModel(self.list_view)
        self.list_view.setModel(self.model)

        # Use the custom delegate for the ListView
        self.delegate = CustomDelegate()
        self.list_view.setItemDelegate(self.delegate)
        layout.addWidget(self.list_view)

        # Add button to add new items
        add_button = QPushButton("Add Item", self)
        add_button.clicked.connect(self.add_item)
        layout.addWidget(add_button)

        # Add button to print all stored values
        print_button = QPushButton("Print Values", self)
        print_button.clicked.connect(self.print_values)
        layout.addWidget(print_button)

    def add_item(self):
        # Add a new row to the model
        item = QStandardItem("")
        self.model.appendRow(item)

    def print_values(self):
        # Print all values stored in the model
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            print(f"Row {row + 1}: {item.text()}")


if __name__ == "__main__":
    app = QApplication([])
    widget = ListViewWidget()
    widget.resize(400, 300)
    widget.show()
    app.exec()
