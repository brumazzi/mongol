class MongolField(dict):
    fields: dict[str|dict] = dict()

    beforeSave: list[any] = []
    afterSave: list[any] = []

    def initFields(self):
        for field in self.fields.keys():
            if type(self.fields.get(field)) == dict:
                self[field] = self.fields.get(field).get("default")
            else:
                self[field] = self.fields.get(field)

    def finalData(self):
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
                data[key] = self[key]
        return data

    def populate(self, **kwds):
        for key in kwds:
            self[key] = kwds[key]