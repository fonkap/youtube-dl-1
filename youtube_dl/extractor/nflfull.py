# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from .. import utils, compat
from ..utils import js_to_json


class NflFullIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?nflfull\.com/(?P<id>.+)\.html'
    _TEST = {
        'url': 'https://nflfull.com/denver-vs-seattle-week-1-sep-12-2022_ca5c41820.html',
        'md5': 'fc8793783061a4e69d5fc00116adae0e',
        'info_dict': {
            'id': 'ip9bfz9sj91h',
            'title': 'W1_-_Denver_vs_Seattle_-_Sep_12__2022.mp4',
            'ext': 'mp4'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        embed = self._search_regex(r'iframe src=\"(https?://.*/player/embed\.php.*?)\"', webpage, 'embed')
        inner_webpage = self._download_webpage(embed, video_id, headers={'Referer': 'https://nflfull.com/'})

        movie_server = self._search_regex(r"loadMovieServer\('(https?://filemoon\.sx.*)',", inner_webpage, 'movie server')
        self.report_following_redirect(movie_server)
        return self.url_result(movie_server)


    def report_following_redirect(self, new_url):
        """Report information extraction."""
        self._downloader.to_screen('[redirect] Following redirect to %s' % new_url)
