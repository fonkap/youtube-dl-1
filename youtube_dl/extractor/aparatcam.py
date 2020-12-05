# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import js_to_json


class AparatCamIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?aparat\.cam/embed-(?P<id>\w+).html'
    _TEST = {
        'url': 'https://aparat.cam/embed-0wfvjmtlvxy5.html',
        'md5': 'f443ee35e0aac693e82ffeb003cfae50',
        'info_dict': {
            'id': '0wfvjmtlvxy5',
            'ext': 'mp4',
            'title': '0wfvjmtlvxy5'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # thumbnail = self._html_search_meta(['og:image'], webpage)
        # uploader = self._search_regex(r'<a[^>]+class="mv_user_name"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False)

        jwplayer_data = self._parse_json(
            self._search_regex(
                r"(?s)videojs\('vjsplayer',({.*?)\)", webpage, 'vjsplayer code'),
            video_id, transform_source=js_to_json)

        formats = self._extract_m3u8_formats(jwplayer_data['sources'][0]['src'], video_id, ext='mp4')

        return {
            'id': video_id,
            'formats': formats,
            'title': video_id
        }
