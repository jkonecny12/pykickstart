import unittest
from tests.baseclass import CommandTest
from pykickstart.errors import KickstartValueError


class F26_TestCase(CommandTest):
    command = "snapshot"

    def runTest(self):
        # pass
        self.assert_parse("snapshot vg00/lv --name test", "snapshot vg00/lv --name=test\n")
        self.assert_parse("snapshot vg00/lv --name=test", "snapshot vg00/lv --name=test\n")
        self.assert_parse("snapshot vg00/lv --name=test --when=post-install", "snapshot vg00/lv --name=test --when=post-install\n")
        self.assert_parse("snapshot vg00/lv --name=test --when=pre-install", "snapshot vg00/lv --name=test --when=pre-install\n")
        self.assert_parse("snapshot vg00/lv --name=test", "snapshot vg00/lv --name=test\n")

        # missing required field
        self.assert_parse_error("snapshot", exception=KickstartValueError)
        self.assert_parse_error("snapshot vg00/lv", exception=KickstartValueError)
        self.assert_parse_error("snapshot --name=test", exception=KickstartValueError)
        self.assert_parse_error("snapshot --name")

        # bad lv name
        self.assert_parse_error("snapshot lv --name test", exception=KickstartValueError)
        self.assert_parse_error("snapshot vg_lv --name test", exception=KickstartValueError)

        # bad when option
        self.assert_parse_error("snapshot lv --name test --when error", exception=KickstartValueError)

        # nonsensical parameter test
        self.assert_parse_error("snapshot --nonsense")


if __name__ == "__main__":
    unittest.main()
