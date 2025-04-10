# PrideLink Bot

O PrideLink Bot é um assistente interativo desenvolvido para facilitar conexões e oferecer funcionalidades personalizadas. Ele suporta múltiplos idiomas e está pronto para integrar novas funcionalidades e linguagens, como o Espanhol.

## Funcionalidades
- Suporte aos idiomas Português e Espanhol (com personalização futura).
- Armazenamento de informações dos usuários.
- Personalização de notificações e configurações.
- Integração com APIs externas e webhooks.
- Sistema seguro para proteger informações sensíveis.

## Como Configurar
Siga os passos abaixo para rodar o bot localmente ou em uma plataforma como Heroku:

1. Clone o repositório:
    ```bash
    git clone <https://github.com/Scarlettmorgana/PrideLink>
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd PrideLinkBot
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente (TOKEN do Telegram, entre outros):
    - Crie um arquivo `.env` no diretório raiz.
    - Adicione suas credenciais no formato:
      ```
      TELEGRAM_TOKEN=seu_token_aqui
      ```

5. Inicie o bot:
    ```bash
    python pridelink_bot.py
    ```

## Deploy
Para publicar seu bot em uma plataforma como Heroku:
1. Certifique-se de que o arquivo `Procfile` está configurado corretamente.
2. Faça o commit das suas alterações e envie para o GitHub:
    ```bash
    git add .
    git commit -m "Preparando para deploy"
    git push origin main
    ```
3. Configure o aplicativo no Heroku e conecte-o ao repositório no GitHub.
4. Habilite o webhook seguindo as instruções no arquivo `webhook.py`.

## Como Contribuir
Quer ajudar a melhorar o PrideLink Bot? Siga estas etapas:

1. Faça um fork do repositório:
    ```bash
    git fork <https://github.com/Scarlettmorgana/PrideLink>
    ```

2. Crie uma branch para suas alterações:
    ```bash
    git checkout -b minha-branch
    ```

3. Faça suas modificações e commit:
    ```bash
    git add .
    git commit -m "Descrição das alterações"
    ```

4. Envie um pull request para revisão.

---

## Licença
Este projeto é de código aberto e pode ser utilizado para fins educacionais e profissionais. Consulte o arquivo LICENSE para mais detalhes.

---

Desenvolvido com 💻 e 💡 por PrideLink (Scarlett Morgana Amorim).
