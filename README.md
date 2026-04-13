# 🔧 Java Class Extractor & Decompiler Tool

This is a tool that automatically extracts system file and decompiles java class configuration files for Java projects.  
It operates on web applications with file download vulnerabilities.

---

## 📋 Requirement
1. File download vulnerability targetURL (LFI or Path Traversal) of the target web application.  
2. Secure the path to at least one .class file.  
3. Web root (WEB-INF/classes) absolute path information.  

---

## 📁 Struct
- extract.py &nbsp;&nbsp;&nbsp;&nbsp;# Script
- cfr-0.154.jar &nbsp;&nbsp;&nbsp;&nbsp;# class Decompiler
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

**Creating a directory using the package name**  
**Downloading chaining classes via import path**
