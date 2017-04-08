# coding: utf-8
# Created by leo on 17-4-8.
"""
运行
"""
from app import create_app
from config import Config
from flask_script import Manager

app = create_app(Config)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
