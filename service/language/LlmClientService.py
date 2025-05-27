from repository.LlmClientRepository import LlmClientRepository


class LlmClientService:
    def __init__(self, repo):
        self.repo = repo

    def get_client(self, client_id):
        return self.repo.get_client_by_id(client_id)
