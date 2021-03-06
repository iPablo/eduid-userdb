# -*- coding: utf-8 -*-
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

import copy

from eduid_userdb.element import Element, VerifiedElement, _update_something_by, _update_something_ts
from eduid_userdb.exceptions import UserDBValueError


__author__ = 'lundberg'


class NinProofingElement(VerifiedElement):
    """
    Element for holding the state of a NIN proofing flow. It should contain meta data needed for logging
    a proofing according to the Kantara specification.

    Properties of NinProofingElement:

        number
        created_by
        created_ts
        is_verified
        verified_by
        verified_ts
        verification_code

    :param data: element parameters from database

    :type data: dict
    """
    def __init__(self, number=None, application=None, created_ts=None, verified=False, verification_code=None,
                 data=None):

        data_in = data
        data = copy.copy(data_in)  # to not modify callers data

        if data is None:
            if created_ts is None:
                created_ts = True
            data = dict(number=number,
                        created_by=application,
                        created_ts=created_ts,
                        verified=verified,
                        verification_code=verification_code,
                        )

        VerifiedElement.__init__(self, data)
        self.number = data.pop('number')

    @property
    def number(self):
        """
        This is the nin number.

        :return: nin number.
        :rtype: str | unicode
        """
        return self._data['number']

    @number.setter
    def number(self, value):
        """
        :param value: nin number.
        :type value: str | unicode
        """
        if not isinstance(value, basestring):
            raise UserDBValueError("Invalid 'number': {!r}".format(value))
        self._data['number'] = str(value.lower())

    def to_dict(self):
        res = super(NinProofingElement, self).to_dict()
        res['number'] = self.number
        return res


class SentLetterElement(Element):
    """
        Properties of SentLetterElement:

        is_sent
        sent_ts
        transaction_id
        created_by
        created_ts
    """
    def __init__(self, data):
        super(SentLetterElement, self).__init__(data)

        self._data['is_sent'] = data.pop('is_sent', False)
        self._data['sent_ts'] = data.pop('sent_ts', None)
        self._data['transaction_id'] = data.pop('transaction_id', None)
        self._data['address'] = data.pop('address', None)

    @property
    def is_sent(self):
        """
        :return: True if this is a verified element.
        :rtype: bool
        """
        return self._data['is_sent']

    @is_sent.setter
    def is_sent(self, value):
        """
        :param value: New verification status
        :type value: bool
        """
        if not isinstance(value, bool):
            raise UserDBValueError("Invalid 'is_sent': {!r}".format(value))
        self._data['is_sent'] = value

    @property
    def sent_ts(self):
        """
        :return: Timestamp of when letter was delivered to letter service.
        :rtype: datetime.datetime
        """
        return self._data.get('sent_ts')

    @sent_ts.setter
    def sent_ts(self, value):
        """
        :param value: Timestamp of when letter was delivered to letter service.
                      Value None is ignored, True is short for datetime.utcnow().
        :type value: datetime.datetime | True | None
        """
        _update_something_ts(self._data, 'sent_ts', value)

    @property
    def transaction_id(self):
        """
        :return: Transaction information from the letter service
        :rtype: str | unicode
        """
        return self._data.get('transaction_id', '')

    @transaction_id.setter
    def transaction_id(self, value):
        """
        :param value: Transaction information from letter service (None is no-op).
        :type value: str | unicode | None
        """
        _update_something_by(self._data, 'transaction_id', value)

    @property
    def address(self):
        """
        :return: Official address the letter should be sent to
        :rtype: str | unicode
        """
        return self._data.get('address', None)

    @address.setter
    def address(self, value):
        """
        :param value: Official address the letter should be sent to
        :type value: dict | None
        """
        self._data['address'] = value
