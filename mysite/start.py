#!/usr/bin/env python3
# Author: Armit
# Create Time: 2022/10/14 

# local debug and test

from flask_app import app

if __name__ == '__main__':
  app.run(host='127.0.0.1', debug=True)
