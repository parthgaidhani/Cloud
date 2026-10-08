import unittest

class TestAppImport(unittest.TestCase):
    def test_import(self):
        try:
            import App
        except Exception as e:
            self.fail(f"Importing App failed: {e}")

if __name__ == "__main__":
    unittest.main()