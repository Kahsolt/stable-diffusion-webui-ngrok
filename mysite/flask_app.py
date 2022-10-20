#!/usr/bin/env python3
# Author: Armit
# Create Time: 2022/10/13 

from flask import Flask
from flask import redirect

import ngrok_utils as ngrok

app = Flask(__name__)


@app.route('/')
def index():
  return redirect('/ngrok/site')

@app.route('/stable-diffusion-webui')
def stable_diffusion_webui():
  return redirect('/ngrok/site')


@app.route('/ngrok/site')
def ngrok_site():
  ngrok.update_ngrok_info()

  public_urls = ngrok.get_ngrok_public_urls()
  if len(public_urls) == 0:
    return '<p> No ngrok public tunnels found, check the status info: <a href="/ngrok/status">Ngrok Debug</a> </p>'
  elif len(public_urls) == 1:
    return redirect(public_urls[0])
  else:
    return '<ul>{}</ul>'.format('\n'.join([f'<li><a href="{url}">{url}</a></li>' for url in public_urls]))

@app.route('/ngrok/status')
def ngrok_status():
  html = '<div><a href="/ngrok/refresh">Force Refresh State!!</a></div>\n'
  html += ngrok.format_ngrok_info_html()
  return html

@app.route('/ngrok/refresh')
def ngrok_refresh():
  ngrok.update_ngrok_info(hayaku=True)
  return redirect('/ngrok/status')
