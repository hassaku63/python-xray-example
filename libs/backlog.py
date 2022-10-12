from typing import Union, Literal
import requests

from libs import logs
from libs import settings


log = logs.get_logger(__name__)

BASE_URL = f'https://{settings.BACKLOG_SPACE}.backlog.jp'
ISSUE_STATUS = Union[
    Literal['open'],
    Literal['inprogress'],
    Literal['resolve'],
]
_ISSUE_STATAUS_MAP = {
    'open': settings.BACKLOG_DEFAULT_ISSUE_CREATE_STATUS,
    'inprogress': settings.BACKLOG_DEFAULT_ISSUE_INPROGRESS_STATUS,
    'resolve': settings.BACKLOG_DEFAULT_ISSUE_RESOLVE_STATUS,
}


def _endpoint(path: str):
    return f'{BASE_URL}/api/v2/{path}'


def create_issue(
    project: str,
    subject: str,
    body: str,
):
    """https://developer.nulab.com/docs/backlog/api/2/add-issue/#role
    """
    resp = requests.post(
        url=_endpoint(f'issues?apiKey={settings.BACKLOG_API_KEY}'),
        headers={
            'Content-Type': 'application/w-www-form-urlencoded'
        },
        data={
            'projectId': project,
            'summary': subject,
            'description': body,
            'issueTypeId': settings.BACKLOG_DEFAULT_ISSUE_TYPE,
            'priorityId': settings.BACKLOG_DEFAULT_PRIORITY,
        }
    )
    log.info(_endpoint(f'issues/{id}?apiKey={settings.BACKLOG_API_KEY}'))
    log.info(f'{resp.headers}')
    return resp.json()


def change_issue_status(issue_id: str, status: ISSUE_STATUS):
    """https://developer.nulab.com/ja/docs/backlog/api/2/add-comment/#
    """
    resp = requests.patch(
        url=_endpoint(f'issues/{issue_id}?apiKey={settings.BACKLOG_API_KEY}'),
        headers={
            'Content-Type': 'application/w-www-form-urlencoded'
        },
        data={
            'statusId': _ISSUE_STATAUS_MAP[status],
        },
    )
    log.info(_endpoint(f'issues/{id}?apiKey={settings.BACKLOG_API_KEY}'))
    log.info(f'{resp.headers}')
    return resp.json()


def add_comment(issue_id: str, content: str):
    """https://developer.nulab.com/ja/docs/backlog/api/2/add-comment/#
    """
    url = _endpoint(f'issues/{issue_id}/comments?apiKey={settings.BACKLOG_API_KEY}')
    resp = requests.post(
        url=url,
        headers={
            'Content-Type': 'application/w-www-form-urlencoded',
        },
        data={
            'content': content,
        },
    )
    log.info(url)
    log.info(f'{resp.headers}')
    return resp.json()


#
# 以降は Step Functions の実装で利用しないので本題から逸れるが、開発中のちょっとした確認にあると便利なので残しておく
#
def list_projects(archived: bool=False):
    archived = 1 if archived else 0
    return requests.get(
        url=_endpoint(f'projects?apiKey={settings.BACKLOG_API_KEY}&archived={archived}')
    ).json()


def get_issue(id: str):
    resp = requests.get(
        url=_endpoint(f'issues/{id}?apiKey={settings.BACKLOG_API_KEY}')
    )
    log.info(_endpoint(f'issues/{id}?apiKey={settings.BACKLOG_API_KEY}\n'))
    log.info(f'{resp.headers}\n')
    return resp.json()


if __name__ == '__main__':
    import argparse
    import json

    def json_print(data):
        print(json.dumps(data))

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    get_issue_parser = subparsers.add_parser('get')
    create_issue_parser = subparsers.add_parser('create')
    resolve_issue_parser = subparsers.add_parser('resolve')
    inprogress_issue_parser = subparsers.add_parser('inprogress')
    list_projects_parser = subparsers.add_parser('list-project')

    get_issue_parser.set_defaults(_action='get')
    create_issue_parser.set_defaults(_action='create')
    resolve_issue_parser.set_defaults(_action='resolve')
    inprogress_issue_parser.set_defaults(_action='inprogress')
    list_projects_parser.set_defaults(_action='list-projects')

    get_issue_parser.add_argument('--id', required=True, type=str, dest='issue_id')
    resolve_issue_parser.add_argument('--id', required=True, type=str, dest='issue_id')
    inprogress_issue_parser.add_argument('--id', required=True, type=str, dest='issue_id')

    args = parser.parse_args()

    if args._action == 'get':
        json_print(get_issue(args.issue_id))
    elif args._action == 'create':
        json_print(create_issue(
            project=settings.BACKLOG_DEFAULT_PROJECT_ID,
            subject='test issue',
            body=(
                'アラート起票の本文\n\n'
                'てすと'
            )
        ))
    elif args._action == 'resolve':
        result = []
        result.append(change_issue_status(
            args.issue_id,
            'resolve',
        ))
        result.append(add_comment(
            args.issue_id,
            'issue が解決したので自動クローズ'
        ))
        json_print(result)
    elif args._action == 'inprogress':
        json_print(change_issue_status(
            args.issue_id,
            'inprogress',
        ))
    elif args._action == 'list-projects':
        json_print(list_projects())
