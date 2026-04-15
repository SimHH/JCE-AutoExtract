
home_directory_files = [
    ".bashrc",
    ".bash_profile",
    ".bash_logout",
    ".profile",
    ".bash_history",
    ".zshrc",
    ".zsh_history",
    ".vimrc",
    ".viminfo",
    ".tmux.conf",
    ".gitconfig",
    ".gitignore_global",
    ".mysql_history",
    ".dist.history"
    ".ssh/",
    ".ssh/id_rsa",
    ".ssh/id_rsa.pub",
    ".ssh/id_ecdsa",
    ".ssh/id_ecdsa.pub",
    ".ssh/id_ed25519",
    ".ssh/id_ed25519.pub",
    ".ssh/authorized_keys",
    ".ssh/known_hosts",
    ".ssh/config",    
    ".zhistory",
    ".history",
    ".sh_history",
    ".nano_history",
    ".sqlite_history",

]

system_file = [

    [
        "/etc/nginx/nginx.conf",
        "/etc/nginx/conf.d/default.conf",
        "/etc/nginx/mime.types",
        "/etc/nginx/fastcgi_params",
        "/etc/nginx/fastcgi_params.default",
        "/etc/nginx/fastcgi.conf",
        "/etc/nginx/fastcgi.conf.default",
        "/etc/nginx/forceRestart.sh",
        "/etc/nginx/win-utf",
        "/etc/nginx/scgi_params",
        "/etc/nginx/fastcgi_params",
        "/etc/nginx/nginx.host"
        "/etc/nginx/scgi_params.default",
        "/etc/nginx/uwsgi_params.default",
        "/etc/nginx/uwsgi_params",
        "/etc/nginx/mime.types.default",
        "/etc/nginx/html/index.html",
        "/etc/nginx/html/50x.html",
        "/usr/share/nginx/html/index.html",
        "/usr/share/nginx/html/50x.html",
        "/var/www/html/index.html",
        "/var/www/html/index.nginx-debian.html",
    ],

    [
        "/etc/hosts",
        "/etc/hostname",
        "/etc/crontab",
        "/etc/resolv.conf",
        "/etc/host.conf",
        "/etc/ssh/sshd_config",
        "/etc/ssh/ssh_config",
        "/etc/apache2/apache2.conf",
        "/etc/mysql/my.cnf",
        "/etc/passwd",
        "/etc/passwd-",
        "/etc/shadow-",
        "/etc/shadow",
        "/etc/sysctl.conf",
        "/etc/bash.bashrc",
        "/etc/fstab",
        "/etc/rsyslog.conf",
        "/etc/services",
        "/etc/modules",
        "/etc/environment",
        "/etc/protocols",
        "/etc/hosts.allow",
        "/etc/hosts.deny",
        "/etc/httpd/conf/httpd.conf",
        "/etc/httpd/conf/magic",
        "/etc/httpd/conf/conf.d",
        "/etc/httpd/conf/autoindex.conf",
        "/etc/httpd/conf/README",
        "/etc/httpd/conf/userdir.conf",
        "/etc/ntp.conf",
        "/etc/ntp/crypto",
        "/etc/ntp/keys",
        "/etc/ntp/step-tickers",
        "/etc/os-release",
        "/etc/centos-release",
        "/etc/redhat-release",
        "/etc/pam.d/other",
        "/etc/pam.d/system-auth",
        "/etc/pam.d/password-auth",
        "/etc/pam.d/common-auth",
        "/etc/pam.d/common-account",
        "/etc/pam.d/common-password",
        "/etc/pam.d/common-session",
        "/etc/pam.d/chfn",
        "/etc/pam.d/chsh",
        "/etc/pam.d/config-util",
        "/etc/pam.d/crond",
        "/etc/pam.d/fingerprint-auth",
        "/etc/pam.d/fingerprint-auth-ac",
        "/etc/pam.d/login",
        "/etc/pam.d/passwd",
        "/etc/pam.d/password-auth-ac",
        "/etc/pam.d/postlogin",
        "/etc/pam.d/su",
        "/etc/pam.d/sudo",
        "/etc/pam.d/sudo-i",
        "/etc/pam.d/su-l",
        "/etc/pam.d/smtp",
        "/etc/pam.d/sshd",
        "/etc/pam.d/systemd-user",
        "/etc/pam.d/ppp",
        "/etc/pam.d/common-auth",
        "/etc/pam.d/common-password",


    ],

    [
        "/proc/self/maps",
        "/proc/self/cmdline",
        "/proc/self/exe",
        "/proc/self/cwd/maps",
        "/proc/self/environ",
        "/proc/self/net/tcp",
        "/proc/self/net/udp",
        "/proc/self/net/arp",
        "/proc/self/comm",
        "/proc/self/syscall",
        "/proc/self/loginuid",

    ],

    [
        "/var/log/nginx/error.log",
        "/var/log/nginx/access.log",
        "/var/log/cron",
        "/var/log/dmesg",
        "/var/log/secure",
        "/var/log/yum.log",
        "/var/log/lastlog",
        "/var/log/wtmp",
        "/var/log/utmp",
        "/var/log/btmp",
        "/var/log/tallylog",

    ],

    [
        "/usr/lib/x86_64-linux-gnu/libc.so.6",
        "/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2",
    ]
]

targets = ( "cat ", "vi ", "vim ", "nano ", "touch ", )

webTarget = ["WEB-INF", "web-inf", "webroot", "WebRoot", "webroots", "WebRoots", "WEB-INF/web.xml", "WEB-INF/classes", "application.properties", "application.yml", "application.yaml", "system.xml", "jdbc.xml", "web.xml", "Web.config", "Web.Config", "php.ini", "bootstrap.properties", "bootstrap.yml", "database.properties", "jdbc.properties", "config.properties", "configuration.properties", "root-context.xml", "server.xml", "context.xml", "tomcat-users.xml", "context-database.xml", "context-property.xml", "servlet-context.xml", "context-security.xml", "context-exception.xml", "JeusServer.log", "jeus8", "security.properties", "domain.xml", "bxm-application.xml", "com/"]

file_extensions = ["xml", "properties", "property", "conf", "config", "class", "log", "logback", "yaml", "yml", "sh", ]

# file_extensions = (
#         'log', 'xml', 'class', 'properties', 'yml', 'yaml', 
#         'conf', 'config', 'jsp', 'php', 'html', 'htm', 
#         'js', 'css', 'txt', 'json', 'sql', 'db', 'bak', 
#         'war', 'jar', 'sh', 'py', 'rb', 'java', 'cpp', 'c', 'h',
#         'md', 'pdf', 'doc', 'docx', 'xls', 'xlsx'
#     )

