# Assistente PetShop - Chatbot com Rasa

Um assistente de inteligência artificial conversacional desenvolvido com **Rasa** para automatizar o agendamento de serviços em PetShop. O bot é capaz de compreender requisições em linguagem natural, coletar informações do usuário e confirmar agendamentos de forma intuitiva e personalizada.

## Características

- **Interface Conversacional**: Chatbot em português capaz de manter diálogos naturais
- **Extração de Entidades**: Identifica automaticamente:
  - Tipos de serviço (banho, tosa, banho e tosa, etc.)
  - Nome do pet
  - Raça do animal
  - Horário desejado
- **Gerenciamento de Estado**: Utiliza slots para rastrear informações ao longo da conversa
- **Validação de Dados**: Valida serviços e horários disponíveis
- **Interface Web**: Chat integrado em HTML/CSS/JavaScript
- **Ações Customizadas**: Processamento de lógica de negócio específica
- **Suporte a Fallback**: Tratamento inteligente de mensagens fora de escopo

## Tecnologias Utilizadas

- **[Rasa 3.x](https://rasa.com/)** - Framework de NLU e gerenciamento de diálogos
- **Python 3.8+** - Linguagem de programação
- **Rasa SDK** - Para desenvolvimento de ações customizadas
- **HTML5/CSS3/JavaScript** - Interface de usuário web
- **YAML** - Configuração e definição de dados de treinamento

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonar o repositório)
- Virtualenv (recomendado para ambientes isolados)

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/petshop-chatbot.git
cd petshop-chatbot
```

### 2. Crie um ambiente virtual

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` não existir, instale manualmente:

```bash
pip install rasa rasa-sdk
```

### 4. Treine o modelo

```bash
rasa train
```

Este comando irá:
- Processar os dados de NLU definidos em `data/nlu.yml`
- Processar as regras em `data/rules.yml`
- Processar as histórias em `data/stories.yml`
- Gerar um modelo treinado na pasta `models/`

## Como Usar

### 1. Inicie o servidor de ações

Em um terminal separado:

```bash
rasa run actions
```

Este servidor executa as ações customizadas definidas em `actions/actions.py`.

### 2. Inicie o servidor Rasa

```bash
rasa run -m models --enable-api --cors "*"
```

O servidor estará disponível em `http://localhost:5005`

### 3. Acesse a interface web

Abra `chat.html` em seu navegador:

```bash
# Windows
start chat.html

# macOS
open chat.html

# Linux
xdg-open chat.html
```

Ou copie o caminho do arquivo e abra em seu navegador (ex: `file:///C:/path/to/chat.html`)

### 4. Interaja com o chatbot

Exemplos de mensagens para testar:

- **Saudação**: "Olá!" ou "Bom dia"
- **Ver serviços**: "Quais serviços vocês oferecem?"
- **Marcar agendamento**: "Quero marcar um banho para o Rex amanhã às 14h"
- **Pedir ajuda**: "Pode me ajudar?"
- **Despedir-se**: "Tchau!"

## Estrutura do Projeto

```
petshop-chatbot/
├── chat.html                 # Interface web do chatbot
├── config.yml              # Configuração do pipeline NLU e políticas
├── domain.yml              # Definição de intents, entidades, slots e respostas
├── endpoints.yml           # Configuração de endpoints (ações, tracker store)
├── requirements.txt        # Dependências do projeto
├── data/
│   ├── nlu.yml            # Dados de treinamento NLU (intents e exemplos)
│   ├── rules.yml          # Regras de diálogo (fluxos determinísticos)
│   └── stories.yml        # Histórias de conversa (fluxos aprendidos)
├── actions/
│   └── actions.py         # Ações customizadas em Python
├── models/                # Modelos treinados (gerado após `rasa train`)
└── .rasa/                 # Arquivos internos do Rasa
```

### Descrição dos Arquivos Principais

#### `config.yml`
Define o pipeline de processamento de linguagem natural e as políticas de diálogo:
- **Pipeline**: Tokenização, extração de features, classificação de intents, reconhecimento de entidades
- **Políticas**: Algoritmos de decisão para próximas ações (Memoização, Regras, TED)

#### `domain.yml`
Especifica:
- **Intents**: Tipos de intenção do usuário (saudação, agendamento, etc.)
- **Entities**: Informações extraídas (serviço, nome_pet, horário, raça)
- **Slots**: Variáveis de estado para armazenar informações
- **Responses**: Respostas templates do bot

#### `data/nlu.yml`
Contém exemplos de frases para treinar o modelo a reconhecer intents e extrair entidades.

#### `data/rules.yml`
Define regras de conversa - fluxos determinísticos que devem ser sempre seguidos.

#### `data/stories.yml`
Define histórias de conversa - exemplos de diálogos completos para treinamento.

#### `actions/actions.py`
Implementa ações customizadas em Python:
- `ActionResumoAgendamento`: Reúne informações do agendamento
- `ActionValidarServico`: Valida se o serviço é válido

#### `chat.html`
Interface web responsiva com:
- Estilo moderno e amigável para pet
- Comunicação via API REST com Rasa
- Exibição de mensagens do bot e usuário
- Input field para novas mensagens

## Configuração Avançada

### Adicionar Novos Intents

1. Edite `data/nlu.yml`:
```yaml
- intent: novo_intent
  examples: |
    - exemplo 1
    - exemplo 2
    - exemplo 3
```

2. Adicione em `domain.yml`:
```yaml
intents:
  - novo_intent
```

3. Defina as respostas em `domain.yml`:
```yaml
responses:
  utter_resposta:
    - text: "Texto da resposta"
```

4. Crie regras ou histórias em `data/rules.yml` ou `data/stories.yml`

5. Treine novamente:
```bash
rasa train
```

### Adicionar Novas Ações Customizadas

1. Edite `actions/actions.py`:
```python
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class MinhaAcao(Action):
    def name(self) -> Text:
        return "action_minha_acao"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Sua lógica aqui
        dispatcher.utter_message(text="Resposta do bot")
        return []
```

2. Use em `domain.yml` como uma ação
3. Restart o servidor de ações

### Integração com Banco de Dados

No arquivo `actions/actions.py`, você pode adicionar:

```python
import sqlite3
# ou
from pymongo import MongoClient
# ou
import requests  # para APIs externas
```

## Testando o Chatbot

### Via Shell do Rasa

```bash
rasa shell
```

Digite suas mensagens diretamente no terminal para testar.

### Via API REST

```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -d '{"sender": "user", "message": "Olá!"}' \
  -H "Content-Type: application/json"
```

### Análise do Modelo

```bash
rasa test nlu --nlu data/nlu.yml
```

## Métricas e Avaliação

Após treinar, você pode visualizar:

- Acurácia de classificação de intents
- Precisão e recall de reconhecimento de entidades
- Matriz de confusão de intents

```bash
rasa test
```

## Troubleshooting

### Erro: "Module 'rasa' has no attribute..."

Certifique-se de estar usando a versão correta do Rasa:
```bash
pip install rasa==3.x.x
```

### O chatbot não responde

1. Verifique se o servidor de ações está rodando: `rasa run actions`
2. Verifique se o servidor Rasa está rodando: `rasa run -m models --enable-api`
3. Verifique o console para erros

### Modelo não treinado

Execute:
```bash
rasa train
```

Se persistir, limpe e treine novamente:
```bash
rm -rf models/
rasa train
```

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona minha feature'`)
4. Push para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE) - veja o arquivo LICENSE para detalhes.


