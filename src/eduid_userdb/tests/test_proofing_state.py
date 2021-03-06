# -*- coding: utf-8 -*-

from unittest import TestCase

from collections import OrderedDict
from eduid_userdb.nin import Nin
from eduid_userdb.proofing.proofing_state import LetterProofingState, OidcProofingState

__author__ = 'lundberg'

EPPN = 'foob-arra'

# Address as we get it from Navet
ADDRESS = OrderedDict([
    (u'Name', OrderedDict([
        (u'GivenNameMarking', u'20'), (u'GivenName', u'Testaren Test'),
        (u'SurName', u'Testsson')])),
    (u'OfficialAddress', OrderedDict([(u'Address2', u'\xd6RGATAN 79 LGH 10'),
                                      (u'PostalCode', u'12345'),
                                      (u'City', u'LANDET')]))
])


class ProofingStateTest(TestCase):

    def test_create_letterproofingstate(self):
        """
        {
             'eppn': 'foob-arra',
             'nin': {
                 'created_by': 'eduid-userdb.tests',
                 'created_ts': datetime(2015, 11, 9, 12, 53, 9, 708761),
                 'number': '200102034567',
                 'verification_code': 'abc123',
                 'verified': False
             },
             'proofing_letter': {
                 'is_sent': False,
                 'sent_ts': None,
                 'transaction_id': None
                 'address': {
                    'Name' : {
                        u'GivenNameMarking', u'20',
                        u'GivenName', u'Testaren Test',
                        u'SurName', u'Testsson'
                    },
                    u'OfficialAddress': {
                        u'Address2', u'\xd6RGATAN 79 LGH 10',
                        u'PostalCode', u'12345',
                        u'City', u'LANDET
                    }
                }'
             }
         }
        """
        state = LetterProofingState({
            'eduPersonPrincipalName': EPPN,
            'nin': {
                'number': '200102034567',
                'created_by': 'eduid_letter_proofing',
                'created_ts': True,
                'verified': False,
                'verification_code': 'abc123'
            }
        })
        state.proofing_letter.address = ADDRESS
        state_dict = state.to_dict()
        self.assertItemsEqual(state_dict.keys(), ['_id', 'eduPersonPrincipalName', 'nin', 'proofing_letter'])
        self.assertItemsEqual(state_dict['nin'].keys(), ['created_by', 'created_ts', 'number', 'verified',
                                                         'verification_code'])
        self.assertItemsEqual(state_dict['proofing_letter'].keys(), ['is_sent', 'sent_ts', 'transaction_id',
                                                                     'address'])

    def test_create_oidcproofingstate(self):
        """
        {
            'eduPersonPrincipalName': 'foob-arra',
            'nin': {
                'created_ts': datetime.datetime(2016, 11, 16, 14, 47, 0, 379810),
                'verified': False,
                'number': '190101021234',
                'created_by': 'eduid_oidc_proofing'
            },
            'state': '2c84fedd-a694-46f0-b235-7c4dd7982852'
            'nonce': 'bbca50f6-5213-4784-b6e6-289bd1debda5',
            'token': 'de5b3f2a-14e9-49b8-9c78-a15fcf60d119',
        }
        """

        nin = Nin(number='200102034567', application='eduid_oidc_proofing', verified=False, primary=False)
        state = OidcProofingState({
            'eduPersonPrincipalName': EPPN,
            'nin': nin.to_dict(),
            'state': '2c84fedd-a694-46f0-b235-7c4dd7982852',
            'nonce': 'bbca50f6-5213-4784-b6e6-289bd1debda5',
            'token': 'de5b3f2a-14e9-49b8-9c78-a15fcf60d119'
        })
        state_dict = state.to_dict()
        self.assertItemsEqual(state_dict.keys(), ['_id', 'nin', 'eduPersonPrincipalName', 'state', 'nonce', 'token'])
        self.assertItemsEqual(state_dict['nin'].keys(), ['created_by', 'created_ts', 'number', 'verified'])
