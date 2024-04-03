from __future__ import annotations
class Validation():
    _required: bool
    _min: int|float
    _max: int|float

    def __init__(self, required: bool = False, min: int = None, max: int = None):
        self.required = required
        self.min = min
        self.max = max
        pass

    def check(self, field: str, mongol: object):
        data:any = mongol.__getattribute__(field)
        if self.required and not data:
            mongol.error = field, "can't be null"

        if type(data) is str:
            if self.min and self.min > len(data): mongol.error = field, f"string size needed be greater than or iqual {self.min}"
            elif self.max and self.max < len(data): mongol.error = field, f"string size needed be less than or iqual {self.max}"
        elif type(data) is int or type(data) is float:
            if self.min and self.min > data: mongol.error = field, f"needed be greater than or iqual {self.min}"
            elif self.max and self.max < data: mongol.error = field, f"needed be less than or iqual {self.max}"

class DataValidation():
    def validateFieldsType(self):
        for field in self.fields:
            _field = self.__getattribute__(field)
            if self.fieldTypes[field][0] == "Reference": continue
            if _field and type(_field).__name__ != self.__annotations__[field]:
                self.error = field, f"{field} request a \"{self.__annotations__[field]}\" value type"
        for validationDict in self._validation_vars:
            for key, validation in validationDict.items():
                validation.check(key, self)

    def runValidations(self):
        self._errors = {}
        self.validateFieldsType()
        for validation in self._validations:
            validation()
        pass

    def registerValidation(self, field: str):
        if self.__getattribute__(field):
            self._validation_vars.append({field: self.__getattribute__(field)})

    @property
    def errors(self) -> dict:
        return self._errors

    @errors.setter
    def error(self, error: dict):
        if not type(error) is list and not type(error) is tuple:
            raise "Error value require a list type"

        self.errors.update({error[0]: error[1]})
        return self.error