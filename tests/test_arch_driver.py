import unittest
from unittest.mock import patch, MagicMock
from aurora.drivers.arch import Archlinux
from aurora.drivers.ubuntu import Ubuntu

class BaseDriverTest:
    """Base tests for all Driver implementations."""

    driver_class = None  # Set this in subclasses

    def setUp(self):
        self.driver = self.driver_class()

    def test_check_updates_returns_string(self):
        # We mock subprocess.run to avoid real commands
        from unittest.mock import patch, MagicMock
        with patch("aurora.drivers.arch.subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "pkg1\npkg2\npkg3\n"
            mock_run.return_value = mock_result

            updates = self.driver.check_updates()
            assert updates == "3"

    def test_check_updates_raises_on_error(self):
        from unittest.mock import patch, MagicMock
        with patch("aurora.drivers.arch.subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_run.return_value = mock_result

            import unittest
            with unittest.TestCase().assertRaises(self.driver.Error):
                self.driver.check_updates()

    #TODO
    def test_check_dependencies(self):
        pass
        
                
class TestArchlinuxDriver(BaseDriverTest, unittest.TestCase):
    driver_class = Archlinux

class TestUbuntuDriver(BaseDriverTest, unittest.TestCase):
    driver_class = Ubuntu

    
if __name__ == "__main__":
    unittest.main()
