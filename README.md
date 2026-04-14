# 🔧 JCE-AutoExtract Tool

추출된 Passwd 파일 및 .class 파일을 기반으로 시스템 파일 및 Java 프로젝트의 구성 및 클래스 파일을 추출하고 디컴파일합니다.  
파일 다운로드 취약점이 있는 웹 애플리케이션에서 작동합니다.

#

Extracts and decompiles system files and Java project configuration and class files based on extracted Passwd files and .class files.  
Operates on web applications with file download vulnerabilities.

---

## 📋 Requirement

- 대상 웹 애플리케이션의 파일 다운로드 취약점 URL(targetURL, LFI 또는 경로 탐색)

- 추출된 passwd 파일 또는 .class 파일  

#

- URL of the target web application's file download vulnerability (targetURL, LFI, or path traversal)

- passwd file or .class file

---

## 📁 Struct
- extract.py &nbsp;&nbsp;&nbsp;&nbsp;# Script
- cfr-0.154.jar &nbsp;&nbsp;&nbsp;&nbsp;# class Decompiler
- dictionary.py &nbsp;&nbsp;&nbsp;&nbsp;# path dictionary
- passwd &nbsp;&nbsp;&nbsp;&nbsp;# Example 

---

## 📖 Execute
```bash
# Bash
python extract.py --passwd passwd
python extract.py --class_file test.class
```

---

## ⚙️ Principle
If test.class is...
```java
// Java

package com.test.seed.front.main.service;

import com.test.seed.front.common.service.CommonService;
import com.test.seed.front.member.controller.MemberController;
import com.test.seed.front.member.dao.MemberDAO;

.................

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

**패키지 이름을 사용하여 디렉토리 생성**  
**import 경로를 통한 클래스 체이닝 다운로드**

**Creating a directory using the package name**  
**Downloading chaining classes via import path**

---