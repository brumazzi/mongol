VALIDATE_ROLES_REQUIRED = "required"
VALIDATE_ROLES_TYPE     = "type"
VALIDATE_ROLES_UNIQUE   = "unique"
VALIDATE_ROLES_FORMAT   = "format"
VALIDATE_ROLES_MAX      = "max"
VALIDATE_ROLES_MIN      = "min"

import hashlib

class MongolValidate():
    roles: list[str] = [VALIDATE_ROLES_REQUIRED, VALIDATE_ROLES_TYPE, VALIDATE_ROLES_UNIQUE, VALIDATE_ROLES_FORMAT, VALIDATE_ROLES_MAX, VALIDATE_ROLES_MIN]
    validates: list[dict] = list()
    errors: dict[dict] = dict()

    def validate(self) -> bool:
        is_valid = True
        self.errors.clear()
        for validate in self.validates:
            tmp_valid = True
            if not "role" in validate: continue
            if not validate.get("role") in self.roles: continue

            field = validate.get("field")
            role = validate.get("role")
            roleValue = validate.get("roleValue")
            ifValidation = True
            if "if" in validate:
                ifValidation = eval(validate.get("if"))

            if role == VALIDATE_ROLES_TYPE and ifValidation:
                if type(self[field]) != roleValue: tmp_valid = False
            elif role == VALIDATE_ROLES_REQUIRED and ifValidation:
                if roleValue != True: continue
                if self[field] == "" or self[field] == None: tmp_valid = False
            elif role == VALIDATE_ROLES_UNIQUE and ifValidation:
                pass
            elif role == VALIDATE_ROLES_FORMAT and ifValidation:
                pass
            elif role == VALIDATE_ROLES_MAX and ifValidation:
                if type(self[field]) == str and len(self[field]) > roleValue: tmp_valid = False
                elif type(self[field]) == int or type(self[field]) == float:
                    if self[field] > roleValue: tmp_valid = False
            elif role == VALIDATE_ROLES_MIN and ifValidation:
                if type(self[field]) == str and len(self[field]) < roleValue: tmp_valid = False
                elif type(self[field]) == int or type(self[field]) == float:
                    if self[field] < roleValue: tmp_valid = False

            if not tmp_valid:
                self.addValidateError(role, field, self[field], roleValue)
                is_valid = tmp_valid

        return is_valid

    def addValidateError(self, role: str, field: str, fieldValue: any, roleValue: any):
        errorMessage = None

        if role == VALIDATE_ROLES_REQUIRED:
            errorMessage = f"can't be null or blank"
        elif role == VALIDATE_ROLES_UNIQUE:
            errorMessage = f'"{fieldValue}" is already being used'
        elif role == VALIDATE_ROLES_TYPE:
            errorMessage = f'require a "{roleValue}" type'
        elif role == VALIDATE_ROLES_MIN:
            errorMessage = f'can\'t be less than {roleValue}'
        elif role == VALIDATE_ROLES_MAX:
            errorMessage = f'can\'t be greater than {roleValue}'
        elif role == VALIDATE_ROLES_FORMAT:
            errorMessage = f'format not match'

        if not errorMessage: return None


        if field in self.errors:
            self.errors[field].append(errorMessage)
        else:
            self.errors[field] = [errorMessage]
        pass

    def isValid(self) -> bool:
        return self.validate()