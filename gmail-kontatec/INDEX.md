# 📑 Kontatec Gmail - Project Index

Estrutura completa e documentação de todos os arquivos.

## 📁 Estrutura de Diretórios

```
gmail-kontatec/
├── README.md                          # Overview do projeto
├── QUICKSTART.md                      # Guia rápido (3 minutos)
├── SETUP.md                           # Setup detalhado
├── INDEX.md                           # Este arquivo
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Dependências Python
├── setup_kontatec_auth.py             # Script de setup
├── search_kontatec_emails.py          # Script principal
└── .claude/
    └── agents/
        └── gmail-kontatec-expert.md   # Claude Code skill
```

## 📄 Arquivos de Documentação

### README.md
- **Propósito:** Overview geral do projeto
- **Conteúdo:** Funcionalidades, pré-requisitos, quick start
- **Leitura:** 5 minutos
- **Para quem:** Gerentes, desenvolvedores novos

### QUICKSTART.md
- **Propósito:** Guia rápido
- **Conteúdo:** 3 passos para começar
- **Leitura:** 3 minutos
- **Para quem:** Usuários com pressa

### SETUP.md
- **Propósito:** Guia completo de configuração
- **Conteúdo:** Passo-a-passo, troubleshooting, automação
- **Leitura:** 15 minutos
- **Para quem:** Administradores, DevOps

### INDEX.md
- **Propósito:** Estrutura do projeto
- **Conteúdo:** Descrição de todos os arquivos
- **Leitura:** Este arquivo
- **Para quem:** Desenvolvedores

## 🐍 Scripts Python

### setup_kontatec_auth.py
**Versão:** 1.0.0  
**Propósito:** Configurar credenciais do Gmail

**Como usar:**
```bash
python3 setup_kontatec_auth.py
```

**O que faz:**
1. Pede email e App Password
2. Testa conexão IMAP
3. Salva credenciais em `~/.gmail/`
4. Valida funcionalidade

**Dependências:**
- Python 3.7+
- Modules: imaplib, json, pathlib, getpass

**Saída:**
- `~/.gmail/config.json` (email)
- `~/.gmail/.apppass` (password)

**Tempo:** ~10 segundos

### search_kontatec_emails.py
**Versão:** 1.0.0  
**Propósito:** Buscar e exportar emails

**Como usar:**
```bash
python3 search_kontatec_emails.py
```

**Opções:**
```bash
--email seu@email.com          # Email diferente
--recipients list@emails.com   # Destinatários customizados
--output custom.json           # Arquivo de saída
```

**O que faz:**
1. Carrega credenciais salvas
2. Conecta ao Gmail IMAP
3. Busca mensagens
4. Extrai conteúdo
5. Exporta para JSON

**Dependências:**
- Python 3.7+
- Modules: imaplib, email, json

**Saída:**
- `gmail_kontatec_results.json`
- Console output com resumo

**Tempo:** Depende de quantidade de emails (10-60 segundos típico)

## 🛠️ Arquivos de Configuração

### requirements.txt
- **Conteúdo:** Dependências Python
- **Status:** Usa apenas stdlib (nenhuma dep externa)
- **Mantém:** Documentação de módulos usados

### .gitignore
- **Regras:** Credenciais, cache, resultados
- **Protege:** Archivos sensíveis
- **Excludes:**
  - `~/.gmail/` (credenciais)
  - `*.apppass` (senhas)
  - `gmail_kontatec_results.json` (resultados)
  - `__pycache__/` (cache Python)

## 🧠 Claude Code Integration

### gmail-kontatec-expert.md
- **Tipo:** Claude Code Skill/Subagent
- **Local:** `.claude/agents/`
- **Uso:** Integração com Claude Code
- **Funcionalidades:**
  - Email search planning
  - Query optimization
  - Data analysis
  - Security protocol
  - Integration patterns

**Como usar em Claude Code:**
```
/invoke gmail-kontatec-expert
```

## 📊 Fluxo de Dados

```
┌─────────────────────────────┐
│  setup_kontatec_auth.py     │
│  (Configuração uma vez)     │
└────────────┬────────────────┘
             │
             ▼
      ~/.gmail/ (credenciais)
             │
             ▼
┌─────────────────────────────┐
│  search_kontatec_emails.py  │
│  (Busca múltiplas vezes)    │
└────────────┬────────────────┘
             │
             ▼
   gmail_kontatec_results.json
             │
             ▼
    (análise/integração)
```

## 🔒 Segurança

### Arquivos Sensíveis
- `~/.gmail/config.json` - Email (mode 0o600)
- `~/.gmail/.apppass` - Password (mode 0o600)

### Proteção
- ✅ Arquivos com permissões restritas
- ✅ Credenciais fora do repositório
- ✅ .gitignore evita commits acidentais
- ✅ App Password (não senha real)

## 📈 Performance

**Configuração Inicial:**
- Time: ~10 segundos
- Actions: Teste IMAP, save credenciais

**Busca Típica:**
- Time: 20-60 segundos
- Quantidade: 100-200 emails
- Output: JSON estruturado

**Otimizações:**
- IMAP em SSL/TLS
- Paginação automática
- Cache local
- Processamento em lote

## 🚀 Próximos Passos

1. **Ler:** [QUICKSTART.md](QUICKSTART.md)
2. **Executar:** `python3 setup_kontatec_auth.py`
3. **Buscar:** `python3 search_kontatec_emails.py`
4. **Analisar:** `cat gmail_kontatec_results.json`
5. **Integrar:** Use em seu código/workflows

## 📞 Referências Rápidas

| Tarefa | Comando |
|--------|---------|
| Setup | `python3 setup_kontatec_auth.py` |
| Buscar | `python3 search_kontatec_emails.py` |
| Customizar | `--email email@kontatec.com.br --output custom.json` |
| Ver resultados | `cat gmail_kontatec_results.json \| jq` |
| Resetar | `rm -rf ~/.gmail/ && python3 setup_kontatec_auth.py` |

## 📝 Changelog

### v1.0.0 (2026-04-09)
- ✨ Initial release
- 🔐 Secure App Password authentication
- 📧 IMAP-based email search
- 💾 JSON export
- 🧠 Claude Code skill integration
- 📚 Complete documentation

---

**Última atualização:** 2026-04-09  
**Status:** Production Ready ✅
