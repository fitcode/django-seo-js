import re
from django_seo_js import settings
from django_seo_js.backends import SelectedBackend
from django_seo_js.helpers import request_should_be_ignored

import logging
logger = logging.getLogger(__name__)


class UserAgentMiddleware(SelectedBackend):
    def __init__(self, *args, **kwargs):
        super(UserAgentMiddleware, self).__init__(*args, **kwargs)
        regex_str = "|".join(settings.USER_AGENTS)
        regex_str = ".*?(%s)" % regex_str
        self.USER_AGENT_REGEX = re.compile(regex_str, re.IGNORECASE)

    def process_request(self, request):
        if not request.ENABLED:
            return

        if request_should_be_ignored(request):
            return

        if "HTTP_USER_AGENT" not in request.META:
            return

        if not self.USER_AGENT_REGEX.match(request.META["HTTP_USER_AGENT"]):
            return

        url = request.build_absolute_uri()
        try:
            return self.backend.get_response_for_url(url)
        except Exception as e:
            logger.exception(e)
