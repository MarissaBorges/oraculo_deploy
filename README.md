<!-- BADGES -->

[PYTHON_BADGE]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[STREAMLIT_BADGE]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[LANGCHAIN_BADGE]: https://img.shields.io/badge/LangChain-1A1A1A?style=flat&logo=langchain&logoColor=white

<!-- PROJECT -->
<h1 align="center" style="font-weight: bold;">Oráculo Mimir 🤖</h1>

<p align="center">
  <!-- Adicione aqui os badges das tecnologias que você usou -->
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit Badge">
  <img src="https://img.shields.io/badge/LangChain-1A1A1A?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain Badge">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Deployed%20on-Streamlit%20Cloud-FF4B4B?logo=streamlit&style=for-the-badge" alt="Deployed on Streamlit Cloud">
</p>

<p align="center">
 <a href="#-descrição">Descrição</a> • 
 <a href="#-funcionalidades">Funcionalidades</a> • 
 <a href="#-começando">Como Executar</a> • 
 <a href="#️-demonstrações-capturas-de-tela">Demonstrações</a> • 
 <a href="https://oraculomimir.streamlit.app/">Ver na Web</a>
</p>

---

## 📌 Descrição

O **Oráculo Mimir** é uma inteligência artificial desenvolvida para interagir com usuários, respondendo a dúvidas baseadas em dados fornecidos por diversas fontes. A ferramenta aceita arquivos em formatos como **PDF, CSV, TXT**, e também conteúdos de **links de sites** e **links do YouTube**.

Construído com base em **modelos de linguagem gratuitos** via `langchain-groq`, o Oráculo Mimir oferece a flexibilidade de escolha entre modelos como `"llama3-70b-8192"`, `"qwen/qwen3-32b"`, entre outros. A interface intuitiva permite inicializar o oráculo e limpar o histórico do chat com facilidade.

---

## 🚀 Funcionalidades

- **Interação com IA:** Responda a dúvidas do usuário com base em informações de diversas fontes.
- **Suporte a Múltiplas Fontes:** Carregamento de dados de **PDFs, CSVs, TXTs, links de sites e links do YouTube**.
- **Modelos de IA Gratuitos:** Escolha entre os modelos `"llama3-70b-8192"`, `"qwen/qwen3-32b"`, ` "deepseek-r1-distill-llama-70b"` e `"allam-2-7b"` via `langchain-groq`.
- **Controle de Chat:** Botões dedicados para **inicializar o oráculo** e **limpar o histórico de chat**.

---

## 🔒 Destaques Técnicos

- **RAG:** Técnica usada para aprimorar modelos de linguagem buscando informações de acordo com a pergunta nas fontes externas, gerando uma resposta precisa e relevante.
- **Memória em Cache:** Utilização de cache do Streamlit para otimizar o desempenho e evitar recarregamentos desnecessários de dados.
- **Contexto de Conversa:** O modelo considera o histórico completo da conversa para fornecer respostas mais coerentes.
- **Modularidade:** Módulos de código dedicados para carregar cada tipo de fonte de dados de forma independente.
- **Custo-Benefício:** Implementação focada exclusivamente em **modelos de IA gratuitos**, garantindo acessibilidade e escalabilidade.

---

## 📍Como Executar Localmente

Siga as instruções abaixo para executar o projeto em seu ambiente local.

### Pré-requisitos

- [Python](https://www.python.org/) (versão 3.9+)
- [Git](https://git-scm.com/)

### Clonando o Repositório

```bash
git clone https://github.com/MarissaBorges/oraculo_deploy.git

cd oraculo_deploy
```

### Variáveis de Ambiente

Este projeto utiliza a API da Groq para acessar os modelos de linguagem, por isso é necessário criar uma chave de API no [site oficial](https://console.groq.com/keys).

> Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```yaml
GROQ_API_KEY="SUA_CHAVE_DE_API_DA_GROQ_AQUI"
```

### Iniciando o Projeto

Crie um ambiente virtual para evitar conflito de dependências

```bash
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente
# No Windows:
.venv\Scripts\activate

# No macOS/Linux:
source .venv/bin/activate
```

Instale as dependências e inicie.

```bash
# Instale as dependências
pip install -r requirements.txt

# Inicie a aplicação com Streamlit
streamlit run app_oraculo.py
```

---

## 🖼️ Demonstrações (capturas de tela)

![Página Inicial do Oráculo](https://i.postimg.cc/F1tDPz5n/tela-inicial.png)
_Visão geral da página inicial e opções de fontes de dados._

![Seleção de Modelos e Interação](https://i.postimg.cc/0ykHh6KL/selecao-modelos.png)
_Usuário pode escolher o modelo de IA e interagir via chat._

![Interação com Conteúdo de Site](https://i.postimg.cc/WbX7F5tH/interacao-site.png)
_Exemplo de pergunta sobre um artigo da web carregado na plataforma._

---

## 📫 Como Contribuir

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será muito apreciada.

1. Faça um **Fork** do projeto.
2. Crie uma nova branch para sua Feature (`git checkout -b feature/AmazingFeature`).
3. Faça o **Commit** de suas mudanças (`git commit -m 'Add some AmazingFeature'`).
4. Faça o **Push** da sua branch (`git push origin feature/AmazingFeature`).
5. Abra um **Pull Request**.

### Documentações Úteis

- [📝 Como criar um Pull Request](https://www.atlassian.com/br/git/tutorials/making-a-pull-request)
- [💾 Padrão de Commits (Conventional Commits)](https://www.conventionalcommits.org/en/v1.0.0/)
