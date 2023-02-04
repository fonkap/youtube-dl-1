# coding: utf-8
from __future__ import unicode_literals

import json

from .common import InfoExtractor
from .. import utils, compat
from ..utils import js_to_json


class NflFullIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?(nflfull\.com|footballusa\.net)/(?P<id>.+)\.html'
    _TEST = {
        'url': 'https://nflfull.com/49ers-vs-panthers-week-5-oct-08-2022_c51b958bb.html',
        'md5': '3870bd8148ace139bd6451549f258fec',
        'info_dict': {
            'id': '49ers-vs-panthers-week-5-oct-08-2022_c51b958bb',
            'title': '49ers-vs-panthers-week-5-oct-08-2022_c51b958bb',
            'ext': 'mp4'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        embed = self._search_regex(r'iframe src=\"(https?://.*/player/embed\.php.*?)\"', webpage, 'embed')

        inner_webpage = self._download_webpage(embed, video_id, headers={'Referer': 'https://nflfull.com/'}, note="download embedded iframe")
        movie_server = self._search_regex(r"loadMovieServer\('(https?://spcdn\.xyz.*)',", inner_webpage, 'index webpage')

        if movie_server:
            idx_webpage = self._download_webpage(movie_server, video_id, headers={'Referer': 'https://nflfull.com/'}, note="download movie server page")
            js_data = self._search_regex(r'FirePlayer\(vhash,(.*),.*\);', idx_webpage, 'js player data')
            json_data = js_to_json(js_data)
            videoSettings = json.loads(json_data)
            videoDisk = videoSettings['videoDisk']
            if videoDisk:
                videoDisk = str(videoDisk)
            else:
                videoDisk = ""

            file = "https://spcdn.xyz" + videoSettings['videoUrl'] + "?s=" + videoSettings['videoServer'] + "&d=" + videoDisk
            # headers needed to avoid "security error" message
            headers = {'Referer': movie_server, 'Accept': '*/*'}
            m3u8_webpage = self._download_webpage(file, video_id, headers=headers, note="download first m3u8 file")

            formats = self._parse_m3u8_formats(m3u8_webpage, file)
            for format in formats:
                format['protocol'] = 'm3u8_native'
                format['ext'] = 'mp4'

            result = {
                'id': video_id,
                'title': video_id,
                'formats': formats,
                'ext': 'mp4',
                'http_headers': headers
            }
        else:
            movie_server = self._search_regex(r"loadMovieServer\('(https?://filemoon\.sx.*)',", inner_webpage, 'movie server', default=None)
            self.report_following_redirect(movie_server)
            result = self.url_result(movie_server)

        return result


    def report_following_redirect(self, new_url):
        """Report information extraction."""
        self._downloader.to_screen('[redirect] Following redirect to %s' % new_url)
