import os
import smtplib
import requests
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_cotacao():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()["USDBRL"]

    return {
        "bid": float(data["bid"]),
        "ask": float(data["ask"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "pct_change": float(data["pctChange"]),
        "timestamp": datetime.fromtimestamp(int(data["timestamp"])).strftime(
            "%d/%m/%Y %H:%M"
        ),
    }


def build_email_body(cotacao):
    variacao_emoji = "📈" if cotacao["pct_change"] >= 0 else "📉"
    variacao_sinal = "+" if cotacao["pct_change"] >= 0 else ""
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    return f"""\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
    .container {{ max-width: 480px; margin: auto; background: #fff; border-radius: 10px;
                  padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
    h2 {{ color: #2c3e50; text-align: center; }}
    .rate {{ font-size: 42px; font-weight: bold; text-align: center; color: #27ae60; margin: 10px 0; }}
    .grid {{ display: flex; justify-content: space-around; margin: 20px 0; }}
    .cell {{ text-align: center; }}
    .label {{ font-size: 12px; color: #888; text-transform: uppercase; }}
    .value {{ font-size: 18px; font-weight: bold; color: #2c3e50; }}
    .change {{ text-align: center; font-size: 16px; margin: 10px 0; }}
    .footer {{ text-align: center; font-size: 11px; color: #aaa; margin-top: 20px; }}
  </style>
</head>
<body>
  <div class="container">
    <h2>💵 Cotação do Dólar — {data_hoje}</h2>
    <div class="rate">R$ {cotacao['bid']:.4f}</div>
    <div class="change">{variacao_emoji} Variação: {variacao_sinal}{cotacao['pct_change']:.2f}%</div>
    <div class="grid">
      <div class="cell">
        <div class="label">Compra</div>
        <div class="value">R$ {cotacao['bid']:.4f}</div>
      </div>
      <div class="cell">
        <div class="label">Venda</div>
        <div class="value">R$ {cotacao['ask']:.4f}</div>
      </div>
      <div class="cell">
        <div class="label">Máxima</div>
        <div class="value">R$ {cotacao['high']:.4f}</div>
      </div>
      <div class="cell">
        <div class="label">Mínima</div>
        <div class="value">R$ {cotacao['low']:.4f}</div>
      </div>
    </div>
    <div class="footer">
      Atualizado em: {cotacao['timestamp']}<br>
      Fonte: AwesomeAPI — economia.awesomeapi.com.br
    </div>
  </div>
</body>
</html>
"""


def send_email(cotacao):
    email_from = os.environ["EMAIL_FROM"]
    email_to = os.environ["EMAIL_TO"]
    password = os.environ["EMAIL_PASSWORD"]

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    subject = f"💵 Cotação do Dólar — {data_hoje} | R$ {cotacao['bid']:.4f}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = email_to

    html_body = build_email_body(cotacao)
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, msg.as_string())

    print(f"Email enviado para {email_to} | USD/BRL: R$ {cotacao['bid']:.4f}")


if __name__ == "__main__":
    cotacao = get_cotacao()
    send_email(cotacao)
