# Kubernetes Ansible Playbooks
Ansible playbooks for deploying ansible applications in kubernetes.


## Getting Started

## Behaviour:

**Feature:** Deploy ansible Apps in Kubernetes clusters

These playbooks automated deployments to kubernetes.

- **Scenario:** Deploys an App to kubernetes
- **Given:** at least a kubeconfig is set up in local machine
- **Given:** at least a ssh public key exists in github repository
- **Given:** at least a circleCi token is linked to your account
- **Given:** a correctly configured vars file
- **When:** the playbook is executed
- **Then:** the k8s github is cloned or pulled
- **Then:** the build process for your app is checked on circleCi
- **Then:** the image tag is returned and replaced in your yaml file automatically. No need to add any regexp to do that.
- **Then:** the yaml file is applied to current context in kubernetes cluster.
- **Then:** the changes are pushed to github k8s repository.

#### Contexts and Extra Variables

Contexts can be seen as a logical entity used to represent cluster resources for usage of a particular set of users.

By default, the ansible playbooks have support to the following four contexts:

* Default - The default namespace used for testing purposes only.
* Review - The review context used for objects in the review environment.
* Staging - The staging context for objects in the staging environment.
* Production - The production context for objects in the production environment.

To use extra variables you can set by command line using `-e` flag or add new vars to `vars/<context>/vars.yml`. You can check defaults extra variables in [vars/required_var](vars/required_vars/required_vars.yml). In ansible playbooks, they are called required variables. You may add one or more required vars: add a slash + variable name before the latest one (i.e. `- github_pass`).

### Prerequisites

Before starting the automation with the Ansible Playbooks, you must install the ansible package:

* MacOS

```bash
$ brew install ansible
```
* Ubuntu
```bash
$ sudo apt install ansible
```

## Configuration

A list of the external variables used by the playbook.

| Variable  | Description  | Example  | Where set |
|---|---|---|---|
| **k8s_kubeconfig**  | A file path to kubernetes configuration hosted in your machine  |  ~/.kube/config | vars/\<context>/vars.yml |
| **k8s_context**  | The current kubernetes context that you are working on |  review, production, staging, develop | vars/\<context>/vars.yml |
| **github_repo**  | A github link (ssh) to kubernetes repository | git@github.com:ansible/k8s.git  | vars/\<context>/vars.yml |
| **github_dest**  | A destination path for cloning a k8s repository | ~/Documents/k8s | vars/\<context>/vars.yml |
| **github_ssh_keys**  | A file path to your ssh private key | ~/.ssh/id_rsa  | vars/\<context>/vars.yml |
| **github_message** | A commit message to your k8s yaml file | "feat: added yaml file"  | vars/\<context>/vars.yml |
| **github_version** | A github branch that you are working on k8s repository | review, production, staging, develop | vars/\<context>/vars.yml |
| **ansible_app** | The app name in github given for your application  | ansible, nginx, rabbitmq, postgres, so on... | vars/\<context>/vars.yml |
| **ansible_branch** | The branch name in github given that you have pushed  | develop-1313, review, master, hotfix-2168 | vars/\<context>/vars.yml |
| **files** | A file or list of files to k8s yaml file corresponding to your application that you are currently working on | app.yaml, ansible.yaml | vars/\<context>/vars.yml |
| **keys** | A list of keywords to replace in k8s yaml file: Regexp (word in your yaml file to be replaced) and line (value to replace) | Regexp: YOUR_PORT -> line: 5462 | vars/\<context>/vars.yml |

#### Configurating CircleCi

The ansible playbooks use the CircleCi API to access the build process and GitHub TAGS to fill up the yaml files dynamically. Follow the steps below to create your CircleCi token.

##### Creating a Personal API Token:

1) In the CircleCI application, go to your [User settings](https://circleci.com/account).

2) Click [Personal API Tokens](https://circleci.com/account/api).

3) Click the Create New Token button.

4) In the Token name field, type a memorable name for the token.

5) Click the Add API Token button.
After the token appears, copy and paste it to `CIRCLE_TOKEN` env variable. You will not be able to view the token again. To delete a personal API token, click the X in the Remove column.

6) Set up the `token_key` as your env variable as following:

```bash
$ export CIRCLE_TOKEN=your_key
```

## Running playbooks

Before running the Ansible playbooks, filled up the variables in `vars/<context>/vars.yml`.

The flag to `--ask-become-pass` is required to change the `image tag` and `keywords` in k8s yaml file.

1) Execute the automation:
```bash
$ ansible-playbook -i inventory/local -e "vars_file=../../vars/<context>/vars.yml" main.yml --ask-become-pass
```
2) To see the outputs, set the verbose flag `-vvvvv`

```bash
$ ansible-playbook -i inventory/local -e "vars_file=../../vars/<context>/vars.yml" main.yml -vvvvv --ask-become-pass
```

3) Set extra variables up with the verbose flag `-e EXTRA_VARIABLE=value`:

```bash
$ ansible-playbook -i inventory/local -e "vars_file=../../vars/<context>/vars.yml" main.yml -e github_repo=YOUR_GIT_REPO -e github_version=YOUR_GIT_VERSION --ask-become-pass
```

# TODO:

```
1. Install required packages using ansible-galaxy
2. Improvements in ansible playbooks
```
