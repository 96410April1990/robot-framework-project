import requests

class MultipartPostApiCall(object):

    ROBOT_LIBRARY_VERSION = '__version__'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def make_multipart_post_api_call(self, url, payload, files):

        with open(files, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, data=payload, files=files)

        return str(response)