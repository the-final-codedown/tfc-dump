import falcon
import json
import os
import requests


class DumpInfo:
    account_url = None
    profile_url = None


# port : 8083
class DumpController(object):
    def on_get(self, req, resp):
        x =requests.get(DumpInfo.account_url + '/accounts/SAVINGS/' + "accounts")
        print(x)
        resp.body = json.dumps(x)
        resp.status = falcon.HTTP_200
        return resp


def setup_dump(account_url, profile_url):
    if account_url is not None and profile_url is not None:
        DumpInfo.account_url = account_url
        DumpInfo.profile_url = profile_url

        print(DumpInfo.account_url)
        print(DumpInfo.profile_url)
    app = falcon.API()

    dump_controller = DumpController()
    app.add_route('/dump', dump_controller)

    return app
