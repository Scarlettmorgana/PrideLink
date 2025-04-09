from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import csv

# Inicializar o objeto Flask
app = Flask(__name__)

# Dicionário para armazenar os dados dos usuários durante o fluxo
users_data = {}

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    try:
        # Registrar no terminal que o webhook recebeu uma solicitação
        print("Recebendo requisição no webhook...")

        # Obter informações da mensagem recebida
        from_number = request.form.get('From')  # Número do remetente
        incoming_msg = request.form.get('Body').strip().lower()  # Mensagem recebida

        print(f"Mensagem recebida de {from_number}: {incoming_msg}")  # Para depuração

        # Iniciar resposta Twilio
        response = MessagingResponse()

        # Verificar se o usuário já está no fluxo
        if from_number not in users_data:
            users_data[from_number] = {"step": 1}  # Iniciar o fluxo no passo 1

        # Identificar o passo atual do fluxo
        step = users_data[from_number]["step"]

        # Fluxo de perguntas baseado no passo atual
        if step == 1:
            response.message("Como você se descreveria em poucas palavras?")
            users_data[from_number]["step"] = 2
            users_data[from_number]["bio"] = incoming_msg
        elif step == 2:
            response.message("Qual cidade você mora atualmente?")
            users_data[from_number]["step"] = 3
            users_data[from_number]["location"] = incoming_msg
        elif step == 3:
            response.message("Você prefere relacionamentos casuais ou sérios?")
            users_data[from_number]["step"] = 4
            users_data[from_number]["relationship"] = incoming_msg
        elif step == 4:
            response.message("Quais são seus hobbies favoritos? (Ex.: esportes, sinuca, action figures)")
            users_data[from_number]["step"] = 5
            users_data[from_number]["hobbies"] = incoming_msg
        elif step == 5:
            response.message("Quais são seus interesses? (Ex.: vídeo game, séries, política, música)")
            users_data[from_number]["step"] = 6
            users_data[from_number]["interests"] = incoming_msg
        elif step == 6:
            response.message("Quais são seus cantores favoritos?")
            users_data[from_number]["step"] = 7
            users_data[from_number]["music"] = incoming_msg
        elif step == 7:
            response.message("Quais séries você ama assistir?")
            users_data[from_number]["step"] = 8
            users_data[from_number]["series"] = incoming_msg
        elif step == 8:
            response.message("Qual é a data do seu aniversário? (Ex.: 15/08/1990)")
            users_data[from_number]["step"] = 9
            users_data[from_number]["birthday"] = incoming_msg
        elif step == 9:
            response.message("Qual país você sonha em conhecer?")
            users_data[from_number]["step"] = "completed"
            users_data[from_number]["dream_country"] = incoming_msg
            response.message("Obrigado por compartilhar suas informações! Estamos processando seus dados para encontrar conexões incríveis.")

            # Salvar os dados no arquivo CSV
            with open('dados_usuarios.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Número", "Bio", "Localização", "Relacionamento", "Hobbies", "Interesses", "Cantores", "Séries", "Aniversário", "País dos Sonhos"])
                for number, data in users_data.items():
                    writer.writerow([
                        number,
                        data.get("bio", ""),
                        data.get("location", ""),
                        data.get("relationship", ""),
                        data.get("hobbies", ""),
                        data.get("interests", ""),
                        data.get("music", ""),
                        data.get("series", ""),
                        data.get("birthday", ""),
                        data.get("dream_country", "")
                    ])
                print("Dados salvos com sucesso no arquivo 'dados_usuarios.csv'!")
        else:
            response.message("Obrigado! Você já completou o formulário. Estamos processando seus dados.")

        # Retornar a resposta para o Twilio
        return str(response)

    except Exception as e:
        # Capturar e exibir erros no Terminal
        print(f"Erro ao processar mensagem: {e}")
        return "Erro interno no servidor", 500

@app.route('/dados', methods=['GET'])
def exibir_dados():
    try:
        # Estilo para a tabela
        html = """
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
        <h1>Dados dos Usuários</h1>
        <table>
            <tr>
                <th>Número</th>
                <th>Bio</th>
                <th>Localização</th>
                <th>Relacionamento</th>
                <th>Hobbies</th>
                <th>Interesses</th>
                <th>Cantores</th>
                <th>Séries</th>
                <th>Aniversário</th>
                <th>País dos Sonhos</th>
            </tr>
        """
        for number, data in users_data.items():
            html += f"<tr><td>{number}</td><td>{data.get('bio', '')}</td><td>{data.get('location', '')}</td><td>{data.get('relationship', '')}</td><td>{data.get('hobbies', '')}</td><td>{data.get('interests', '')}</td><td>{data.get('music', '')}</td><td>{data.get('series', '')}</td><td>{data.get('birthday', '')}</td><td>{data.get('dream_country', '')}</td></tr>"
        html += "</table>"
        return html
    except Exception as e:
        print(f"Erro ao exibir dados: {e}")
        return "Erro ao gerar página.", 500

# Iniciar o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)

