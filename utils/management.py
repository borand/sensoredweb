import sh
#import path
import logging
import requests
import re
import subprocess
import time

# #from djSensor.settings import PROJECT_ROOT
# from django.utils.log import getLogger
# logger = getLogger("app")


# projectname = 'univsens'
# runfcgi_pid = 'runfcgi_nginx.pid'

# username    = sh.whoami().stdout[:-1]
 
# VENV          = PROJECT_ROOT + '/../../../venv/bin/'
# VENV_PYTHON   = VENV + 'python'
# PROJECT_PATH  = PROJECT_ROOT + '/../'
# NGINX_CONFIG  = '%s.conf' % projectname

# python_bin  = sh.Command(VENV+'python')
# manage_py   = PROJECT_PATH +'manage.py'
# runfcgi_cmd = r'%s %s runfcgi host=127.0.0.1 port=8080' % (python_bin, manage_py) 


# def ps():
#     p = subprocess.Popen(["ps", "-e","-f"], stdout=subprocess.PIPE, env={'LANG':'C'})
#     return p.communicate()[0]

# def get_pid(lookfor='python', username=r'\w+'):
#     """ return process id of process specfied by lookfor variable 
#         equivalant to shell command ps -ef | grep lookfor
#     """
#     ps_str = r'(?:\w+\s+)(\d+)(?:\s+\d+\s+\d+\s+\w+\d+)(?:.*?)(?:\d{2}\:\d{2}\:\d{2}\s+)'
#     lookfor_expr = re.compile(ps_str + '(.*?' + lookfor + ')', re.DOTALL)
#     return lookfor_expr.findall(ps())

# def get_ps(lookfor='python'):
#     """ return process id of process specfied by lookfor variable 
#         equivalant to shell command ps -ef | grep lookfor
#     """
#     #ps_str = '(?:\w+\s+)(\d+)'
#     logger.info('get_ps(lookfor=%s)' % lookfor)
#     ps_str = '(?:\w+\s+)(\d+)(?:\s+\d+\s+\d+\s+\w+\d+)(?:.*?)(?:\d{2}\:\d{2}\:\d{2}\s+)'
#     lookfor_expr = re.compile(ps_str + '(?:.*?' + lookfor + ')')
#     return lookfor_expr.findall(ps())
#     #return lookfor_expr.findall(sh.ps('-f','-e').stdout)

# def add_sites_available():
#     sites_available_link = '/etc/nginx/sites-available/%s' % NGINX_CONFIG
#     sites_enabled_link = '/etc/nginx/sites-enabled/%s' % NGINX_CONFIG
#     with sh.sudo:
#         if not path.path(sites_available_link).exists():
#             sh.ln('-s', PROJECT_PATH+NGINX_CONFIG,sites_available_link)
#         if not path.path(sites_enabled_link).exists():
#             sh.ln('-s', PROJECT_PATH+NGINX_CONFIG,sites_enabled_link)

# def restart_fcgi():
#     logger.info('restarting runfcgi')
    
#     pid_list = is_fcgi_running()
#     if len(pid_list) > 0:
#         logger.info('killing process %s' % pid_list[0]) 
#         out = sh.kill(pid_list[0])
#         logger.info('kill exit code %d' % out.exit_code)
    
#     logger.info('starting runfcgi')
#     out = python_bin(manage_py,'runfcgi','host=127.0.0.1','port=8080')
#     logger.info('runfcgi exit code %d',out.exit_code)    
#     pid_list = is_fcgi_running()
#     if pid_list:
#         logger.info('runfcgi restarted')
#     else:
#         logger.info('cannot find runfcgi pid after restart attempt')
    
# def start_fcgi():    
#     logger.info('start_fcgi()')
    
#     if is_fcgi_running():
#         output = get_ps('runfcgi')
#     else:
#         output = python_bin(manage_py, 'runfcgi','host=127.0.0.1','port=8080',_bg=True)
#     return output

# def is_fcgi_running():
#     return get_ps("manage.py runfcgi")

# def is_project_linked_to_ngingx():
#     sites_enabled   = sh.ls('/etc/nginx/sites-enabled/'+NGINX_CONFIG,'-la').stdout
#     sites_available = sh.ls('/etc/nginx/sites-available/'+NGINX_CONFIG,'-la').stdout
    
#     if PROJECT_PATH+NGINX_CONFIG in sites_available and PROJECT_PATH+NGINX_CONFIG in sites_enabled:
#         return True
#     else:
#         return False

# def ping_site(app_name='/'):
#     try:
#         out = requests.get('http://%s/ping' % get_host_ip())
#         response = out.content
#     except:
#         response = 'none'
#     if 'pong' in response:
#         return True
#     else:
#         return False
        
# def is_nginx_running():
#     return len(get_ps('nginx: master process')) > 0 

# def stop_nginx():
#     if is_nginx_running():
#         with sh.sudo:
#             nginx = sh.Command('/etc/init.d/nginx')
#             nginx('stop')

# def start_nginx():
#     with sh.sudo:
#         nginx = sh.Command('/etc/init.d/nginx')
#         nginx('start')

# def get_host_ip():
#     ip_exp = re.compile('(?:inet addr:192.168.)(\d+\.\d+)')
#     ip_out = ip_exp.findall(sh.ifconfig().stdout)
#     if len(ip_out) == 1:
#         return '192.168.' + ip_out[0]
#     else:
#         return '127.0.0.1'

# def check_nginx_configuration_file():
#     full_config_filename = PROJECT_PATH+NGINX_CONFIG
#     if path.path(full_config_filename).exists():
#         config_file = open(full_config_filename,'r').read()
#         server_ip = re.compile('(?:server_name )(\d+\.\d+\.\d+\.\d+)').findall(config_file)[0]
#         if server_ip in get_host_ip():
#             return True
#     return False
    
    
# def update_nginx_configfile():
#     full_config_filename = PROJECT_PATH+NGINX_CONFIG
#     if path.path(full_config_filename).exists():
#         config_file = open(full_config_filename,'r').read()
#         server_ip = re.compile('(?:server_name )(\d+\.\d+\.\d+\.\d+)').findall(config_file)[0]
#         config_file = config_file.replace(server_ip, get_host_ip())
#         config_file_handle = open(full_config_filename,'w')
#         config_file_handle.write(config_file)
#         config_file_handle.close()    
#         logging.info('Saving file')
#     else:
#         logging.info('Did not find nginx config file: ' + full_config_filename)

# def stop_fcgi():
    
#     pid = is_fcgi_running()
#     if pid:
#         logging.info('Killing process %s' % pid[0])
#         sh.kill(pid[0])
#     else:
#         logging.info('Process runfcgi already stopped.')

# def start_all():
#     print start_fcgi()
        
# def restart():    
#     stop_fcgi()
#     time.sleep(1)    
#     start_fcgi()    
#     with sh.sudo:
#         run = sh.Command('/etc/init.d/nginx')
#         run('restart')
#     get_status()

# def get_status():
#     ret_status = {'Logged is as':            username,\
#                   'host ip':                 get_host_ip(),\
#                   'Project name':            projectname, \
#                   'Project path':            PROJECT_PATH,\
#                   'Project path found':      path.path(PROJECT_PATH).exists(), \
#                   'Nginx config file found': path.path(PROJECT_PATH+NGINX_CONFIG).exists(), \
#                   'Found nginx log dir':     path.path('/home/%s/log/nginx' % username).exists(),\
#                   'Config file ip match':    check_nginx_configuration_file(),\
#                   'Nginx server is runing':  is_nginx_running(),\
#                   'Project runcgi process':  is_fcgi_running(),\
#                   'Ping main app succesful': ping_site(),\
#                   }
#     return ret_status   
    
# if __name__ == "__main__":
#     logging.basicConfig(format='%(levelname)10s: %(message)10s', level=logging.ERROR)
#     stop_fcgi()
#     start_fcgi()