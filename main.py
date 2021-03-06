import os
from review.gitlab import commits_by
from review.slack import send_commits


def send_commits_on_review():
    """
    Job for sending commits from gitlab in slack channel
    """
    gitlab_url = os.environ.get("GITLAB_URL")
    project_id = os.environ.get("PROJECT_ID")
    project_path = os.environ.get("PROJECT_PATH")
    branches = os.environ.get("BRANCHES").split(',')
    stop_words = os.environ.get("COMMIT_TITLE_STOP_WORDS", "").split(",")
    private_token = os.environ.get("PRIVATE_TOKEN")

    assert len(gitlab_url) > 0
    assert len(project_id) > 0
    assert len(branches) > 0
    get_commits = commits_by(gitlab_url, private_token, stop_words)

    slack_url = os.environ.get("SLACK_URL")
    slack_channel = os.environ.get("SLACK_CHANNEL")
    assert len(slack_url) > 0
    assert len(slack_channel) > 0
    response_text = send_commits(
        get_commits(
            project_id=project_id,
            branches=branches,
            project_path=project_path
        ),
        slack_url,
        slack_channel
    )
    print(response_text)
