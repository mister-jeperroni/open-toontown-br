from panda3d.core import ConfigVariableBool, ConfigVariableString
from importlib import import_module
import sys


class LanguageManager:
    def __init__(self, base_module, default_language="portuguese"):
        self.base_module = base_module
        self.language = ConfigVariableString("language", default_language).value
        self.check_language = ConfigVariableBool("check-language", 0).value
        self._language_module = self._determine_language_module()
        self.module = self._import_language_module()

    def _determine_language_module(self):
        if self.language == "english":
            return f"{self.base_module}{self.language.capitalize()}"
        else:
            self.check_language = 1
            return f"{self.base_module}{self.language.capitalize()}"

    def _import_language_module(self):
        print(f"Localizer: Running in language: {self.language}")
        print(f"from {self._language_module} import *")

        english_module_name = f"{self.base_module}English"
        english_module = import_module(english_module_name)

        try:
            foreign_module = import_module(self._language_module)
        except ModuleNotFoundError:
            print(
                f"WARNING: Language module {self._language_module} not found. Falling back to English."
            )
            foreign_module = english_module

        if self.check_language and foreign_module != english_module:
            self._validate_language_module(english_module, foreign_module)

        self._merge_modules(foreign_module)
        return foreign_module

    def _validate_language_module(self, english_module, foreign_module):
        for key, val in english_module.__dict__.items():
            if key not in foreign_module.__dict__:
                print(
                    f"WARNING: Foreign module: {self._language_module} missing key: {key}"
                )
                setattr(foreign_module, key, val)
            elif isinstance(val, dict):
                fval = foreign_module.__dict__.get(key)
                for dkey, dval in val.items():
                    if dkey not in fval:
                        print(
                            f"WARNING: Foreign module: {self._language_module} missing key: {key}.{dkey}"
                        )
                        fval[dkey] = dval
                for dkey in fval.keys():
                    if dkey not in val:
                        print(
                            f"WARNING: Foreign module: {self._language_module} extra key: {key}.{dkey}"
                        )

        for key in foreign_module.__dict__.keys():
            if key not in english_module.__dict__:
                print(
                    f"WARNING: Foreign module: {self._language_module} extra key: {key}"
                )

    def _merge_modules(self, module):
        sys.modules[self.base_module] = module

    def get_language(self):
        return self.language
