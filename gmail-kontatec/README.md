# Gmail Kontatec - Email Search & Management

Suite completa para buscar, filtrar e gerenciar emails do domínio Kontatec de forma programática e segura.

## 🎯 Objetivo

Automatizar buscas de emails de endereços Kontatec:
- `vitor.canal@kontatec.com.br`
- Qualquer outro endereço @kontatec.com.br

## 📦 Conteúdo

### Scripts Python

- **`setup_kontatec_auth.py`** - Configuração segura de credenciais com App Password
- **`search_kontatec_emails.py`** - Script principal para buscar emails
- **`requirements.txt`** - Dependências Python

### Documentação

- **`README.md`** - Este arquivo
- **`QUICKSTART.md`** - Guia rápido de 3 minutos
- **`SETUP.md`** - Guia completo de configuração

### Claude Code Integration

- **`.claude/agents/gmail-kontatec-expert.md`** - Skill para usar com Claude Code

## 🚀 Quick Start

```bash
# 1. Setup (uma única vez)
python3 setup_kontatec_auth.py

# 2. Buscar emails
python3 search_kontatec_emails.py

# 3. Resultado
cat gmail_kontatec_results.json
```

## 🔍 Funcionalidades

### Busca Avançada

- ✅ Busca por destinatário
- ✅ Busca por remetente
- ✅ Busca por intervalo de datas
- ✅ Filtro por assunto
- ✅ Filtro por labels
- ✅ Extração de corpo da mensagem
- ✅ Exportação em JSON

### Segurança

- 🔒 Armazenamento seguro de credenciais
- 🔐 Autenticação via App Password do Google
- 🛡️ Permissões restritas em arquivos
- 📋 Sem armazenamento de senhas em texto plano

### Performance

- ⚡ Busca em lote (até 100 mensagens)
- 📊 Paginação automática
- 🔄 Cache inteligente
- 📈 Relatórios detalhados

## 📋 Pré-requisitos

- Python 3.7+
- Conta Google com 2FA habilitado
- Acesso ao Gmail
- Permissão para gerar App Password

## 🔧 Instalação

1. **Instale dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure credenciais:**
   ```bash
   python3 setup_kontatec_auth.py
   ```

3. **Comece a buscar:**
   ```bash
   python3 search_kontatec_emails.py
   ```

## 📊 Output

Resultados em JSON com estrutura:

```json
{
  "id": "message_id",
  "from": "sender@example.com",
  "to": "vitor.canal@kontatec.com.br",
  "subject": "Email Subject",
  "date": "Wed, 01 Jan 2026 10:00:00",
  "body_preview": "Email content preview...",
  "labels": ["INBOX", "IMPORTANT"]
}
```

## 🛠️ Uso Avançado

### Buscar com Filtros

Edite `search_kontatec_emails.py` para adicionar:

```python
# Por data
query = 'to:vitor.canal@kontatec.com.br after:2025-01-01'

# Por assunto
query = 'to:vitor.canal@kontatec.com.br subject:"meeting"'

# Excluir spam
query = 'to:vitor.canal@kontatec.com.br -label:spam'
```

### Integração com Claude Code

Use a skill `gmail-kontatec-expert` em Claude Code:

```
/invoke gmail-kontatec-expert
```

### Automação

Crie um cron job para buscas periódicas:

```bash
# Buscar emails diariamente
0 9 * * * cd /caminho/para/gmail-kontatec && python3 search_kontatec_emails.py
```

## 🔐 Segurança & Best Practices

1. **Gere App Password** (não use senha real)
2. **Armazene em `~/.gmail/`** (isolado)
3. **Adicione a `.gitignore`:**
   ```
   .gmail/
   gmail_kontatec_results.json
   *.pyc
   ```
4. **Rotacione credenciais** periodicamente
5. **Nunca commite credenciais** ao repositório

## 📚 Documentação Completa

- [QUICKSTART.md](QUICKSTART.md) - Comece em 3 minutos
- [SETUP.md](SETUP.md) - Configuração detalhada
- [Skill no Claude Code](.claude/agents/gmail-kontatec-expert.md)

## 🐛 Troubleshooting

### Erro: "Authentication failed"
- Verifique a senha de app (não a senha regular)
- Confirme 2FA ativado na conta Google
- Regenere a App Password

### Erro: "Connection timeout"
- Verifique conexão com internet
- Tente novamente em alguns momentos

### Erro: "No messages found"
- Confirme o email correto
- Verifique filtros de busca
- Procure em diferentes rótulos

## 📞 Suporte

Para dúvidas:
1. Consulte [SETUP.md](SETUP.md)
2. Verifique logs de erro
3. Teste conexão IMAP manualmente

## 📄 Licença

Use conforme necessário para fins internos da Kontatec.

## 🔄 Changelog

### v1.0.0 (2026-04-09)
- Initial release
- IMAP-based email search
- Secure credential storage
- JSON export
- Claude Code integration
