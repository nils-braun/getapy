from unittest import TestCase

from getapy import parse
from getapy.basetypes import StrictParseObject, String, List, Int, PageableObject, Float, GreedyStringParseObject


class User(StrictParseObject):
    name = String()


class House(StrictParseObject):
    street = String()
    number = Int()
    members = List(User())
    height = Float()

class Tool(GreedyStringParseObject):
    id = Int()
    name = String()


class TestBase(TestCase):
    def test_dict(self):
        s = """
            { 
                "street": "Test Street",
                "number": 42,
                "height": 10.34,
                "unused_parameter": "stuff",
                "members": [
                    { "name": "Alice" },
                    { "name": "Bob" }
                ]
            }
        """

        import json
        d = json.loads(s)

        parsed = parse(d, House)

        self.assertEqual(parsed.street, "Test Street")
        self.assertEqual(parsed.number, 42)
        self.assertEqual(parsed.height, 10.34)
        self.assertEqual(parsed.members[0].name, "Alice")
        self.assertEqual(parsed.members[1].name, "Bob")

        self.assertRaises(AttributeError, lambda: parsed.unused_parameter)

        self.assertIsInstance(parsed, House)
        self.assertIsInstance(parsed.members, list)
        self.assertIsInstance(parsed.number, int)
        self.assertIsInstance(parsed.height, float)
        self.assertIsInstance(parsed.street, str)
        self.assertIsInstance(parsed.members[0], User)

    def test_pageable(self):
        s = """
            { 
                "items": [
                    { "name": "Alice" },
                    { "name": "Bob" }
                ],
                "next": "www.example.org/next",
                "href": "www.example.org/current"
            }
        """

        import json
        d = json.loads(s)

        parsed = parse(d, PageableObject(User))

        self.assertEqual(parsed.next, "www.example.org/next")
        self.assertEqual(parsed.href, "www.example.org/current")
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0].name, "Alice")
        self.assertEqual(parsed[1].name, "Bob")

        for user in parsed:
            self.assertIsInstance(user, User)

    def test_greedy(self):
        s = """
            [
                { "name": "hammer", "id": 0, "weight": "0.5kg" },
                { "name": "pincer", "id": 1, "size": "20cm" }
            ]
        """

        import json
        d = json.loads(s)

        parsed = parse(d, List(Tool))

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0].name, "hammer")
        self.assertEqual(parsed[0].id, 0)
        self.assertEqual(parsed[0].weight, "0.5kg")

        self.assertEqual(parsed[1].name, "pincer")
        self.assertEqual(parsed[1].id, 1)
        self.assertEqual(parsed[1].size, "20cm")

        self.assertRaises(AttributeError, lambda: parsed[0].size)
        self.assertRaises(AttributeError, lambda: parsed[1].weight)