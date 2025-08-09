# Stoots - Dashboard Financeiro

Uma aplicação web moderna para gestão financeira e investimentos, desenvolvida em Flask com interface dark elegante.

## 🎨 Design

### Paleta de Cores Dark
- **Fundo Principal**: Preto (#0a0a0a) e azul escuro (#1a1a2e)
- **Acentos**: 
  - Roxo (#8b5cf6) - Cor principal
  - Verde-água (#14b8a6) - Destaque
  - Azul turquesa (#06b6d4) - Informações
  - Laranja (#f97316) - Alertas e pontos

### Interface Moderna
- Layout responsivo com sidebar lateral
- Cards com efeitos hover e animações suaves
- Gráficos interativos com Chart.js
- Tipografia clara e legível

## 🚀 Funcionalidades

### Dashboard Principal (Investimentos)
- **Saldo Total da Carteira**: Visão geral do patrimônio
- **Valor Aplicado**: Capital investido
- **Aporte do Mês**: Contribuições mensais
- **Rentabilidade da Carteira**: Performance dos investimentos

### Gráfico de Pizza Interativo
- Distribuição da carteira por tipo de investimento
- Filtros por categoria (Renda Fixa, Variável, Internacional)
- Legendas coloridas e responsivas

### Menu Lateral
- **Dashboard**: Visão geral
- **Gastos** e **Metas**: Em desenvolvimento (marcados como "Em Breve")
- **Gamificação**: Sistema de pontos e conquistas
- **Educação**: Conteúdo educacional
- **Investimentos**: Dashboard principal (ativo)
- **Notificações**: Alertas e avisos
- **Configurações**: Preferências do usuário

## 🛠️ Tecnologias

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite
- **Gráficos**: Chart.js
- **Ícones**: Font Awesome
- **Autenticação**: Flask-Login

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd stoots2
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute a aplicação:
```bash
python app.py
```

6. Acesse no navegador:
```
http://localhost:5000
```

## 📊 Estrutura do Projeto

```
stoots2/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── static/
│   ├── css/
│   │   └── style.css     # Estilos dark theme
│   └── js/
│       └── main.js       # JavaScript principal
├── templates/
│   ├── base.html         # Template base
│   ├── dashboard.html    # Dashboard financeiro
│   └── ...              # Outros templates
└── instance/
    └── stoots.db        # Banco de dados SQLite
```

## 🎯 Próximas Funcionalidades

- [ ] Sistema completo de gastos
- [ ] Gestão de metas financeiras
- [ ] Integração com APIs de investimentos
- [ ] Relatórios detalhados
- [ ] Notificações push
- [ ] Modo offline

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Stoots** - Transformando a gestão financeira com tecnologia e design moderno. 