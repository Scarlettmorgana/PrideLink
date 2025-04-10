import os
from twilio.rest import Client

# Carregar as credenciais da conta Twilio das variáveis de ambiente
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Enviar mensagem de boas-vindas
message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Bem-vindo ao Pridelink! 🎉 Responda algumas perguntas rápidas para encontrarmos conexões incríveis para você.',
    to='whatsapp:+5511932035224'
)

print(f"Mensagem enviada com SID: {message.sid}")
