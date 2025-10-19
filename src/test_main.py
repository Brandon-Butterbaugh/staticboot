import unittest
from extract_title import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Tolkien Fan Club
"""
        heading = extract_title(md)
        self.assertEqual(
            heading,
            "Tolkien Fan Club"
        )


if __name__ == "__main__":
    unittest.main()