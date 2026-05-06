#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada WSGI para Render/Gunicorn
Importa la aplicación Flask desde servidor_todo_en_uno.py
"""

from servidor_todo_en_uno import app

if __name__ == '__main__':
    app.run()
