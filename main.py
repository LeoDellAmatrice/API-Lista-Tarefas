from datetime import date
from flasgger import Swagger, swag_from
from flask import Flask, request

app = Flask(__name__)
Swagger(app)

tarefas = [
    {
        'id': 1,
        'titulo': 'Atualizar Git Hub',
        'descricao': 'Atualizar perfil do Git Hub, alterando foto, e adicionando descrição',
        'status': 'Em andamento',
        'prioridade': "Baixa",
        'data-inicio': '24/02/2025',
        'data-fim': None,
    },
    {
        'id': 2,
        'titulo': 'Estudar Flask',
        'descricao': 'Estudar Flask para aprender sobre Web Service',
        'status': 'Finalizado',
        'prioridade': "Baixa",
        'data-inicio': '24/02/2025',
        'data-fim': '25/02/2025',
    }
]

# Schema padrão para respostas de tarefas
TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'titulo': {'type': 'string'},
        'descricao': {'type': 'string'},
        'status': {'type': 'string', 'enum': ['Não iniciada', 'Em andamento', 'Finalizado']},
        'prioridade': {'type': 'string', 'enum': ['Baixa', 'Média', 'Alta']},
        'data-inicio': {'type': 'string', 'format': 'date'},
        'data-fim': {'type': ['string', 'null'], 'format': 'date'}
    }
}

@app.route('/tasks', methods=['GET'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Lista todas as tarefas cadastradas',
    'responses': {
        200: {
            'description': 'Listagem de todas as tarefas',
            'schema': {
                'type': 'array',
                'items': TASK_SCHEMA
            }
        }
    }
})
def get_tasks():
    return tarefas

@app.route('/tasks', methods=['POST'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Cria uma nova tarefa',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'titulo': {'type': 'string'},
                    'descricao': {'type': 'string'},
                    'status': {'type': 'string', 'enum': ['Não iniciada', 'Em andamento', 'Finalizado']},
                    'prioridade': {'type': 'string', 'enum': ['Baixa', 'Média', 'Alta']},
                    'data-inicio': {'type': 'string', 'format': 'date'},
                    'data-fim': {'type': ['string', 'null'], 'format': 'date'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Tarefa criada com sucesso',
            'schema': TASK_SCHEMA
        }
    }
})
def create_task():
    task = request.json
    task['id'] = len(tarefas) + 1

    if not task.get('titulo'):
        task['titulo'] = 'Sem titulo'

    if not task.get('descricao'):
        task['descricao'] = 'Sem descrição'

    if not task.get('status'):
        task['status'] = 'Em andamento'

    if not task.get('prioridade'):
        task['prioridade'] = 'Baixa'

    if not task.get('data-inicio'):
        task['data-inicio'] = date.today().strftime('%d/%m/%Y')

    if not task.get('data-fim') and task['status'] == 'Finalizado':
        task['data-fim'] = date.today().strftime('%d/%m/%Y')
    else:
        task['data-fim'] = None

    tarefas.append(task)
    return task, 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Atualiza uma tarefa existente',
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da tarefa'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'titulo': {'type': 'string'},
                    'descricao': {'type': 'string'},
                    'status': {'type': 'string', 'enum': ['Não iniciada', 'Em andamento', 'Finalizado']},
                    'prioridade': {'type': 'string', 'enum': ['Baixa', 'Média', 'Alta']},
                    'data-inicio': {'type': 'string', 'format': 'date'},
                    'data-fim': {'type': ['string', 'null'], 'format': 'date'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Tarefa atualizada com sucesso',
            'schema': TASK_SCHEMA
        },
        404: {
            'description': 'Tarefa não encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Task not found'}
                }
            }
        }
    }
})
def update_task(task_id):
    tarefa_atualizar = None
    for tarefa in tarefas:
        if tarefa['id'] == task_id:
            tarefa_atualizar = tarefa
            break

    if not tarefa_atualizar:
        return {'error': 'Task not found'}, 404

    task_body = request.json

    if task_body.get('titulo'):
        tarefa_atualizar['titulo'] = task_body['titulo']

    if task_body.get('descricao'):
        tarefa_atualizar['descricao'] = task_body['descricao']

    if task_body.get('status'):
        tarefa_atualizar['status'] = task_body['status']
        if task_body['status'] == 'Finalizado':
            tarefa_atualizar['data-fim'] = date.today().strftime('%d/%m/%Y')

    if task_body.get('prioridade'):
        tarefa_atualizar['prioridade'] = task_body['prioridade']

    if task_body.get('data-inicio'):
        tarefa_atualizar['data-inicio'] = task_body['data-inicio']

    if task_body.get('data-fim'):
        tarefa_atualizar['data-fim'] = task_body['data-fim']

    return tarefa_atualizar

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Exclui uma tarefa',
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da tarefa'
        }
    ],
    'responses': {
        200: {
            'description': 'Tarefa excluída com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'sucess': {'type': 'string', 'example': 'Task deleted'}
                }
            }
        },
        404: {
            'description': 'Tarefa não encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Task not found'}
                }
            }
        }
    }
})
def delete_task(task_id):
    for tarefa in tarefas:
        if tarefa['id'] == task_id:
            tarefas.remove(tarefa)
            return {'sucess': 'Task deleted'}
    return {'error': 'Task not found'}, 404

@app.route('/tasks/<int:task_id>', methods=['GET'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Obtém detalhes de uma tarefa específica',
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da tarefa'
        }
    ],
    'responses': {
        200: {
            'description': 'Detalhes da tarefa',
            'schema': TASK_SCHEMA
        },
        404: {
            'description': 'Tarefa não encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Task not found'}
                }
            }
        }
    }
})
def get_task_by_id(task_id):
    for tarefa in tarefas:
        if tarefa['id'] == task_id:
            return tarefa
    return {'erro': 'Task not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)