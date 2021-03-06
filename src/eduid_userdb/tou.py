#
# Copyright (c) 2015 NORDUnet A/S
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided
#        with the distribution.
#     3. Neither the name of the NORDUnet nor the names of its
#        contributors may be used to endorse or promote products derived
#        from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author : Fredrik Thulin <fredrik@thulin.net>
#

import copy

from eduid_userdb.event import Event, EventList
from eduid_userdb.exceptions import BadEvent


class ToUEvent(Event):
    """
    A record of a user's acceptance of a particular version of the Terms of Use.
    """
    def __init__(self, version=None, application=None, created_ts=None, event_id=None,
                 data=None, raise_on_unknown=True):
        data_in = data
        data = copy.copy(data_in)  # to not modify callers data

        if data is None:
            data = dict(version = version,
                        created_by = application,
                        created_ts = created_ts,
                        event_type = 'tou_event',
                        id = event_id,
                        )
        for required in ['created_by', 'created_ts']:
            if required not in data or not data.get(required):
                raise BadEvent('missing required data for event: {!s}'.format(required))
        Event.__init__(self, data=data, raise_on_unknown=raise_on_unknown, ignore_data = ['version'])
        self.version = data.pop('version')

    # -----------------------------------------------------------------
    @property
    def version(self):
        """
        This is the version of the ToU that was accepted.

        :return: ToU version.
        :rtype: str | unicode
        """
        return self._data['version']

    @version.setter
    def version(self, value):
        """
        :param value: Unique ID of event.
        :type value: bson.ObjectId
        """
        if not isinstance(value, str) and not isinstance(value, unicode):
            raise BadEvent("Invalid tou_event 'version': {!r}".format(value))
        self._data['version'] = value

    # -----------------------------------------------------------------


class ToUList(EventList):
    """
    List of ToUEvents.
    """
    def __init__(self, events, raise_on_unknown=True, event_class=ToUEvent):
        EventList.__init__(self, events, raise_on_unknown=raise_on_unknown, event_class=event_class)

    def has_accepted(self, version):
        """
        Check if the user has accepted a particular version of the ToU.

        :param version: Version of ToU
        :type version: str | unicode

        :return: True or False
        :rtype: bool
        """
        # All users have implicitly accepted the first ToU version (info stored in another collection)
        if version in ['2014-v1', '2014-dev-v1']:
            return True
        for this in self._elements:
            if this.version == version:
                return True
        return False
