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

    def test_optional_readability_limits(self):
        text = '1\n00:00:00,000 --> 00:00:01,000\nHello world'
        self.assertTrue(check(text)['ok'])
        types = {x['type'] for x in check(text, max_line_length=5, max_cps=10)['issues']}
        self.assertEqual(types, {'line_too_long', 'reading_speed'})

    def test_readability_boundaries_and_multiline(self):
        text = '1\n00:00:00,000 --> 00:00:02,000\nABCD\nEFGH'
        self.assertTrue(check(text, max_line_length=4, max_cps=4)['ok'])

    def test_unicode_numeric_index_is_reported(self):
        self.assertEqual(check('\u00b2\n00:00:00,000 --> 00:00:01,000\nA')['issues'][0]['type'],
                         'invalid_index_or_block')

    def test_invalid_thresholds(self):
        for threshold in (0, -1, float('nan'), float('inf')):
            with self.assertRaises(ValueError): check('', max_cps=threshold)
        with self.assertRaises(ValueError): check('', max_line_length=0)

    def test_bom_crlf_and_no_caption_leak(self):
        result = check('\ufeff1\r\n00:00:00,000 --> 00:00:01,000\r\nSynthetic caption', max_cps=1)
        self.assertNotIn('Synthetic caption', str(result))
        self.assertEqual(result['blocks'], 1)
