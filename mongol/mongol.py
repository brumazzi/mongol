from pymongo import MongoClient
import inflection

class Mongol(object):
    _id: str = None
    validation_errors: dict = dict()

    # Set field to use in project with validations
    # fields = {
    #     "name": {"type": str, "max": 10, "min": 5, "default": "Peixe"},
    #     "age": {"type": int, "default": 18, "max": 16, "min": 10},
    #     "comment": {"type": str, "presence": True}
    # }

    def __init__(self, **kwds):
        if not hasattr(self.__class__, "table"): self.__sync()

        self.__prepare_fields()
        self.__populate(**kwds)

    @classmethod
    def find(self, **query):
        if not hasattr(self.__class__, "table"): self.__sync_class()
        registers = list()
        for data in self.table.find(query):
            registers.append(self(**data))
        return registers

    @classmethod
    def find_one(self, **query):
        if not hasattr(self.__class__, "table"): self.__sync_class()
        return self(**self.table.find_one(query))

    def destroy(self):
        return self.table.delete_one({"_id": self._id})

    @classmethod
    def destroy_many(self, **query):
        if not hasattr(self.__class__, "table"): self.__sync_class()
        return self.table.delete_many(query)

    def save(self, validation: str = True) -> bool:
        if validation != False and not self.__validate_fields():
            return False
        data_dict = dict()
        for field in self.fields:
            data_dict.setdefault(field, self.__getattribute__(field))
        self.id = self.table.insert_one(data_dict).inserted_id
        return True

    def errors(self) -> dict:
        return self.validation_errors

    def is_valid(self) -> bool:
        return self.__validate_fields()

    @classmethod
    def __sync_class(self):
        self.connection = Mongol.connection
        if not hasattr(self, "table_name"):
            self.table_name = inflection.pluralize(inflection.underscore(self.__name__))
        self.collection = self.connection[Mongol.collection]
        self.table = self.collection[self.table_name]

    def __sync(self):
        self.connection = Mongol.connection
        if not hasattr(self, "table_name"):
            self.table_name = inflection.pluralize(inflection.underscore(self.__class__.__name__))
        self.collection = self.connection[Mongol.collection]
        self.table = self.collection[self.table_name]

    def __prepare_fields(self):
        for field in self.fields:
            type = self.fields.get(field)
            default = None
            if type.__class__ == dict:
                default = type.get("default")
                if default and type.get("type") and default.__class__ != type.get("type"):
                    raise ValueError(f"\"{default.__class__.__name__}({default})\" is not a valid {type.get('type').__name__}")
            self.__setattr__(field, default)
        pass

    def __populate(self, **kwds):
        for key in kwds:
            self.__setattr__(key, kwds[key])

    def __validate_fields(self):
        is_valid = True
        for field in self.fields:
            tmp_valid = self.__validate_field(field, self.fields[field])
            if is_valid: is_valid = tmp_valid

        return is_valid

    def __validate_field(self, field: str, value):
        if value.__class__ == dict and value["type"]:
            value_field = self.__getattribute__(field)
            value_max = value.get('max')
            value_min = value.get('min')
            value_presence = value.get('presence')
            value_unique = value.get('unique')

            validation_errors = {}
            validation_errors.setdefault(field, [])
            if value_presence and value_field == None:
                validation_errors[field].append(f"Can't be null!")
            if value_unique == True:
                query = { field: f"{self.__getattribute__(field)}" }
                if len(self.__class__.find(**query)) > 0:
                    validation_errors[field].append(f'"{self.__getattribute__(field)}" is already being used!')
                pass
            if value_field:
                try:
                    if value_field.__class__ != value["type"]:
                        validation_errors[field].append(f"\"{value_field.__class__.__name__}({value_field})\" is not a valid {value.get('type')}!")
                    if value["type"] == int:
                        if value_max and value_field > value_max:
                            validation_errors[field].append(f"Can't be bigger than {value_max}!")
                        if value_min and value_field < value_min:
                            validation_errors[field].append(f"Can't be lower than {value_min}!")
                    elif value["type"] == str:
                        if value_max and len(value_field) > value_max:
                            validation_errors[field].append(f"Can't be bigger than {value_max} characters!")
                        if value_min and len(value_field) < value_min:
                            validation_errors[field].append(f"Can't be lower than {value_min} characters!")
                        pass
                except: pass

        for field in validation_errors:
            if len(validation_errors[field]) > 0:
                self.validation_errors = validation_errors
                return False
        return True

    def __repr__(self):
        output = f"<{self.__class__.__name__}"
        for field in self.fields:
            output += f" @{field}='{self.__getattribute__(field)}'"
        output += ">"
        return output

def listen(host: str = "localhost", port: int = 27017):
    Mongol.connection = MongoClient(host, port)
Mongol.listen = listen