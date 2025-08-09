from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stoots-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stoots.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos do banco de dados
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    investor_level = db.Column(db.String(50), default='Iniciante')
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)
    activities = db.relationship('Activity', backref='user', lazy=True)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), default='pessoal')  # pessoal, empresarial, familiar
    total_value = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    assets = db.relationship('Asset', backref='portfolio', lazy=True)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # acao, fundo, cdb, etc
    quantity = db.Column(db.Float, default=0.0)
    unit_price = db.Column(db.Float, default=0.0)
    total_value = db.Column(db.Float, default=0.0)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    deadline = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # receita, despesa, meta, video
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    points = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas
@app.route('/')
def index():
    return render_template('splash.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe', 'error')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            name=name
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Dados do dashboard financeiro - começa do zero
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    total_balance = sum([p.total_value for p in portfolios])
    monthly_contribution = 0.0  # Começa do zero
    portfolio_return = 0.0  # Começa do zero
    
    # Atividades recentes
    recent_activities = Activity.query.filter_by(user_id=current_user.id).order_by(Activity.created_at.desc()).limit(3).all()
    
    # Próximas metas
    upcoming_goals = Goal.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html',
                         total_balance=total_balance,
                         monthly_contribution=monthly_contribution,
                         portfolio_return=portfolio_return,
                         recent_activities=recent_activities,
                         upcoming_goals=upcoming_goals,
                         portfolios=portfolios)

@app.route('/expenses')
@login_required
def expenses():
    return render_template('expenses.html')

@app.route('/goals')
@login_required
def goals():
    return render_template('goals.html')

@app.route('/gamification')
@login_required
def gamification():
    return render_template('gamification.html')

@app.route('/education')
@login_required
def education():
    return render_template('education.html')

@app.route('/investments')
@login_required
def investments():
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    return render_template('investments.html', portfolios=portfolios)

@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

# APIs Interativas
@app.route('/api/create_portfolio', methods=['POST'])
@login_required
def create_portfolio():
    data = request.get_json()
    portfolio = Portfolio(
        name=data['name'],
        type=data.get('type', 'pessoal'),
        user_id=current_user.id
    )
    db.session.add(portfolio)
    db.session.commit()
    
    # Adiciona atividade
    activity = Activity(
        type='portfolio',
        description=f'Carteira "{data["name"]}" criada',
        points=10,
        user_id=current_user.id
    )
    db.session.add(activity)
    current_user.points += 10
    db.session.commit()
    
    return jsonify({
        'success': True,
        'portfolio': {
            'id': portfolio.id,
            'name': portfolio.name,
            'type': portfolio.type,
            'total_value': portfolio.total_value
        }
    })

@app.route('/api/add_asset', methods=['POST'])
@login_required
def add_asset():
    data = request.get_json()
    portfolio = Portfolio.query.get(data['portfolio_id'])
    
    if not portfolio or portfolio.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Portfolio não encontrado'})
    
    asset = Asset(
        name=data['name'],
        type=data['type'],
        quantity=data['quantity'],
        unit_price=data['unit_price'],
        total_value=data['quantity'] * data['unit_price'],
        portfolio_id=portfolio.id
    )
    db.session.add(asset)
    
    # Atualiza valor total do portfolio
    portfolio.total_value += asset.total_value
    db.session.commit()
    
    # Adiciona atividade
    activity = Activity(
        type='asset',
        description=f'Ativo "{data["name"]}" adicionado',
        amount=asset.total_value,
        points=5,
        user_id=current_user.id
    )
    db.session.add(activity)
    current_user.points += 5
    db.session.commit()
    
    return jsonify({
        'success': True,
        'asset': {
            'id': asset.id,
            'name': asset.name,
            'type': asset.type,
            'quantity': asset.quantity,
            'unit_price': asset.unit_price,
            'total_value': asset.total_value
        }
    })

@app.route('/api/update_asset', methods=['POST'])
@login_required
def update_asset():
    data = request.get_json()
    asset = Asset.query.get(data['asset_id'])
    
    if not asset or asset.portfolio.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Ativo não encontrado'})
    
    old_value = asset.total_value
    asset.quantity = data['quantity']
    asset.unit_price = data['unit_price']
    asset.total_value = data['quantity'] * data['unit_price']
    
    # Atualiza valor total do portfolio
    portfolio = asset.portfolio
    portfolio.total_value = portfolio.total_value - old_value + asset.total_value
    db.session.commit()
    
    return jsonify({
        'success': True,
        'asset': {
            'id': asset.id,
            'name': asset.name,
            'type': asset.type,
            'quantity': asset.quantity,
            'unit_price': asset.unit_price,
            'total_value': asset.total_value
        }
    })

@app.route('/api/delete_asset', methods=['POST'])
@login_required
def delete_asset():
    data = request.get_json()
    asset = Asset.query.get(data['asset_id'])
    
    if not asset or asset.portfolio.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Ativo não encontrado'})
    
    portfolio = asset.portfolio
    portfolio.total_value -= asset.total_value
    db.session.delete(asset)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/get_portfolio_data', methods=['GET'])
@login_required
def get_portfolio_data():
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    
    portfolio_data = []
    for portfolio in portfolios:
        assets = []
        for asset in portfolio.assets:
            assets.append({
                'id': asset.id,
                'name': asset.name,
                'type': asset.type,
                'quantity': asset.quantity,
                'unit_price': asset.unit_price,
                'total_value': asset.total_value
            })
        
        portfolio_data.append({
            'id': portfolio.id,
            'name': portfolio.name,
            'type': portfolio.type,
            'total_value': portfolio.total_value,
            'assets': assets
        })
    
    total_balance = sum([p.total_value for p in portfolios])
    
    return jsonify({
        'success': True,
        'portfolios': portfolio_data,
        'total_balance': total_balance
    })

@app.route('/api/add_activity', methods=['POST'])
@login_required
def add_activity():
    data = request.get_json()
    activity = Activity(
        type=data['type'],
        description=data['description'],
        amount=data.get('amount', 0),
        points=data.get('points', 0),
        user_id=current_user.id
    )
    db.session.add(activity)
    current_user.points += data.get('points', 0)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/add_goal', methods=['POST'])
@login_required
def add_goal():
    data = request.get_json()
    goal = Goal(
        name=data['name'],
        target_amount=data['target_amount'],
        deadline=datetime.strptime(data['deadline'], '%Y-%m-%d').date(),
        user_id=current_user.id
    )
    db.session.add(goal)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 