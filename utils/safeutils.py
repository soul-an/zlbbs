# encoding: utf-8
# safeutils.py by Anderson Huang at 2019/1/3 11:56
from urllib.parse import urlparse, urljoin
from flask import request


# 判断url是否正确安全
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
