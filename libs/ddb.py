import boto3

from libs import settings
from libs.misc import hexdigest


_table = None


def get_table():
    global _table
    if _table is None:
        r = boto3.resource('dynamodb')
        r.Table()
        _table = settings.DDB_TABLE
    return _table


def get_partition_key(project: str, issue_id: str):
    return hexdigest(f'{project}/{issue_id}')


def create_issue(
    project: str,
    issue_id: str,
):
    pk = get_partition_key(project, issue_id)
    pass


def resolve_issue(
    project: str,
    issue_id: str,
):
    pass
