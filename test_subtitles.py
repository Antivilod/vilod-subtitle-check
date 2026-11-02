import unittest
from subtitle_check import check


class SubtitleTests(unittest.TestCase):
    def test_adjacent_valid(self):
        self.assertTrue(check('1\n00:00:00,000 --> 00:00:01,000\nA\n\n2\n00:00:01,000 --> 00:00:02,000\nB')['ok'])

    def test_nested_overlap(self):
        result=check('1\n00:00:00,000 --> 00:00:10,000\nA\n\n2\n00:00:01,000 --> 00:00:02,000\nB\n\n3\n00:00:03,000 --> 00:00:04,000\nC')
        self.assertEqual(sum(x['type']=='overlap' for x in result['issues']),2)

    def test_invalid_and_empty(self):
        self.assertFalse(check('')['ok'])
        self.assertFalse(check('1\n00:61:00,000 --> 00:62:00,000\nA')['ok'])

    def test_empty_caption_and_duration(self):
        types={x['type'] for x in check('1\n00:00:02,000 --> 00:00:01,000\n')['issues']}
        self.assertIn('empty_caption',types)
        self.assertIn('nonpositive_duration',types)
