# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from .. import utils, compat
from ..utils import js_to_json


class FileMoonIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?filemoon\.sx/./(?P<id>.+)/(?P<title>.+)'
    _TEST = {
        # 'url': 'https://filemoon.sx/e/ashwd61m74ge/W02.Seahawks.vs.49ers.18-09-2022.mp4',
        'url': 'https://filemoon.sx/d/e2l4uy8tiisg/sample_3840x2160.mkv',
        'md5': '441f0a1b75e5fe42d762fc5e28c60146',
        'info_dict': {
            'id': 'e2l4uy8tiisg',
            'title': 'sample_3840x2160.mkv',
            'ext': 'mp4'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        m = self._VALID_URL_RE.match(url)
        title = compat.compat_str(m.group('title'))

        webpage = self._download_webpage(url, video_id)
        packed = self._search_regex(r'(eval\(function.+)', webpage, 'packed code')
        unpacked = utils.decode_packed_codes(packed)

        jwplayer_sources = self._parse_json(
            self._search_regex(
                r"(?s)player\.setup\(\{sources:(.*?])", unpacked, 'jwplayer sources'),
            video_id, transform_source=js_to_json)

        formats = self._parse_jwplayer_formats(jwplayer_sources, video_id)

        return {
            'id': video_id,
            'title': title,
            'formats': formats
        }
