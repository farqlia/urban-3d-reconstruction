from ..models.basic_model import BasicModelInt

class TabHandler:
    def __init__(self):
        self._selected_tab = BasicModelInt()

    @property
    def selected_tab(self):
        return self._selected_tab