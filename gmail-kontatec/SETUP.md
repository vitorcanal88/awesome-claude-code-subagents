# 📖 Kontatec Gmail - Setup Detalhado

Configuração passo-a-passo completa para busca de emails Kontatec.

## 📋 Pré-requisitos

- Python 3.7+ instalado
- Conta Google com 2-Factor Authentication ativado
- Acesso à conta v.canal88@gmail.com (ou similar)
- Conexão com internet

## 🔧 Instalação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

Dependências necessárias:
- imaplib (built-in)
- email (built-in)
- json (built-in)
- pathlib (built-in)

### 2. Gerar App Password no Google

**Por que App Password?**
- Mais seguro que usar senha real
- Pode ser revogado/regenerado facilmente
- Acesso restrito apenas a Gmail

**Passos:**

1. Acesse: https://myaccount.google.com/apppasswords
   - Certifique-se de estar logado

2. Confirme **2-Factor Authentication** ativado:
   - Se não estiver, vá a: https://myaccount.google.com/security
   - Ative "2-Step Verification"

3. Em "App passwords":
   - **Select app:** Mail
   - **Select device:** Windows Computer (ou seu SO)
   - Clique: **Generate**

4. Google mostra uma senha assim:
   ```
   xxxx xxxx xxxx xxxx
   ```
   - **Copie exatamente** (sem espaços se quiser)
   - Você não verá novamente

## 🚀 Configurar Credenciais

### Run Setup Script

```bash
python3 setup_kontatec_auth.py
```

**Prompts:**

```
📧 Enter your Gmail address: v.canal88@gmail.com
🔐 Enter the 16-character App Password: xxxx xxxx xxxx xxxx
```

**O que acontece:**
1. Testa conexão IMAP com Gmail
2. Conta mensagens em INBOX
3. Salva credenciais em `~/.gmail/`:
   - `config.json` (email apenas)
   - `.apppass` (password protegida)

**Sucesso:**
```
✓ IMAP connection successful
✓ Found 1234 messages in INBOX
✓ Configuration saved to: /home/user/.gmail/config.json
✅ Authentication successful!
```

## 🔍 Buscar Emails

### Uso Básico

```bash
python3 search_kontatec_emails.py
```

Busca por padrão:
- `vitor.canal@kontatec.com.br`
- Últimas 100 mensagens

### Com Opções

```bash
# Output customizado
python3 search_kontatec_emails.py --output meus_resultados.json

# Email diferente
python3 search_kontatec_emails.py --email joao.silva@kontatec.com.br

# Ambos
python3 search_kontatec_emails.py \
  --email outro@kontatec.com.br \
  --output busca_2026.json
```

## 📊 Interpretar Resultados

### Estrutura JSON

```json
{
  "id": "174e1c84c45b12a5",
  "from": "João Silva <joao.silva@kontatec.com.br>",
  "to": "vitor.canal@kontatec.com.br",
  "subject": "Reunião de Projeto - Segunda",
  "date": "Wed, 09 Apr 2026 10:30:00 -0300",
  "body_preview": "Olá Vitor,\n\nComo discutido ontem...",
  "labels": ["INBOX", "IMPORTANT"]
}
```

### Campos

| Campo | Significado |
|-------|------------|
| `id` | ID único da mensagem |
| `from` | Quem enviou |
| `to` | Para quem foi enviado |
| `subject` | Assunto do email |
| `date` | Data/hora de envio |
| `body_preview` | Primeiros 500 caracteres |
| `labels` | Rótulos/categorias |

## 🔐 Segurança

### Credenciais

**Armazenadas em:**
```
~/.gmail/
├── config.json      (email - seguro)
└── .apppass         (senha - privado)
```

**Permissões:**
```bash
ls -la ~/.gmail/
-rw------- 1 user user  config.json
-rw------- 1 user user  .apppass
```

**Apenas o usuário pode ler!**

### .gitignore

Nunca commite credenciais:

```bash
# Adicione ao .gitignore:
.gmail/
~/.gmail/
*.pyc
__pycache__/
gmail_kontatec_results.json
```

### Regenerar App Password

Se comprometer a password:

1. Acesse: https://myaccount.google.com/apppasswords
2. Selecione o app "Mail"
3. Clique: **Delete**
4. Gere nova password
5. Delete `~/.gmail/.apppass`
6. Rode `python3 setup_kontatec_auth.py` novamente

## 🔍 Filtros Avançados

Edite `search_kontatec_emails.py` para customizar buscas:

### Por Data

```python
# Emails do último mês
query = 'to:vitor.canal@kontatec.com.br after:2026-03-09'

# Período específico
query = 'to:vitor.canal@kontatec.com.br after:2026-01-01 before:2026-03-31'
```

### Por Assunto

```python
query = 'to:vitor.canal@kontatec.com.br subject:"reunião"'
query = 'to:vitor.canal@kontatec.com.br subject:"proposta"'
```

### Por Labels

```python
# Apenas importante
query = 'to:vitor.canal@kontatec.com.br label:important'

# Excluir spam
query = 'to:vitor.canal@kontatec.com.br -label:spam'

# Não lido
query = 'to:vitor.canal@kontatec.com.br is:unread'
```

### Combinações

```python
query = 'to:vitor.canal@kontatec.com.br after:2026-03-01 subject:"projeto"'
```

## 📅 Automatizar com Cron

### Linux/Mac

```bash
# Edite crontab
crontab -e

# Adicione (buscar diariamente às 9h)
0 9 * * * cd /caminho/para/gmail-kontatec && python3 search_kontatec_emails.py
```

### Windows

Use Task Scheduler:

1. Abra "Task Scheduler"
2. "Create Basic Task"
3. Trigger: Diário
4. Action: `python3 search_kontatec_emails.py`
5. Location: `/caminho/para/gmail-kontatec/`

## 🐛 Troubleshooting

### "Authentication failed"

```
❌ Authentication error: [AUTHENTICATE] b'[AUTHENTICATIONFAILED]'
```

**Soluções:**
- Verifique que é a **App Password** (não senha regular)
- Confirme **2FA ativado** na conta
- Regenere a App Password no Google
- Delete `~/.gmail/.apppass` e rode setup novamente

### "Connection refused"

```
❌ Error: [Errno 111] Connection refused
```

**Soluções:**
- Verifique **conexão com internet**
- Firewall pode estar bloqueando IMAP
- Tente novamente em alguns momentos
- Teste: `telnet imap.gmail.com 993`

### "No messages found"

```
❌ No messages found
```

**Soluções:**
- Verifique o **email correto**
- Procure em diferentes **rótulos/labels**
- Tente **ampliar período de busca**
- Use `python3 search_kontatec_emails.py --email seu.email@kontatec.com.br`

### "Timeout"

```
socket.timeout: timed out
```

**Soluções:**
- Conexão lenta - aguarde e tente novamente
- Gmail pode estar temporariamente indisponível
- Tente em outro momento

## 📞 Suporte Adicional

### Debug Mode

Para entender o que está acontecendo:

```bash
# Ver logs detalhados
python3 -u search_kontatec_emails.py 2>&1 | tee debug.log

# Testar conexão IMAP manualmente
python3 -c "
import imaplib
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login('v.canal88@gmail.com', 'sua_app_password')
print('✓ Connected!')
"
```

### Reset Completo

Se tudo falhar:

```bash
# 1. Delete credenciais
rm -rf ~/.gmail/

# 2. Regenere App Password no Google

# 3. Setup novamente
python3 setup_kontatec_auth.py

# 4. Teste
python3 search_kontatec_emails.py
```

## ✅ Checklist de Setup

- [ ] Python 3.7+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] App Password gerado no Google
- [ ] `setup_kontatec_auth.py` rodou com sucesso
- [ ] `~/.gmail/` criado com credenciais
- [ ] `search_kontatec_emails.py` retornou resultados
- [ ] JSON com emails foi criado
- [ ] `.gitignore` atualizado (não commitar credenciais)

## 🎓 Próximas Ações

1. ✅ Credenciais configuradas
2. 📊 Resultados em JSON
3. 🔄 Integrar com seu código/análise
4. 📅 Considerar automação com cron
5. 🔐 Revisar segurança periodicamente

---

**Pronto para usar!** 🚀
