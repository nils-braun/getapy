class BaseParseObject:
    @classmethod
    def construct_from_json(cls, json):
        return cls()


class String(BaseParseObject):
    @classmethod
    def construct_from_json(cls, json):
        return json


class Int(BaseParseObject):
    @classmethod
    def construct_from_json(cls, json):
        return int(json)


class Float(BaseParseObject):
    @classmethod
    def construct_from_json(cls, json):
        return float(json)


class StrictParseObject(BaseParseObject):
    @classmethod
    def construct_from_json(cls, json):
        instance = super().construct_from_json(json)

        for key, value in json.items():
            if hasattr(cls, key):
                instance.__dict__[key] = getattr(cls, key).construct_from_json(value)

        return instance


class GreedyStringParseObject(StrictParseObject):
    @classmethod
    def construct_from_json(cls, json):
        instance = super().construct_from_json(json)

        for key, value in json.items():
            if not hasattr(cls, key):
                instance.__dict__[key] = String.construct_from_json(value)

        return instance


def List(subclass_type):
    class ListInstance(BaseParseObject, list):
        subclass = subclass_type

        @classmethod
        def construct_from_json(cls, json):
            instance = super().construct_from_json(json)
            for item in json:
                instance.append(cls.subclass.construct_from_json(item))

            return instance

    return ListInstance


def PageableObject(subclass_type):
    class PageableObjectInstance(GreedyStringParseObject):
        items = List(subclass_type)

        def __iter__(self):
            return iter(self.items)

        def __len__(self):
            return len(self.items)

        def __getitem__(self, item):
            return self.items[item]

    return PageableObjectInstance
