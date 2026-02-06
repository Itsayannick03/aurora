import unittest
from unittest.mock import patch, MagicMock

from aurora.drivers.ubuntu import Ubuntu


class TestUbuntuDriver(unittest.TestCase):
    def setUp(self):
        self.driver = Ubuntu()

    @patch("aurora.drivers.ubuntu.subprocess.run")
    def test_check_updates_returns_string_count(self, mock_run):
        # apt list --upgradable output includes a "Listing..." header on Ubuntu
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "Listing...\n"
            "python3/jammy-updates 3.10.6-1~22.04.1 amd64 [upgradable from: 3.10.6-1~22.04]\n"
            "vim/jammy-updates 2:8.2.3995-1ubuntu2.12 amd64 [upgradable from: 2:8.2.3995-1ubuntu2.10]\n"
            "\n"
        )
        mock_run.return_value = mock_result

        updates = self.driver.check_updates()
        self.assertEqual(updates, "2")

        mock_run.assert_called_once()
        called_args = mock_run.call_args[0][0]
        self.assertEqual(called_args, ["apt", "list", "--upgradable"])

    @patch("aurora.drivers.ubuntu.subprocess.run")
    def test_check_updates_allows_returncode_2(self, mock_run):
        # apt sometimes returns 2 and still provides valid output
        mock_result = MagicMock()
        mock_result.returncode = 2
        mock_result.stdout = (
            "Listing...\n"
            "pkg1/jammy 1.1 amd64 [upgradable from: 1.0]\n"
        )
        mock_run.return_value = mock_result

        updates = self.driver.check_updates()
        self.assertEqual(updates, "1")

    @patch("aurora.drivers.ubuntu.subprocess.run")
    def test_check_updates_raises_on_error(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        with self.assertRaises(self.driver.Error):
            self.driver.check_updates()

    @patch("aurora.drivers.ubuntu.subprocess.run")
    def test_check_dependencies_reports_missing_and_installs(self, mock_run):
        """
        check_dependencies() calls subprocess.run multiple times:
          - dpkg -s <dep> for each dependency
          - if missing: sudo apt install <dep>
        We simulate:
          python3 OK, apt missing, systemd OK -> should install apt
        """
        def run_side_effect(cmd, *args, **kwargs):
            # cmd is a list like ["dpkg", "-s", "python3"] etc.
            if cmd[:2] == ["dpkg", "-s"]:
                pkg = cmd[2]
                r = MagicMock()
                if pkg == "apt":
                    r.returncode = 1  # missing
                else:
                    r.returncode = 0  # installed
                return r

            if cmd[:3] == ["sudo", "apt", "install"]:
                r = MagicMock()
                r.returncode = 0
                return r

            # default fallback
            r = MagicMock()
            r.returncode = 0
            return r

        mock_run.side_effect = run_side_effect

        said = []
        terminal_out = []
        wrote = []

        self.driver.check_dependencies(
            say=lambda x: said.append(x),
            terminal=lambda x: terminal_out.append(x),
            write=lambda x: wrote.append(x),
        )

        # terminal shows OK/FAIL
        self.assertTrue(any("[ OK ] python3" in s for s in terminal_out))
        self.assertTrue(any("[ FAIL ] apt" in s for s in terminal_out))
        self.assertTrue(any("[ OK ] systemd" in s for s in terminal_out))

        # should attempt installation for missing apt
        self.assertTrue(any("sudo apt install apt" in s for s in wrote))

        # verify apt install command was called
        self.assertTrue(
            any(
                call_args[0][0][:3] == ["sudo", "apt", "install"]
                and call_args[0][0][3] == "apt"
                for call_args in mock_run.call_args_list
            )
        )


if __name__ == "__main__":
    unittest.main()
