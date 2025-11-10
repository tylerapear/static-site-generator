import unittest

from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_tile(self):
        markdown = "one line\n# uh Hello\nthis a new line"
        self.assertEqual(extract_title(markdown), "uh Hello")