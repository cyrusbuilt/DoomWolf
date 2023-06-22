import copy


def copy_method(method):
    def _inner(self, *args, **kwargs):
        clone = copy.copy(self)
        method(clone, *args, **kwargs)
        return clone

    return _inner
