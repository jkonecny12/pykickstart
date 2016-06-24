#
# Jiri Konecny <jkonecny@redhat.com>
#
# Copyright 2016 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.
#

from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartValueError, formatErrorMsg
from pykickstart.options import KSOptionParser

import gettext
import warnings
_ = lambda x: gettext.ldgettext("pykickstart", x)

class F26_SnapshotData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.name = kwargs.get("name", "")
        self.origin = kwargs.get("origin", "")

    def __eq__(self, y):
        if not y:
            return False
        return (self.name == y.name and
                self.origin == y.origin)

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "snapshot %s --name=%s" % (self.origin, self.snapshot_name)
        return retval + "\n"


class F26_Snapshot(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=140, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.snapshotList = kwargs.get("snapshotList", [])

    def __str__(self):
        retval = ""

        for part in self.snapshotList:
            retval += part.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--name", dest="name", required=1)

        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) == 0:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Snapshot origin must be specified!")))
        elif len(extra) > 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Snapshot origin can be specified only once")))

        snap_data = self.handler.SnapshotData()
        self._setToObj(self.op, opts, snap_data)
        snap_data.lineno = self.lineno
        snap_data.origin = extra[0]

        # Check for duplicates
        if snap_data.name in [snap.name for snap in self.dataList()]:
            raise KickstartValueError(
                        formatErrorMsg(self.lineno,
                                       msg=(_("Snapshot with the name %s has been already defined") %
                                            snap_data.name)))

        groups = snap_data.origin.split('/')
        if len(groups) != 2 or len(groups[0]) == 0 or len(groups[1]) == 0:
            raise KickstartValueError(
                        formatErrorMsg(self.lineno,
                                       msg=(_("Snapshot origin %s must be specified by VG/LV") %
                                            snap_data.origin)))
        return snap_data

    def dataList(self):
        return self.snapshotList
