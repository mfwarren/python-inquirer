# -*- coding: utf-8 -*-
import json

from . import errors


def question_factory(kind, *args, **kwargs):
    for clazz in (Text, Password, Confirm, List, Checkbox):
        if clazz.kind == kind:
            return clazz(*args, **kwargs)
    raise errors.UnknownQuestionTypeError()


def load_from_dict(question_dict):
    return question_factory(**question_dict)


def load_from_json(question_json):
    return question_factory(**json.loads(question_json))


class Question(object):
    kind = 'base question'

    def __init__(self,
                 name,
                 message='',
                 choices=None,
                 default=None,
                 ignore=False,
                 validate=True):
        self.name = name
        self._message = message
        self._choices = choices or []
        self._default = default
        self._ignore = ignore
        self._validate = validate
        self.answers = {}

    @property
    def ignore(self):
        return bool(self._solve(self._ignore))

    @property
    def message(self):
        return self._solve(self._message)

    @property
    def default(self):
        return self._solve(self._default)

    @property
    def choices(self):
        return self._solve(self._choices)

    def validate(self, current):
        try:
            if self._solve(self._validate, current):
                return
        except Exception:
            pass
        raise errors.ValidationError(current)

    def _solve(self, prop, *args, **kwargs):
        if callable(prop):
            return prop(self.answers, *args, **kwargs)
        if isinstance(prop, str):
            return prop.format(**self.answers)
        return prop


class Text(Question):
    kind = 'text'


class Password(Question):
    kind = 'password'


class Confirm(Question):
    kind = 'confirm'

    def __init__(self, name, default=False, **kwargs):
        super(Confirm, self).__init__(name, default=default, **kwargs)


class List(Question):
    kind = 'list'


class Checkbox(Question):
    kind = 'checkbox'
