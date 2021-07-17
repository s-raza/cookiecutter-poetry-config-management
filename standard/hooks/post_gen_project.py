import subprocess as sub
import json
import sys
import os
import platform


platform_ = platform.system()
shell_ = True if platform_ == 'Windows' else False


def run(msg, cmd_arr, stderr2out=False, print_output=False):

    print(f'{msg} ...', end='', flush=True)

    if stderr2out is False:
        res = sub.run(cmd_arr, stdout=sub.PIPE, stderr=sub.PIPE, shell=shell_)

        err = res.stderr.decode('latin1')

        if err == '':
            output = res.stdout.decode('latin1')
            if print_output is True:
                print(f'\n{output}\n')
            print('done')
            return output
        else:
            print(f'\nCommand run Error: {cmd_arr}\nError:\n{err}\n')
            sys.exit(1)
    else:
        output = sub.run(cmd_arr, stdout=sub.PIPE, stderr=sub.STDOUT, shell=shell_).stdout.decode('latin1')
        if print_output is True:
            print(f'\n{output}\n')
        print('done')
        return output


def write_pythonpath_vscode(pypath, vscode_config_path='.vscode/settings.json'):

    with open(vscode_config_path, 'r') as f:
        vscode_config = json.load(f)

    vscode_config.setdefault('python', dict()).update({'pythonPath': pypath})

    with open(vscode_config_path, 'w') as f:
        json.dump(vscode_config, f, indent=4, sort_keys=True)


print()
poetry_install = run('Installing poetry virtual env', ['poetry', 'install'])

poetry_output = poetry_install.split(os.linesep)[0].split()
venv_path = poetry_output[-1]
venv_hash = poetry_output[-3]
venv_full_path = os.path.join(venv_path, venv_hash)

print(f'Poetry virtual env installed at: {venv_full_path}')

python_subdir = "Scripts" if platform_ == "Windows" else "bin"
venv_python = os.path.join(venv_full_path, python_subdir, 'python')

git_init = run('Initializing GIT repo', ['git', 'init', '.'])
pre_commit_install = run('Installing pre-commit', [venv_python, '-m', 'pre_commit', 'install'])
pre_commit_autoupdate = run('Auto Updating pre-commit', [venv_python, '-m', 'pre_commit', 'autoupdate'])
git_init = run('Adding project files to GIT repo', ['git', 'add', '.'])
git_commit = run('Committing to GIT repo', ['git', 'commit', '-m', 'Initialize environment'], stderr2out=True)

print('Updating vscode config with virtual env path ...', end='', flush=True)
write_pythonpath_vscode(venv_python)
print('done')
print()

sys.exit(0)
