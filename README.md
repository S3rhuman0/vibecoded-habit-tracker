# vibecoded-habit-tracker

## Branch `so-biblioteca`: só a biblioteca de PDFs

Versão enxuta do site com **apenas a biblioteca e o leitor de PDF**, sem hábitos, tarefas, pomodoro, diário e dashboard.
A versão completa continua na branch `main`.

**O que tem aqui**

- Estante (lombadas ou lista), busca, estatísticas de leitura e progresso por livro.
- Leitor de PDF (pdf.js) com zoom, navegação por página, contagem do tempo lido e **modo noite** (tecla `D`).
- **Meta diária de leitura**, em minutos ou em páginas: barra de progresso, sequência de dias, aviso ao bater a meta
  e tira dos últimos 14 dias. Coloque `0` para desligar a meta.
- Temas, idioma (português/inglês) e tamanho da fonte.

**Dados compartilhados com a versão completa:** o `data/dados.json` e a pasta `livros/` são os mesmos nas duas branches.
Tudo o que esta versão não usa (hábitos, tarefas, diário...) é mantido no arquivo, então dá para alternar entre as
versões sem perder nada.

## Como rodar

O site precisa do `server.py` (só usa o Python padrão, não precisa instalar nada):

```
python server.py
```

Ele abre `http://localhost:8000`. Os livros ficam em `livros/` e os dados em `data/dados.json` (as duas pastas não vão para o GitHub).

### No celular (Termux)

```
pkg update
pkg install python git
git clone https://github.com/S3rhuman0/vibecoded-habit-tracker
cd vibecoded-habit-tracker
git checkout so-biblioteca
python server.py
```

Depois abra `http://localhost:8000` no navegador do celular. Para atualizar: `git pull`.
Para voltar à versão completa: `git checkout main`.

### No celular (Pydroid 3), sem Termux

1. Baixe o ZIP desta branch no GitHub e extraia numa pasta do celular.
2. No Pydroid 3, abra o `server.py` dessa pasta e toque em ▶.
3. Abra `http://localhost:8000` no navegador do celular e mantenha o Pydroid aberto.

Não foi testado num celular de verdade: o `server.py` só usa a biblioteca padrão do Python, então deve funcionar.
Se o Android encerrar o Pydroid em segundo plano, o site para de responder até você abrir o app de novo.
