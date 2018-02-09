from gln.discord import Webhook
from gln.gitlab import GlProject, GlUser, GlCommit, GlColor, GlMergeRequest, GlIssue
from gln.util import InvalidUsage, url_anchor


class GitlabProcessor(object):
    def __init__(self, config):
        self.config = config

    def get_webhook(self) -> Webhook:
        return Webhook(self.config['discord_webhook_url'])

    def set_private_project_image(self, project):
        if project.full_path in self.config['private_project_icons']:
            project.avatar_url = self.config['private_project_icons'][project.full_path]

    def process_request(self, request):
        if self.config['gitlab_token'] != '' and \
                request.headers.environ['HTTP_X_GITLAB_TOKEN'] != self.config['gitlab_token']:
            print('[ERROR] Invalid gitlab token')
            raise InvalidUsage('gitlab token invalid', status_code=403)

        header_event = request.headers.environ['HTTP_X_GITLAB_EVENT']

        if header_event == 'Push Hook':
            self.push_event(request.json)
        elif header_event == 'Merge Request Hook':
            self.merge_request_event(request.json)
        elif header_event == 'Issue Hook':
            self.issue_event(request.json)
        else:
            print('[ERROR] Unrecognized event')
            raise InvalidUsage('Unrecognized event', status_code=401)

    def push_event(self, event):
        project = GlProject.parse_json(event['project'])
        self.set_private_project_image(project)
        user = GlUser.parse_json_2(event)
        commits = GlCommit.parse_commits_json(event['commits'])

        webhook = self.get_webhook()
        webhook.set_author(name=user.name,
                           icon=user.avatar_url)

        webhook.set_footer(text=project.full_path,
                           icon=project.avatar_url,
                           ts=True)

        webhook.set_title(title='Git Push',
                          url=project.web_url)
        webhook.set_desc('Fresh push to ' + project.full_path)

        webhook.color = GlColor.PUSH
        webhook.set_thumbnail(url=self.config['git_icons']['push_icon'])

        count = 1
        for commit in commits:
            webhook.add_field(name='Commit #%d' % count,
                              value=url_anchor(commit.id[0:6], commit.url) + ' ' + commit.message,
                              inline=False)
            count += 1
        webhook.post()

    def merge_request_event(self, event):
        merge_request = GlMergeRequest.parse_json(event)
        self.set_private_project_image(merge_request.project)

        webhook = self.get_webhook()
        webhook.set_author(name=merge_request.user.name,
                           icon=merge_request.user.avatar_url)

        webhook.set_footer(text=merge_request.project.full_path,
                           icon=merge_request.project.avatar_url,
                           ts=True)

        webhook.color = GlColor.MERGE
        webhook.set_thumbnail(url=self.config['git_icons']['merge_icon'])

        webhook.set_title(title='Merge Request: ' + merge_request.title,
                          url=merge_request.url)
        webhook.set_desc(merge_request.description)

        webhook.add_field(name='Branch',
                          value=merge_request.source_branch + ' ↦ ' + merge_request.target_branch)

        webhook.add_field(name='Status',
                          value=merge_request.state)

        webhook.add_field(name='Assignee',
                          value=merge_request.assignee.name if merge_request.assignee is not None else '-')

        webhook.post()

    def issue_event(self, event):
        project = GlProject.parse_json(event['project'])
        self.set_private_project_image(project)
        user = GlUser.parse_json(event['user'])
        issue = GlIssue.parse_json(event['object_attributes'])

        webhook = self.get_webhook()
        webhook.set_author(name=user.name,
                           icon=user.avatar_url)

        webhook.set_footer(text=project.full_path,
                           icon=project.avatar_url,
                           ts=True)

        webhook.color = GlColor.ISSUE
        webhook.set_thumbnail(url=self.config['git_icons']['issue_icon'])

        webhook.set_title(title='Issue: ' + issue.title,
                          url=issue.url)

        webhook.set_desc(issue.description)

        webhook.add_field(name="Status",
                          value=issue.state)

        if 'assignees' in event and event['assignees'] is not None:
            assignees_text = ''
            for assignee in event['assignees']:
                assignees_text += assignee['name'] + '; '
        else:
            assignees_text = ''
        webhook.add_field(name='Assignees',
                          value=assignees_text)

        webhook.post()
