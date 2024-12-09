import os
from ..models.basic_model import BasicModelBool, BasicModelList

class ParametersHandler:
    def __init__(self):
        self._is_parameters_open = BasicModelBool()
        self._status = BasicModelBool()
        self._params = BasicModelList()
    
    @property
    def is_parameters_open(self):
        return self._is_parameters_open

    @property
    def status(self):
        return self._status
    
    @property
    def params(self):
        return self._params

    def configure_open_handler(self, func):
        self.is_parameters_open.dataChanged.connect(lambda: self._handle_open(func))
    
    def configure_status_handler(self, func):
        self.status.dataChanged.connect(lambda: self._handle_status(func))

    def _handle_open(self, func):
        if self.is_parameters_open.data:
            self.is_parameters_open.data = False
            func()
        
    def _handle_status(self, func):
        if self.status.data:
            for entry in self.params.data:
                print(entry)
                # env_name = entry["label"]
                # env_value = entry["input"]
                # os.environ[env_name] = env_value
            print(f"HERE {self.params.data}")
            self.status.data = False
            func()
    
    def configure_env_var(self, name, value):
        curr_env_vars = self.env_vars.data
        curr_env_vars.append({"label": name, "input": value})
        self.env_vars.data = curr_env_vars