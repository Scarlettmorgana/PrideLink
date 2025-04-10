import sys
import os
from sqlalchemy.orm import sessionmaker
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
from math import radians, sin, cos, sqrt, atan2

# Garantir que o módulo 'database' seja acessível
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Imports dos módulos do projeto
from database.models import Usuario
from database.db_setup import engine

# Configuração do Token do Bot do Telegram
BOT_TOKEN = "8141665075:AAEGHkIre_-a2Qazk5vPjMqbeNaKsQ3SOjM"  # Substitua pelo seu token

# Conexão com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Dicionários para estados temporários
user_data = {}
edit_data = {}  # Armazena dados em edição
message_data = {}  # Armazena mensagens pendentes

# Função para calcular distância entre dois pontos geográficos
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Raio médio da Terra em quilômetros
    dlat = radians(lat2 - lat1)
    dlon = radians(lat2 - lon2)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Comando /start
async def start(update: Update, context: CallbackContext):
    print("Bot iniciado e ativo no Telegram.")
    await update.message.reply_text(
        "Olá! Bem-vindo ao PrideLinkBot! Use /register para começar ou /matches para encontrar conexões."
    )

# Comando /register
async def register(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_data[chat_id] = {}
    await update.message.reply_text("Qual é o seu nome?")
    return "nome"

# Processar respostas durante o registro
async def process_register(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    message = update.message.text

    if "nome" not in user_data[chat_id]:
        user_data[chat_id]["nome"] = message
        await update.message.reply_text("Qual é o seu telefone (com DDD)?")
        return "telefone"

    if "telefone" not in user_data[chat_id]:
        user_data[chat_id]["telefone"] = message
        await update.message.reply_text("Liste seus interesses (ex.: música:3, esportes:2):")
        return "interesses"

    if "interesses" not in user_data[chat_id]:
        user_data[chat_id]["interesses"] = message
        await update.message.reply_text("Descreva-se em uma frase:")
        return "descricao"

    if "descricao" not in user_data[chat_id]:
        user_data[chat_id]["descricao"] = message
        await update.message.reply_text("Qual é o seu gênero?")
        return "genero"

    if "genero" not in user_data[chat_id]:
        user_data[chat_id]["genero"] = message
        await update.message.reply_text("Qual é a sua preferência sexual?")
        return "preferencia"

    if "preferencia" not in user_data[chat_id]:
        user_data[chat_id]["preferencia"] = message
        cadastrar_usuario(user_data[chat_id], chat_id)
        await update.message.reply_text("Cadastro concluído! Use /edit para editar ou /matches para buscar conexões.")
        del user_data[chat_id]

# Comando /edit
async def edit(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    keyboard = [
        [InlineKeyboardButton("Editar Nome", callback_data="edit_nome")],
        [InlineKeyboardButton("Editar Telefone", callback_data="edit_telefone")],
        [InlineKeyboardButton("Editar Interesses", callback_data="edit_interesses")],
        [InlineKeyboardButton("Editar Descrição", callback_data="edit_descricao")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("O que você gostaria de editar?", reply_markup=reply_markup)

# Processar edição
async def process_edit(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = query.data

    if data.startswith("edit_"):
        campo = data.split("_")[1]
        edit_data[chat_id] = campo
        await query.message.reply_text(f"Digite o novo valor para {campo}:")

# Finalizar edição e atualizar no banco
async def finalize_edit(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    novo_valor = update.message.text

    if chat_id in edit_data:
        campo = edit_data[chat_id]
        try:
            usuario = session.query(Usuario).filter(Usuario.chat_id == chat_id).first()
            setattr(usuario, campo, novo_valor)
            session.commit()
            await update.message.reply_text(f"{campo.capitalize()} atualizado com sucesso para: {novo_valor}!")
        except Exception as e:
            session.rollback()
            await update.message.reply_text("Erro ao atualizar. Tente novamente.")
        finally:
            del edit_data[chat_id]

# Função para cadastrar no banco de dados
def cadastrar_usuario(dados_usuario, chat_id):
    try:
        usuario = Usuario(
            nome=dados_usuario["nome"],
            telefone=dados_usuario["telefone"],
            interesses=dados_usuario["interesses"],
            descricao=dados_usuario["descricao"],
            genero=dados_usuario["genero"],
            preferencia_sexual=dados_usuario["preferencia"],
            chat_id=chat_id
        )
        session.add(usuario)
        session.commit()
        print(f"Usuário {dados_usuario['nome']} cadastrado com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao cadastrar usuário: {str(e)}")

# Configuração do bot
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("edit", edit))
    application.add_handler(CallbackQueryHandler(process_edit))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, finalize_edit))

    print("Bot está rodando...")
    application.run_polling()

if __name__ == "__main__":
    main()

