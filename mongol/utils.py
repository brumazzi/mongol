from __future__ import annotations
from sys import modules
from inflection import tableize
import re

def classFromModule(classModuleRef: str):
    moduleName = re.sub("\\.\\w+$", "", classModuleRef)
    className = classModuleRef[len(moduleName)+1:]

    return modules[moduleName].__getattribute__(className)

def collectionFromModule(classModuleRef: str):
    moduleName = re.sub("\\.\\w+$", "", classModuleRef)
    return tableize(moduleName)