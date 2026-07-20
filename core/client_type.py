from core.tsetmc_client import TSETMCClient


class ClientTypeAPI:

    def __init__(self):

        self.client = TSETMCClient()

        print("ClientType API initialized")

    def get(self):

        raw = self.client.get_old("/ClientTypeAll.aspx")

        if raw is None:
            return ""

        return raw


