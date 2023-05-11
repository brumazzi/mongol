class MongolData(dict):
    fields: dict[str|dict] = dict()
    __db__: dict[any]

    beforeSave: list[any] = []
    afterSave: list[any] = []

    def initFields(self):
        for field in self.fields.keys():
            if type(self.fields.get(field)) == dict:
                self[field] = self.fields.get(field).get("default")
            else:
                self[field] = self.fields.get(field)

    def dataToSave(self):
        data: dict[any] = dict()
        for key in self.keys():
            fieldDescription = self.fields.get(key)
            if key in self.fields:
                if type(fieldDescription) == dict:
                    try:
                        if not eval(fieldDescription.get("if")):
                            continue
                    except:
                        pass
                if data.get("__db__"):
                    if data.get("__db__").get(key) != self[key]:
                        data[key] = self[key]
                else:
                    data[key] = self[key]
        return data

    def __populate__(self, **kwds):
        if not "_id" in kwds: self.initFields()
        self.__db__ = {}
        for key in kwds:
            if "_id" in kwds and key != "_id": self.__db__[key] = kwds[key]
            self[key] = kwds[key]

    def __update_dict_data__(self, **kwds):
        for key in kwds:
            self.__db__[key] = kwds[key]