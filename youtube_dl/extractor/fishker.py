# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import js_to_json
import random
import string


def to_ascii_hex(string):
    return ''.join([format(ord(c), 'x') for c in string])


def generate_random_string(l):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(l))

class FishkerIE(InfoExtractor):
    _VALID_URL = r'https://fishker.com/(?P<id>.+)/'
    _TEST = {
        'url': 'https://fishker.com/103-2/',
        'md5': '76a26a2905c1536515ec345755641ca2',
        'info_dict': {
            'id': '103-2',
            'ext': 'mp4',
            'title': 'NFL-2023-01-29 W21 SF@PHI'
        }
    }


    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        iframe_url = self._search_regex(r'IFRAME SRC=\"(.*)\"', webpage, 'iframe')
        video_code = self._search_regex(r"(\w*).html", iframe_url, 'video_code')

        l = 12
        req = generate_random_string(l) + '||' + video_code + '||' + generate_random_string(l) + '||streamsb'
        ereq = 'https://sbchill.com/sources50/' + to_ascii_hex(req)

        video_data = self._download_webpage(ereq, video_id, headers={
            'Referer': iframe_url,
            'watchsb': 'sbstream'}
        )
        player_data = self._parse_json(video_data, video_id)
        formats = self._extract_m3u8_formats(player_data['stream_data']['file'], video_id, ext='mp4'
                                             ,entry_protocol='m3u8_native', m3u8_id='hls', fatal=False)
        return {
            'id': video_id,
            'formats': formats,
            'title': player_data['stream_data']['title']
        }
