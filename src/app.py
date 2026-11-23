"""Aplicação web para gestão de tarefas da TechFlow Solutions."""
import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, abort

DB_DEFAULT = Path(__file__).resolve().parent.parent / 'tasks.db'
STATUS = ('A Fazer', 'Em Progresso', 'Concluído')
PRIORITIES = ('Baixa', 'Média', 'Alta')

def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates')
    app.config.update(DATABASE=os.environ.get('TECHFLOW_DB', str(DB_DEFAULT)), TESTING=False)
    if test_config:
        app.config.update(test_config)

    def connect():
        db = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        return db

    def initialize():
        with connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'Média',
                status TEXT NOT NULL DEFAULT 'A Fazer',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")

    initialize()

    def validate(form):
        title = form.get('title', '').strip()
        description = form.get('description', '').strip()
        priority = form.get('priority', 'Média')
        status = form.get('status', 'A Fazer')
        if not title or len(title) > 120 or len(description) > 1000:
            abort(400, description='Título obrigatório (até 120 caracteres); descrição até 1000.')
        if priority not in PRIORITIES or status not in STATUS:
            abort(400, description='Prioridade ou status inválido.')
        return title, description, priority, status

    @app.get('/')
    def index():
        status_filter = request.args.get('status', '')
        with connect() as db:
            if status_filter in STATUS:
                tasks = db.execute('SELECT * FROM tasks WHERE status=? ORDER BY id DESC', (status_filter,)).fetchall()
            else:
                tasks = db.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
        return render_template('index.html', tasks=tasks, statuses=STATUS, priorities=PRIORITIES, selected=status_filter)

    @app.post('/tasks')
    def create_task():
        title, description, priority, status = validate(request.form)
        with connect() as db:
            db.execute('INSERT INTO tasks(title, description, priority, status) VALUES (?, ?, ?, ?)',
                       (title, description, priority, status))
        return redirect(url_for('index'))

    @app.get('/tasks/<int:task_id>/edit')
    def edit_form(task_id):
        with connect() as db:
            task = db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
        if task is None:
            abort(404)
        return render_template('edit.html', task=task, statuses=STATUS, priorities=PRIORITIES)

    @app.post('/tasks/<int:task_id>/edit')
    def edit_task(task_id):
        title, description, priority, status = validate(request.form)
        with connect() as db:
            cur = db.execute('UPDATE tasks SET title=?, description=?, priority=?, status=? WHERE id=?',
                             (title, description, priority, status, task_id))
            if cur.rowcount == 0:
                abort(404)
        return redirect(url_for('index'))

    @app.post('/tasks/<int:task_id>/delete')
    def delete_task(task_id):
        with connect() as db:
            cur = db.execute('DELETE FROM tasks WHERE id=?', (task_id,))
            if cur.rowcount == 0:
                abort(404)
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    create_app().run(debug=False)
