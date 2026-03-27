# cotacao-dolar-email

Envio automático diário da cotação do dólar (USD/BRL) por e-mail usando GitHub Actions. Todo dia útil às 9h (horário de Brasília), o script busca a taxa oficial no Banco Central do Brasil (API PTAX) e envia um e-mail em HTML para um ou mais destinatários.

## Como funciona

1. O GitHub Actions dispara o workflow de segunda a sexta às 09:00 BRT (12:00 UTC).
2. O script consulta a [API PTAX do Banco Central](https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3) para obter a cotação mais recente do USD/BRL.
   - Se a API do BCB falhar (ex.: feriado sem cotação publicada), o script usa a [AwesomeAPI](https://economia.awesomeapi.com.br/) como fallback.
   - O script retrocede até 4 dias anteriores para lidar com fins de semana e feriados.
3. Um e-mail em HTML com as taxas de compra e venda é enviado via Gmail SMTP.

## Configuração

### 1. Faça um fork ou clone este repositório

### 2. Configure o Gmail

Ative as [Senhas de app](https://myaccount.google.com/apppasswords) na sua conta Google (requer verificação em duas etapas). Use a senha gerada como `EMAIL_PASSWORD`.

### 3. Adicione os Secrets do GitHub

Acesse **Settings → Secrets and variables → Actions** e adicione:

| Secret | Descrição |
|--------|-----------|
| `EMAIL_FROM` | Endereço Gmail remetente (ex.: `voce@gmail.com`) |
| `EMAIL_TO` | Endereço(s) destinatário(s), separados por vírgula (ex.: `a@exemplo.com,b@exemplo.com`) |
| `EMAIL_PASSWORD` | Senha de app do Gmail |

### 4. Ative o GitHub Actions

O workflow é executado automaticamente. Você também pode dispará-lo manualmente em **Actions → Cotação Diária do Dólar → Run workflow**.

## Estrutura do projeto

```
cotacao-dolar-email/
├── cotacao_dolar.py               # Script principal
├── requirements.txt               # Dependências Python
└── .github/workflows/
    └── cotacao_diaria.yml         # Workflow do GitHub Actions
```

## Fontes de dados

- **Principal:** [Banco Central do Brasil — PTAX](https://www.bcb.gov.br/estabilidadefinanceira/taxasdecambio) (oficial, sem limite de requisições)
- **Fallback:** [AwesomeAPI](https://economia.awesomeapi.com.br/)

## Requisitos

- Python 3.12+
- `requests` 2.32.3

## Licença

MIT
