class GlColor:
    PUSH = 0xff8000
    MERGE = 0x1e90ff
    ISSUE = 0x00ff33


class GlUser:
    def __init__(self):
        self.name = ''
        self.username = ''
        self.avatar_url = ''
        self.url = ''

    @staticmethod
    def parse_json(json_in):
        user = GlUser()
        user.name = json_in['name']
        user.username = json_in['username']
        user.avatar_url = json_in['avatar_url']
        return user

    @staticmethod
    def parse_json_2(json_in):
        user = GlUser()
        user.name = json_in['user_name']
        user.username = json_in['user_username']
        user.avatar_url = json_in['user_avatar']
        return user


class GlProject:
    def __init__(self):
        self.name = ''
        self.description = ''
        self.web_url = ''
        self.avatar_url = ''
        self.full_path = ''
        self.namespace = ''
        self.default_branch = ''

    @staticmethod
    def parse_json(json_in):
        project = GlProject
        project.name = json_in['name']
        project.description = json_in['description'] if json_in['description'] is not None else ''
        project.web_url = json_in['web_url']
        project.avatar_url = json_in['avatar_url']
        project.full_path = json_in['path_with_namespace']
        project.namespace = json_in['namespace']
        project.default_branch = json_in['default_branch']
        return project


class GlIssue:
    def __init__(self):
        self.title = ''
        self.description = ''
        self.created_date = ''
        self.closed_date = ''
        self.state = ''
        self.url = ''
        self.assignees = []

    @staticmethod
    def parse_json(json_in):
        issue = GlIssue
        issue.title = json_in['title']
        issue.description = json_in['description'] if json_in['description'] is not None else ''
        issue.state = json_in['state']
        issue.created_date = json_in['created_at']
        issue.closed_date = json_in['closed_at']
        issue.url = json_in['url']
        return issue


class GlCommit:
    def __init__(self):
        self.id = ''
        self.message = ''
        self.timestamp = ''
        self.url = ''

    @staticmethod
    def parse_json(json_in):
        commit = GlCommit()
        commit.id = json_in['id']
        commit.message = json_in['message']
        commit.timestamp = json_in['timestamp']
        commit.url = json_in['url']
        return commit

    @staticmethod
    def parse_commits_json(json_in):
        commits = []
        for commit_json in json_in:
            commits.append(GlCommit.parse_json(commit_json))
        return commits


class GlMergeRequest:
    def __init__(self):
        self.title = ''
        self.assignee = None
        self.project = None
        self.description = ''
        self.url = ''
        self.user = None
        self.state = ''
        self.id = 0
        self.source_branch = ''
        self.target_branch = ''

    @staticmethod
    def parse_json(json_in):
        merge_request = GlMergeRequest()
        merge_request.title = json_in['object_attributes']['title']
        merge_request.url = json_in['object_attributes']['url']
        merge_request.state = json_in['object_attributes']['state']
        merge_request.source_branch = json_in['object_attributes']['source_branch']
        merge_request.target_branch = json_in['object_attributes']['target_branch']
        merge_request.id = json_in['object_attributes']['iid']
        merge_request.description = json_in['object_attributes']['description'] \
            if json_in['object_attributes']['description'] is not None else ''
        if 'assignee' in json_in and json_in['assignee'] is not None:
            merge_request.assignee = GlUser.parse_json(json_in['assignee'])
        merge_request.project = GlProject.parse_json(json_in['project'])
        merge_request.user = GlUser.parse_json(json_in['user'])
        return merge_request
