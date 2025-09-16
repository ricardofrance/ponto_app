# Aplicativo Flask para Marcação de Ponto

Este aplicativo Flask automatiza a marcação de ponto para saída do almoço, entrada do almoço e final do expediente, utilizando o script `clocking_script.py` e o agendador APScheduler.

## Instalação e Configuração

Siga os passos abaixo para configurar e executar o aplicativo em seu servidor local:

### 1. Pré-requisitos

Certifique-se de ter o Python 3 e o `pip` (gerenciador de pacotes do Python) instalados em seu sistema.

### 2. Clonar o Repositório (ou baixar os arquivos)

Se você recebeu os arquivos do projeto, descompacte-os em um diretório de sua escolha. Caso contrário, se for um repositório Git, clone-o:

```bash
git clone <URL_DO_REPOSITORIO>
cd ponto_app
```

### 3. Configurar Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto:

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate  # No Windows
```

### 4. Instalar Dependências

Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

### 5. Configurar Credenciais (clocking_script.py)

Edite o arquivo `src/clocking_script.py` e substitua as credenciais `USERNAME` e `PASSWORD` pelos seus dados reais de login na plataforma Senior:

```python
# Credenciais de login (substitua pelos valores reais)
USERNAME = "seu.email@exemplo.com"
PASSWORD = "SuaSenhaAqui"
```

**Importante:** Este script simula a marcação de ponto. Em um ambiente real, você precisaria integrar uma solução de automação de navegador (como Selenium) para interagir com a página web de forma efetiva. As linhas comentadas no `login_and_clock_in` mostram onde essa lógica seria implementada.

### 6. Executar o Aplicativo Flask

Com todas as dependências instaladas e as credenciais configuradas, você pode iniciar o servidor Flask:

```bash
source venv/bin/activate # Se ainda não estiver ativado
python src/main.py
```

O aplicativo será executado em `http://0.0.0.0:5000`. Você verá mensagens no console indicando que as tarefas de marcação de ponto foram agendadas.

## Como Funciona o Agendamento

O aplicativo utiliza o `APScheduler` para agendar as tarefas de marcação de ponto. As tarefas são configuradas para serem executadas de segunda a sexta-feira nos seguintes intervalos aleatórios:

- **Saída do Almoço:** Entre 12:28 e 12:32
- **Entrada do Almoço:** Entre 13:28 e 13:32
- **Final do Expediente:** Entre 17:30 e 17:35

Quando o aplicativo Flask é iniciado, ele configura esses agendamentos. O script `clocking_script.py` é então chamado nos horários agendados para simular a marcação do ponto. Cada execução do script seleciona um minuto e segundo aleatórios dentro do intervalo especificado para adicionar uma variação à marcação.

## Rotas da API (Opcional)

Embora o agendamento seja automático, o aplicativo também expõe rotas POST para acionar as marcações manualmente (principalmente para testes):

- `POST /api/mark_lunch_out`: Marca a saída do almoço.
- `POST /api/mark_lunch_in`: Marca a entrada do almoço.
- `POST /api/mark_end_of_day`: Marca o final do expediente.

Você pode testar essas rotas usando ferramentas como `curl` ou Postman:

```bash
curl -X POST http://localhost:5000/api/mark_lunch_out
```

## Observações

- O script `clocking_script.py` atualmente apenas **simula** a marcação de ponto. Para uma automação real, a seção `login_and_clock_in` precisaria ser implementada com uma biblioteca de automação de navegador (ex: Selenium, Playwright) para interagir com a página web da Senior.
- A verificação de feriados não está implementada. O agendamento ocorre de segunda a sexta, independentemente de feriados.





## 7. Configuração do Selenium (para automação real)

Para que a marcação de ponto funcione de forma automatizada e real, você precisará configurar o Selenium e um WebDriver (como o ChromeDriver).

### 7.1. Instalar o ChromeDriver

Baixe o ChromeDriver compatível com a versão do seu navegador Google Chrome. Você pode encontrá-lo em [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).

Após baixar, extraia o executável `chromedriver` e coloque-o em um diretório que esteja no seu `PATH` do sistema, ou especifique o caminho completo no `clocking_script.py`.

### 7.2. Configurar o `clocking_script.py`

O arquivo `src/clocking_script.py` já foi atualizado para incluir a lógica do Selenium. Certifique-se de que as credenciais `USERNAME` e `PASSWORD` estejam corretas. Se você precisar especificar o caminho do ChromeDriver, modifique a linha `driver = webdriver.Chrome(options=options)` para incluir o `executable_path`:

```python
driver = webdriver.Chrome(executable_path="/caminho/para/seu/chromedriver", options=options)
```

### 7.3. Executar em modo Headless (sem interface gráfica)

Por padrão, o script está configurado para rodar em modo headless (`options.add_argument('--headless')`), o que significa que o navegador não será exibido. Se você quiser ver o navegador em ação (para depuração, por exemplo), comente ou remova essa linha:

```python
# options.add_argument('--headless')
```

## Observações Importantes sobre o Selenium

- **Dependências:** O `requirements.txt` já foi atualizado para incluir o `selenium`.
- **Estabilidade:** A automação de navegador pode ser frágil. Pequenas mudanças na página web da Senior podem exigir atualizações no `clocking_script.py`.
- **Segurança:** Mantenha suas credenciais seguras e evite compartilhá-las. Considere usar variáveis de ambiente para armazenar `USERNAME` e `PASSWORD` em um ambiente de produção.


