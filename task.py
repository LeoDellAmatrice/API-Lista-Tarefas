class Task:
    def __init__(self, task_id, titulo, descricao, status, prioridade, data_inicio, data_fim):
        self.task_id = task_id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.prioridade = prioridade
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def get_id(self):
        return self.task_id

    def json(self):
        return {
            "task_id": self.task_id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "prioridade": self.prioridade,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
        }

    def atualizar(self, dados):
        self.data_inicio = dados["data_inicio"]
        self.data_fim = dados["data_fim"]
        self.status = dados["status"]
        self.prioridade = dados["prioridade"]
        self.titulo = dados["titulo"]
        self.descricao = dados["descricao"]
        self.task_id = dados["task_id"]
