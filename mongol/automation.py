from __future__ import annotations
import re

def run_before_after(action: str):
    def layer(callback):
        def callable(self, *args, **kwds):
            for beforeCallback in self.__getattribute__(f"_before_{action}s"):
                beforeCallback()
            response = callback(self, *args, **kwds)
            if not response: return response
            for afterCallback in self.__getattribute__(f"_after_{action}s"):
                afterCallback()
            return response
        return callable
    return layer

class Automation:
    def syncMethods(self):
        self.syncBeforeDeletes()
        self.syncAfterDeletes()
        self.syncBeforeSaves()
        self.syncAfterSaves()
        self.syncBeforeValidates()
        self.syncAfterValidates()
        self.syncValidations()

    def syncBeforeDeletes(self):
        for attr in dir(self):
            if not attr.startswith("sync") and attr.endswith("BeforeDelete") and type(self.__getattribute__(attr)).__name__ == "method":
                self._before_deletes.append(self.__getattribute__(attr))
        pass
    def syncAfterDeletes(self):
        for attr in dir(self):
            if not attr.startswith("sync") and attr.endswith("AfterDelete") and type(self.__getattribute__(attr)).__name__ == "method":
                self._after_deletes.append(self.__getattribute__(attr))
        pass
    def syncBeforeSaves(self):
        for attr in dir(self):
            if not attr.startswith("sync") and attr.endswith("BeforeSave") and type(self.__getattribute__(attr)).__name__ == "method":
                self._before_saves.append(self.__getattribute__(attr))
        pass
    def syncAfterSaves(self):
        for attr in dir(self):
            if not attr.startswith("sync") and attr.endswith("AfterSave") and type(self.__getattribute__(attr)).__name__ == "method":
                self._after_saves.append(self.__getattribute__(attr))
        pass
    def syncBeforeValidates(self):
        for attr in dir(self):
            if not attr.startswith("sync") and attr.endswith("BeforeValidate") and type(self.__getattribute__(attr)).__name__ == "method":
                self._before_validates.append(self.__getattribute__(attr))
        pass
    def syncAfterValidates(self):
        for attr in dir(self):
            if not attr.startswith("sync") and attr.endswith("AfterValidate") and type(self.__getattribute__(attr)).__name__ == "method":
                self._after_validates.append(self.__getattribute__(attr))
        pass
    def syncValidations(self):
        for attr in dir(self):
            if not attr.startswith("sync") and attr.endswith("Validation") and type(self.__getattribute__(attr)).__name__ == "method":
                self._validations.append(self.__getattribute__(attr))
        pass
    pass