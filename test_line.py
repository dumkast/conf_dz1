import unittest
import platform
from command_line import VirtualFileSystem


class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        self.vfs = VirtualFileSystem("system.tar", "user", "hostname")

    def test_cd_to_root(self):
        self.vfs.cd('~')
        self.assertEqual(self.vfs.current_dir, '/')

    def test_cd_to_nonexistent_directory(self):
        self.vfs.cd('nonexistent_folder')
        self.assertEqual(self.vfs.current_dir, '/')

    def test_cd_to_subdirectory(self):
        self.vfs.cd('system/folder_1')
        self.assertEqual(self.vfs.current_dir, '/system/folder_1/')

    def test_uptime_format(self):
        uptime_info = self.vfs.uptime()
        self.assertIn("Текущее время:", uptime_info)
        self.assertIn("Время работы:", uptime_info)


    def test_uptime_value(self):
        uptime_info = self.vfs.uptime()
        uptime_seconds = float(uptime_info.split("Время работы: ")[1].split(" секунд")[0])
        self.assertGreaterEqual(uptime_seconds, 0)

    def test_uptime_after_delay(self):
        import time
        time.sleep(1)
        uptime_info_before = self.vfs.uptime()
        time.sleep(1)
        uptime_info_after = self.vfs.uptime()

        uptime_before = float(uptime_info_before.split("Время работы: ")[1].split(" секунд")[0])
        uptime_after = float(uptime_info_after.split("Время работы: ")[1].split(" секунд")[0])

        self.assertGreater(uptime_after, uptime_before)

    def test_who_returns_username(self):
        self.assertEqual(self.vfs.who(), 'user')

    def test_who_with_different_user(self):
        self.vfs.user_name = 'another_user'
        self.assertEqual(self.vfs.who(), 'another_user')

    def test_who_initialization(self):
        self.assertEqual(self.vfs.user_name, 'user')

    def test_uname_structure(self):
        output = self.vfs.uname()
        self.assertIsInstance(output, str)

    def test_uname_contains_system_info(self):
        output = self.vfs.uname()
        self.assertIn("Система:", output)
        self.assertIn("Имя узла:", output)
        self.assertIn("Версия:", output)
        self.assertIn("Полная версия:", output)
        self.assertIn("Архитектура:", output)
        self.assertIn("Процессор:", output)

    def test_uname_correctness(self):
        output = self.vfs.uname()
        expected_system = platform.system()
        expected_node = platform.node()
        expected_release = platform.release()
        expected_version = platform.version()
        expected_machine = platform.machine()
        expected_processor = platform.processor()

        self.assertIn(expected_system, output)
        self.assertIn(expected_node, output)
        self.assertIn(expected_release, output)
        self.assertIn(expected_version, output)
        self.assertIn(expected_machine, output)
        self.assertIn(expected_processor, output)

    def test_ls_root_directory(self):
        self.vfs.cd('~')
        expected_output = ['system']
        actual_output = self.vfs.ls("/")
        self.assertEqual(sorted(actual_output), sorted(expected_output))

    def test_ls_subdirectory(self):
        expected_output = ['folder_1', 'folder_2', 'folder_3']
        actual_output = self.vfs.ls("system")
        self.assertEqual(sorted(actual_output), sorted(expected_output))

    def test_ls_nonexistent_directory(self):
        actual_output = self.vfs.ls("nonexistent_folder")
        self.assertEqual(actual_output, [])


if __name__ == "__main__":
    unittest.main()