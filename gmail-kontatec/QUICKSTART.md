# 🚀 Kontatec Gmail - Quick Start (3 minutos)

Comece a buscar emails Kontatec agora!

## Passo 1️⃣: Gerar Senha de App (1 min)

1. Acesse: **https://myaccount.google.com/apppasswords**
2. Selecione:
   - **App:** Mail
   - **Device:** Windows Computer
3. Copie a senha (16 caracteres)

## Passo 2️⃣: Setup (1 min)

```bash
python3 setup_kontatec_auth.py
```

Digite quando pedir:
- **Email:** `v.canal88@gmail.com` (ou seu email)
- **Password:** Cole a senha copiada

Verá:
```
✓ IMAP connection successful
✓ Found XXX messages in INBOX
✅ Authentication successful!
```

## Passo 3️⃣: Buscar Emails (1 min)

```bash
python3 search_kontatec_emails.py
```

## 📊 Resultado

```
🔍 Gmail Kontatec Search
📧 Searching for messages to: vitor.canal@kontatec.com.br
   → Found 150 messages

📊 GMAIL SEARCH RESULTS
📮 Messages to: vitor.canal@kontatec.com.br
   Count: 150
   [1] From: João Silva
       Subject: Reunião de Projeto
       Date: 09 Apr 2026
       Preview: Olá, vamos reagendar...

📈 SUMMARY STATISTICS
Total messages found: 150

✓ Results exported to: gmail_kontatec_results.json
```

## 📁 Arquivos Criados

- `~/.gmail/config.json` - Configuração (segura)
- `~/.gmail/.apppass` - Senha app (protegida)
- `gmail_kontatec_results.json` - Resultados da busca

## 🔍 Dados Exportados

Cada email tem:
- From (quem enviou)
- To (destinatário)
- Subject (assunto)
- Date (data)
- Body preview (primeiras 500 caracteres)
- Labels (rótulos/categorias)

## ⚙️ Opções Avançadas

```bash
# Output customizado
python3 search_kontatec_emails.py --output meus_emails.json

# Usar email diferente
python3 search_kontatec_emails.py --email outro.email@kontatec.com.br
```

## 🔒 Segurança

- Senha guardada em `~/.gmail/.apppass` (permissões 600)
- Não commitada ao git
- Pode regenerar anytime no Google

## ❌ Troubleshooting

| Erro | Solução |
|------|---------|
| "Invalid app password" | Use a senha de app (não a regular) |
| "Authentication failed" | Regenere a password no Google |
| "Connection timeout" | Verifique internet, tente novamente |
| "No messages" | Procure em diferentes rótulos |

## 🎓 Próximas Passos

1. ✅ Setup completo
2. 📊 Exportou resultados para JSON
3. 🔄 Usar no código/análise
4. 📅 Automatizar com cron (opcional)

## 📚 Mais Informações

- Guia completo: [SETUP.md](SETUP.md)
- Skill Claude Code: [gmail-kontatec-expert.md](.claude/agents/gmail-kontatec-expert.md)

---

**Pronto! Seus emails Kontatec estão em `gmail_kontatec_results.json`** 🎉
