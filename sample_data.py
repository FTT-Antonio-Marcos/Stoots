#!/usr/bin/env python3
"""
Script para adicionar dados de exemplo de investimentos ao banco de dados Stoots.
Execute este script após criar um usuário para popular o dashboard com dados realistas.
"""

from app import app, db, User, Portfolio, Asset
from datetime import datetime
import random

def create_sample_data():
    """Cria dados de exemplo para demonstração do dashboard financeiro."""
    
    with app.app_context():
        # Verifica se já existem dados
        if Portfolio.query.first():
            print("Dados de exemplo já existem. Pulando criação...")
            return
        
        # Busca o primeiro usuário (assume que já existe)
        user = User.query.first()
        if not user:
            print("Nenhum usuário encontrado. Crie um usuário primeiro.")
            return
        
        print(f"Criando dados de exemplo para usuário: {user.name}")
        
        # Cria portfolio principal
        portfolio = Portfolio(
            name="Carteira Principal",
            type="pessoal",
            total_value=25000.0,
            user_id=user.id
        )
        db.session.add(portfolio)
        db.session.commit()
        
        # Cria ativos de exemplo
        assets_data = [
            {
                "name": "CDB Banco Inter",
                "type": "renda_fixa",
                "quantity": 10000.0,
                "unit_price": 1.0,
                "total_value": 10000.0
            },
            {
                "name": "PETR4",
                "type": "acao",
                "quantity": 100.0,
                "unit_price": 28.50,
                "total_value": 2850.0
            },
            {
                "name": "VALE3",
                "type": "acao",
                "quantity": 50.0,
                "unit_price": 65.20,
                "total_value": 3260.0
            },
            {
                "name": "ITUB4",
                "type": "acao",
                "quantity": 80.0,
                "unit_price": 32.10,
                "total_value": 2568.0
            },
            {
                "name": "HGLG11",
                "type": "fii",
                "quantity": 50.0,
                "unit_price": 12.50,
                "total_value": 625.0
            },
            {
                "name": "XPML11",
                "type": "fii",
                "quantity": 30.0,
                "unit_price": 8.90,
                "total_value": 267.0
            },
            {
                "name": "Tesouro Selic 2025",
                "type": "tesouro",
                "quantity": 5000.0,
                "unit_price": 1.0,
                "total_value": 5000.0
            }
        ]
        
        for asset_data in assets_data:
            asset = Asset(
                name=asset_data["name"],
                type=asset_data["type"],
                quantity=asset_data["quantity"],
                unit_price=asset_data["unit_price"],
                total_value=asset_data["total_value"],
                portfolio_id=portfolio.id
            )
            db.session.add(asset)
        
        # Atualiza o valor total do portfolio
        portfolio.total_value = sum(asset["total_value"] for asset in assets_data)
        
        db.session.commit()
        
        print("✅ Dados de exemplo criados com sucesso!")
        print(f"📊 Portfolio criado: {portfolio.name}")
        print(f"💰 Valor total: R$ {portfolio.total_value:,.2f}")
        print(f"📈 {len(assets_data)} ativos adicionados")
        
        # Mostra distribuição da carteira
        print("\n📊 Distribuição da Carteira:")
        renda_fixa = sum(a["total_value"] for a in assets_data if a["type"] in ["renda_fixa", "tesouro"])
        acoes = sum(a["total_value"] for a in assets_data if a["type"] == "acao")
        fiis = sum(a["total_value"] for a in assets_data if a["type"] == "fii")
        
        total = portfolio.total_value
        print(f"   Renda Fixa: {renda_fixa/total*100:.1f}% (R$ {renda_fixa:,.2f})")
        print(f"   Ações: {acoes/total*100:.1f}% (R$ {acoes:,.2f})")
        print(f"   FIIs: {fiis/total*100:.1f}% (R$ {fiis:,.2f})")

if __name__ == "__main__":
    create_sample_data() 