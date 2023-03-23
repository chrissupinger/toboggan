# Third-party
from requests import Request

__all__ = ('Blocking',)


class Blocking:

    @staticmethod
    def sender(session, state):
        try:
            prepped = session.prepare_request(Request(**state))
            return session.send(prepped)
        except Exception as err_msg:
            return err_msg
