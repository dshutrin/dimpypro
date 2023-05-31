from os import system as s
from os import path
from os import mkdir, chdir
import sys
import venv
from subprocess import run
from pprint import pprint


def apps_install():
	commands = [
		'add-apt-repository ppa:deadsnakes/ppa',
		'apt update',
		'apt upgrade',
		'apt install python3.11',
		'apt install gunicorn',
		'apt install nginx',
		'apt install mysql-server',
		'apt install mysql-client',
		'apt install python3-dev',
		'apt install libmysqlclient-dev',
		'apt install python3-venv',
		'apt install python3-pip',
		'apt install python-is-python3'
	]
	for command in commands:
		s(f'NEEDRESTART_MODE=a {command} -y')
	s('service nginx status')


def nginx_conf(project_name):
	domen = input('Введите домен, на котором будет работать сайт: ')
	file_data = 'server {\nlisten 80;\nserver_name ' + domen
	file_data = file_data + ';\nlocation = /favicon.ico { access_log off; log_not_found off; }\nlocation /static/ {\nroot '
	file_data = file_data + f'/{project_name}/{project_name}'
	file_data += ';\nindex index.html;\n}\nlocation / {\ninclude proxy_params;\nproxy_pass http://unix:/run/gunicorn.sock;\n}\n}\n'
	with open(f'/etc/nginx/sites-available/{project_name}', 'w', encoding='utf-8') as file:
		file.write(file_data)
	commands = [f'ln -s /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled', 'systemctl restart nginx', 'service nginx restart']
	for command in commands:
		s(command)


def gunicorn_conf(project_name):
	#  Настройка файлов для работы gunicorn
	with open('/etc/systemd/system/gunicorn.socket', 'w', encoding='utf-8') as file:
		file.write('[Unit]\nDescription=gunicorn socket\n[Socket]\nListenStream=/run/gunicorn.sock\n[Install]\nWantedBy=sockets.target')
	with open('/etc/systemd/system/gunicorn.service', 'w', encoding='utf-8') as file:
		file.write(f'[Unit]\nDescription=gunicorn daemon\nRequires=gunicorn.socket\nAfter=network.target\n[Service]\nUser=root\nGroup=www-data\nWorkingDirectory=/{project_name}/{project_name}\nExecStart=/{project_name}/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock {project_name}.wsgi:application\n[Install]\nWantedBy=multi-user.target')

	commands = ['systemctl daemon-reload', 'systemctl restart gunicorn.socket', 'systemctl restart gunicorn.service', 'systemctl start gunicorn.socket', 'systemctl enable gunicorn.socket']
	for command in commands:
		s(command)

	nginx_conf(project_name)


def venv_conf(project_name):
	sys.executable = f'/{project_name}/venv/bin/python'
	all_pkgs = ''
	with open(f'/{project_name}/{project_name}/requirements.txt', 'r', encoding='utf-8') as file:
		all_pkgs = file.read()
	for pkg in all_pkgs.split('\n'):
		run([sys.executable, "-m", "pip", "install", pkg])
	need_pkgs = ('gunicorn', 'django', 'mysqlclient')
	for pkg in need_pkgs:
		if not (pkg in all_pkgs):
			run([sys.executable, "-m", "pip", "install", pkg])

	run([sys.executable, f"/{project_name}/{project_name}/manage.py", "makemigrations"])
	run([sys.executable, f"/{project_name}/{project_name}/manage.py", "migrate"])

	username = input('Введите имя пользователя для суперпользователя: ')
	email = input('Введите email суперпользователя: ')
	password = input('Введите пароль для суперпользователя: ')

	s(f'export DJANGO_SUPERUSER_PASSWORD={password}')
	s(f'/{project_name}/venv/bin/python /{project_name}/{project_name}/manage.py createsuperuser --username {username} --email {email} --noinput')
	run([sys.executable, f"/{project_name}/{project_name}/manage.py", "collectstatic", "--noinput"])

	gunicorn_conf(project_name)


def mysql_init(project_name):
	sys.path.append(f'/{project_name}/{project_name}/{project_name}')
	from settings import DATABASES

	db_name = DATABASES['default']['NAME']
	db_user = DATABASES['default']['USER']
	db_user_password = DATABASES['default']['PASSWORD']
	db_user_host = DATABASES['default']['HOST']

	sql_command = f'''create database {db_name};
create user {db_user}@{db_user_host} identified by "{db_user_password}";
grant all privileges on {db_name}.* to {db_user}@{db_user_host} with grant option;
flush privileges;
'''
	with open('mysql_conf.sql', 'w', encoding='utf-8') as file:
		file.write(sql_command)

	s('mysql < mysql_conf.sql')
	s('rm mysql_conf.sql')

	venv_conf(project_name)


def download_repo():
	repo_link = input('Введите ссылку на публичный репозиторий проекта: ')
	project_name = repo_link.split('/')[-1].replace('.git', '')

	mkdir(f'/{project_name}')
	chdir(f'/{project_name}')

	s(f'git clone {repo_link}')
	venv.create(f'/{project_name}/venv', with_pip=True)
	#s('python -m venv venv')
	s(f'chown www-data -R /{project_name}')
	s(f'chmod 755 -R /{project_name}')

	is_ok = True
	if not path.exists(f'/{project_name}/{project_name}/{project_name}/settings.py'):
		print('Файл settings.py находится не там, где должен!')
		is_ok = False
	if not path.exists(f'/{project_name}/venv'):
		print('Папка venv находится не там, где должена!')
		is_ok = False
	if not path.exists(f'/{project_name}/{project_name}/requirements.txt'):
		print('Файл requirements.txt не найден!')
		is_ok = False

	if not is_ok:
		print('Ошибка конфигурации проекта')
		return 'error'

	mysql_init(project_name)


if __name__ == '__main__':
	apps_install()
	download_repo()
