# -*- coding: utf-8 -*-
'''
本脚本用于运行模块的测试用例。适用于windows环境。

版本信息：
1.python2.7
2. odoo10
3.win7

使用方法:
1. 在交互界面提供的DB列表中输入需要测试的DB
2. 在交互界面提供的模块列表中输入需要测试的模块名
3.如果选中的模块已经安装了，会先执行更新， 然后测试；否则直接执行测试
'''
import os
import ConfigParser
import psycopg2
import subprocess

work_directory = os.getcwd()
odoo_conf_path = os.path.join(work_directory, 'odoo-server.conf')

# 获取测试DB
cf = ConfigParser.ConfigParser()
cf.read(odoo_conf_path)
db_user = cf.get('options', 'db_user')
db_pwd = cf.get('options', 'db_password')
db_port = cf.get('options', 'db_port')
db_host = cf.get('options', 'db_host')
try:
    conn = psycopg2.connect(dbname='postgres', user=db_user, host='localhost', password=db_pwd, port=db_port)
except:
    print 'I am unable to connect to the database'
cur = conn.cursor()
cur.execute('select datname from pg_database where datistemplate = false')
db_list_all = cur.fetchall()
conn.close()
db_list_input = map((lambda x: x[0]), db_list_all)
print(db_list_input)
db_select = raw_input('please select the test db:')
while not db_select:
    db_select = raw_input('please select the test db:')
while db_select not in db_list_input:
    db_select = raw_input('please select the right test db:')

# 获取测试模块
try:
    conn = psycopg2.connect(dbname=db_select, user=db_user, host='localhost', password=db_pwd, port=db_port)
except:
    print 'I am unable to connect to the database'
cur = conn.cursor()
cur.execute('select name from ir_module_module order by id desc')
module_list_all = cur.fetchall()
conn.close()
module_list_input = map((lambda x: x[0]), module_list_all)
print module_list_input
module_selected = raw_input('please select the test module:')
while not module_selected:
    module_selected = raw_input('please select the test module:')
while module_selected not in module_list_input:
    module_selected = raw_input('please select the right test module:')

# 执行测试命令
try:
    command_module_init = ' -i ' + module_selected
    command_module_upd = ' -u ' + module_selected
    command_db = ' -d ' + db_select
    conn = psycopg2.connect(dbname=db_select, user=db_user, host='localhost', password=db_pwd, port=db_port)
    cur = conn.cursor()
    cur.execute('select state from ir_module_module where name=%s',
                (module_selected,))  # 查看模块存储在数据库中的状态字段是installed 还是uninstalled
    module_state = cur.fetchall()
    conn.close()
    if module_state[0][0] == 'installed':
        print('\nUpdating the installed module')
        command_upd = 'python.exe odoo-bin -c odoo-server.conf --stop-after-init' + command_module_upd + command_db
        subprocess.call(command_upd, shell=True)
    command_init = 'python.exe odoo-bin -c odoo-server.conf --log-level=error --test-enable --stop-after-init' + command_module_init + command_db
    print('\nThe Test Result:\n')
    subprocess.call(command_init, shell=True)
except:
    print('With some error when run the test script ')
