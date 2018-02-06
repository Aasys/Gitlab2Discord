import yaml
from flask import Flask, request

from gln.processor import GitlabProcessor

app = Flask(__name__)

print("Loading configuration from config.yml")

config = {}

try:
    with open('config.yml') as config_data:
        config = yaml.load(config_data)
        print(config)
    print('Server address      : %s' % config['server_address'])
    print('Server port         : %s' % config['server_port'])
    print('Gitlab token        : %s' % config['gitlab_token'])
    print('Discord webhook URL : %s' % config['discord_webhook_url'])
except:
    print('!!! Error loading configuration')
    exit(1)

GitlabProcessor = GitlabProcessor(config)


@app.route('/')
def root_get():
    return 'OK'


@app.route("/gitlab-feed", methods=["POST"])
def gitlab_feed():
    print("[NEW EVENT]", request.json)

    GitlabProcessor.process_request(request)

    return "OK"


if __name__ == '__main__':
    app.run(host=config['server_address'], port=config['server_port'])
