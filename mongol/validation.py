from __future__ import annotations

class Validation():
    def validateFieldsType(self):
        for field in self.fields:
            if self.__getattribute__(field) and type(self.__getattribute__(field)).__name__ != self.__annotations__[field]:
                self.error = {field: f"{field} request a \"{self.__annotations__[field]}\" value type"}

    def runValidations(self):
        self._errors = {}
        self.validateFieldsType()
        for validation in self._validations:
            validation()

    @property
    def errors(self) -> dict:
        return self._errors

    @errors.setter
    def error(self, error: dict):
        if not type(error) is dict:
            raise "Error value require a dict type"

        self.errors.update(error)
        return self.error