# stable-diffusion-webui-ngrok

    Tools for easy & stable public serving the stable-diffusion-webui app through ngrok tunnel from local PC ;)

----

Visit my demo :)

- forwarded sd-webui app: => [https://kahsolt.pythonanywhere.com/stable-diffusion-webui-lite](https://kahsolt.pythonanywhere.com/stable-diffusion-webui-lite)
- ngrok status page: => [https://kahsolt.pythonanywhere.com/ngrok/status](https://kahsolt.pythonanywhere.com/ngrok/status)


#### Step 1: setup stable-diffusion-webui

- follow guide of [https://github.com/AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- start `webui.bat` and wait for installation & startup :(
- `mklink /J sd-webui path/to/your/stable-diffusion-webui`

ℹ Check it: Now you should be able to visit the **local** service at `http://localhost:7860/`

#### Step 2: expose local service to public network

To forward the local site, you need two more tools: 1. a frp-like tool `ngrok` for NAT tunnels to bridge local service to public; 2. a panel webserver like `pythonanywhere` for a fixed domain name, step them up as follows:

- register a [ngrok](https://ngrok.com/) account (free plan is ok)
- download and unzip the `ngrok.exe` executable to root folder of this repo 
- create a `API_KEY`  in your dashboard and save it to file `mysite/API_KEY.txt` (remember that API_KEY is not the AUTH_TOKEN, it should be manually created)
- run `ngrok http 7860` to forward your webui app
- run the tracking flask site `python mysite/start.py`
  - visit `https://127.0.0.1:5000/` to check the domain redirecting is ok
  - visit `https://127.0.0.1:5000/ngrok/refresh` to check your ngrok tunnel is working

ℹ Check it: Now **everyone** should be able to visit your service through ngrok's tunnel like `http://xxxx-xxx-xxx-xxx-xx.xx.ngrok.io/` on public network, and you can track ngrok status via the local Flask app

However, the free plan of ngrok won't give you a fixed domain name, every time you restart ngrok manually or due to network errors, the service url will change, which makes the service rather unstable. Hence we need a fix domain name to track ngrok's dynamic-generated domain name. Luckily, `pythonanywhere.com` will do!

- register a [pythonanywhere](https://www.pythonanywhere.com) account (free plan is ok)
- now you have a free domain name like `<username>.pythonanywhere.com`
- deploy the tracking flask site to your pythonanywhere cloudserver, go to your pythonanywhere.com control panel 
  - in the File tab, upload `mysite` folder to overwrite your default WWWROOT (tipically `/home/<username>/mysite/`)
  - in the Webapps tab, **reload** your website and 
    - visit `https://<username>.pythonanywhere.com/` to check the domain redircting and app service is ok
    - visit `https://<username>.pythonanywhere.com/ngrok/refresh` to check ngrok tunnel is accessible & working

ℹ  Check it: Now everyone should be able to visit your service **redirected** from your public pythonanywhere site like `http://<username>.pythonanywhere.com/`

#### Step 3: start stable serving 

Once you've done the steps above without errors, next time you can directly run:

- run `run.cmd`

This will start both **webui server** and **ngrok client** locally<del>, together with an extra daemon thread to monitor, if either is dead unexpectly, the daemon will try to restart it automatically</del>. Don't forget that your pythonanywhere site on cloud will also track your ngrok status at `http://<username>.pythonanywhere.com/ngrok/status`.

ℹ Now, everything's perfectly done! Taker your time~ 😀

----

by Armit
2022/10/10
