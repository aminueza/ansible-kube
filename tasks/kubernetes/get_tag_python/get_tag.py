from circleclient import circleclient
import datetime
import os
import sys
import json

# The DockerHub API URL, replace 'org' and 'repo' accordingly.
ORG = "ansible"
REPO = sys.argv[1]
BRANCH = sys.argv[2]


def connection(circle_token=None):
    if circle_token:
        self_circle_token = circle_token
    elif os.environ.get('CIRCLE_TOKEN', None):
        self_circle_token = os.environ['CIRCLE_TOKEN']

    assert self_circle_token, ('You must supply a CircleCI token '
                               'in the environment variable CIRCLE_TOKEN or '
                               'via command line.')

    self_cci = circleclient.CircleClient(self_circle_token)
    return self_cci


def get_tag_build_info(self_cci, org_name, repo, branch_name):
    connection = self_cci
    builds = connection.build.recent(org_name, repo, branch=branch_name)
    message = json.dumps(builds)
    json_tag = json.loads(message)
    if not (json_tag[0]['vcs_tag'] is None):
        return(json_tag[0]['vcs_tag'])
    else:
        return str(json_tag[0]['branch']) + '_latest'


if __name__ == "__main__":
    conn = connection()
    build_num = get_tag_build_info(conn, ORG, REPO, BRANCH)
    print(build_num)
