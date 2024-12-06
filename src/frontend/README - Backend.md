# Backend integration

## Backend object

```python
class Backend(QObject):
    pass
```

## Adding parameters

### Python

```python
paramNameChanged = Signal()

def __init__(self):
    super().__init__()
    self._param_name = ""

@Property(param_type, notify=paramNameChanged)
def paramName(self):
    return self._param_name

@paramName.setter
def paramName(self, value):
    if self._param_name != value:
        self._param_name = value
        self.paramNameChanged.emit()
```

Signal allows for dynamic changes in UI.

### QML

```qml
backend.paramName // getter
backend.paramName = value // setter
```

## Adding methods

### Python

```python
@Slot()
def method_name(self, param):
    pass
```

### QML

```qml
param = backend.method_name(arg1) // return value
onChanged: {
    backend.method_name(arg1) // void
}
```

## Integration

### Example

```qml
RoundButton_ {
    id: buttonRun
    icon.source: "../icons/run.png"
    icon.width: RoundButtonConst.headerImageRadius
    icon.height: RoundButtonConst.headerImageRadius
    background: null
    onClicked: {
        switch (optionBuildMode.currentText) {
            case LangConst.comboBoxPointCloud:
                backend.generatePointCloud()
                break;
            case LangConst.comboBoxSplats:
                backend.generateSplats()
                break;
            case LangConst.comboBoxCategorization:
                backend.categorize()
                break;
        }
        loadingWindow.open()
    }
}
```