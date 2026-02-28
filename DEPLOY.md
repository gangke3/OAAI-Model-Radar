# OAAI Model-Radar 远程部署文档

> 版本：v1.0  
> 日期：2026-02-27  
> 状态：✅ 已成功部署上线

---

## 一、项目概述

**OAAI Model-Radar** 是一个通用 LLM API 节点管理与测速工具，支持多配置、并发测试、中英文界面切换。

- **线上访问地址**：https://oaai.xyz/model-radar/
- **本地项目路径**：`D:\OPENCLAW\APP\Manager\`
- **服务器项目路径**：`C:\model-radar\`  
- **技术架构**：单 HTML 文件前端（React + Babel CDN）+ Python 纯标准库后端

---

## 二、服务器环境

| 项目 | 值 |
|------|----|
| 服务器 IP | 124.223.59.60 |
| 操作系统 | Windows Server（腾讯云） |
| SSH 用户名 | administrator |
| SSH 密码 | Hongyu244222 |
| SSH 端口 | 22（Windows OpenSSH） |
| Nginx 路径 | `C:\nginx\` |
| Nginx 配置文件 | `C:\nginx\conf\nginx.conf` |
| Nginx 服务名 | `nginx`（Windows 服务，AUTO_START） |
| Nginx 启动方式 | `C:\nginx\nginx.exe -p C:\nginx` |
| 主站前端 | Compliance 静态站，`C:\nginx\html\compliance_site\` |
| 主站后端 | OA Fund Manager Node.js，端口 3001 |

---

## 三、最终部署架构

```
               Internet
                  │
         ┌────────▼────────┐
         │   Nginx :443    │  HTTPS 终止 + SSL
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
/model-radar/     /api/      /fond/       /
静态文件          OA基金        OA基金     合规主站
C:\model-radar\   Node.js     Node.js    compliance_site
                  :3001       :3001
    │
    ├── /model-radar/api/ ──► Python :5001
    └── /model-radar/*   ──► C:\model-radar\index.html
```

### Nginx location 配置（关键）

```nginx
# OAAI Model-Radar - Backend API
location /model-radar/api/ {
    proxy_pass http://127.0.0.1:5001/api/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 60s;
}

# OAAI Model-Radar - Static Frontend
location /model-radar/ {
    alias C:/model-radar/;
    index index.html;
}
```

> ⚠️ **必须使用 `alias`，不可使用 `root`**（见经验教训第 5 条）

---

## 四、部署步骤（完整流程）

### 前置准备（本地）

```bash
# 安装 paramiko（SSH/SFTP 自动化库）
pip install paramiko
```

### Step 1：创建服务器目录

```python
# 服务器 D: 盘不可访问（空盘），必须用 C: 盘
run(client, r'powershell -Command "New-Item -ItemType Directory -Force -Path C:\model-radar\configs | Out-Null"')
```

### Step 2：上传项目文件

由于 Windows OpenSSH 的 SFTP 默认根目录为 `/C:/`，D 盘不可通过 SFTP 访问。  
C 盘可以通过 SFTP 路径 `/C:/model-radar/filename` 上传：

```python
sftp.put(local_path, "/C:/model-radar/index.html")
sftp.put(local_path, "/C:/model-radar/server.py")
```

### Step 3：创建默认配置文件

```python
# 通过 SFTP 直接写 JSON 文件
default_json = '{"models":{"providers":{}},"agents":{"defaults":{"model":{"primary":""}}}}'
with sftp.open('/C:/model-radar/configs/默认配置.json', 'w') as f:
    f.write(default_json)
```

### Step 4：启动 Python 后端

以进程方式后台运行（直接 Start-Process，不注册服务）：

```powershell
# Python 路径：C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe
Start-Process -FilePath "python.exe" -ArgumentList "C:\model-radar\server.py 5001" -WorkingDirectory C:\model-radar -WindowStyle Hidden
```

验证后端：
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5001/api/config/list -UseBasicParsing | Select -Expand Content
# 预期输出: ["默认配置"]
```

### Step 5：更新 Nginx 配置

**写配置文件时必须用 base64 + WriteAllBytes（无 BOM，无编码问题）：**

```python
import base64

NGINX_CONF = r"""worker_processes 1; ... """  # 完整配置内容

b64 = base64.b64encode(NGINX_CONF.encode('utf-8')).decode('ascii')
ps_cmd = f"$b = [System.Convert]::FromBase64String('{b64}'); [System.IO.File]::WriteAllBytes('C:\\nginx\\conf\\nginx.conf', $b)"
run(client, f'powershell -Command "{ps_cmd}"')
```

测试配置：
```bash
# 必须带 -p 参数指定工作目录！
cmd /c "cd /d C:\nginx && nginx.exe -p C:\nginx -t"
```

### Step 6：重启 Nginx 服务（关键）

**⚠️ 必须用 Windows 服务级别的停止/启动，不能只用 `nginx -s reload`！**

```python
# 用 fire-and-forget 方式，避免 SSH 连接因服务重启而断开
def fire_forget(c, cmd):
    transport = c.get_transport()
    ch = transport.open_session()
    ch.exec_command(cmd)

fire_forget(c, "powershell -Command \"Stop-Service nginx -Force; Start-Sleep 1; Start-Service nginx\"")

# 断开当前连接，等待 nginx 重启
c.close()
time.sleep(8)

# 重新连接验证
c2 = make_client()
```

### Step 7：验证

```python
# 本地 HTTP 验证（通过 HTTP 80，由 location /model-radar/ alias 处理）
out = "(Invoke-WebRequest 'http://127.0.0.1/model-radar/' -UseBasicParsing).Content.Substring(0,200)"
# 预期输出包含: OAAI Model-Radar

# 公网 HTTPS 验证
# 直接访问 https://oaai.xyz/model-radar/
```

---

## 五、经验教训与踩坑记录

### ❌ 坑 1：SSH 密码认证在 PowerShell 中无法非交互式传入
**现象**：`ssh administrator@124.223.59.60` 会卡住等待密码输入。  
**解决**：使用 `paramiko` Python 库实现自动化 SSH，在代码中直接传入密码。

```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=22, username=USER, password=PASSWD)
```

---

### ❌ 坑 2：Windows OpenSSH 的 SFTP 无法访问 D: 盘
**现象**：SFTP `sftp.put(local, "D:/model-radar/file")` 报 `OSError: Failure`。  
**原因**：Windows OpenSSH SFTP 服务的根目录默认为 `C:` 盘，D 盘路径会报 `Bad message`。  
**解决**：
- ✅ 将项目部署到 `C:\model-radar\` 而非 `D:\model-radar\`
- ✅ SFTP 路径使用 `/C:/model-radar/filename` 格式（注意前缀 `/C:`）

---

### ❌ 坑 3：PowerShell 写文件会添加 BOM（字节顺序标记）
**现象**：`nginx -t` 报错 `unknown directive "﻿worker_processes"`（BOM 字符被识别为指令名前缀）。  
**原因**：PowerShell 的 `Set-Content ... -Encoding UTF8` 会默认写入 UTF-8 BOM（`EF BB BF`），nginx 无法解析。  
**解决**：用 `[System.IO.File]::WriteAllBytes()` 写入原始字节（base64 解码后），完全避免 BOM：

```powershell
$b = [System.Convert]::FromBase64String('BASE64_CONTENT')
[System.IO.File]::WriteAllBytes('C:\nginx\conf\nginx.conf', $b)
```

---

### ❌ 坑 4：直接向 PowerShell 传递长字符串会导致 Channel closed 异常
**现象**：写 80KB HTML 文件时，`client.exec_command(...)` 报 `SSHException: Channel closed`。  
**原因**：Windows OpenSSH 对单条 exec_command 的命令长度有限制（约 8KB）。  
**解决**：
- 将文件通过 SFTP `sftp.put()` 直接上传（针对 C 盘路径有效）
- 或通过 SFTP 先将 base64 解码 PowerShell 脚本写入临时 `.ps1` 文件，再 `exec_command` 执行该脚本

---

### ❌ 坑 5：Nginx location 使用 `root` 配合子路径时会导致路径错乱
**现象**：配置 `root C:/; try_files $uri $uri/ /model-radar/index.html;` 后，浏览器访问 `/model-radar/` 仍返回主站内容。  
**原因**：`try_files` 的最后一个 fallback 参数 `/model-radar/index.html` 是 URI 形式的内部重定向，Nginx 会将其重新匹配 location，经过 `location /` 的 SPA fallback 逻辑，最终返回 compliance 站的 `index.html`。  
**解决**：使用 `alias` 代替 `root`：

```nginx
# ✅ 正确
location /model-radar/ {
    alias C:/model-radar/;
    index index.html;
}

# ❌ 错误（会导致 try_files fallback 被 location / 拦截）
location /model-radar/ {
    root C:/;
    try_files $uri $uri/ /model-radar/index.html;
}
```

---

### ❌ 坑 6：`nginx -s reload` 失败（PID 文件不匹配）
**现象**：`nginx -s reload` 报 `OpenEvent("Global\ngx_reload_XXXX") failed (2: The system cannot find the file specified)`。  
**原因**：`C:\nginx\logs\nginx.pid` 中记录的 PID 与当前实际运行的 nginx master 进程 PID 不一致（因为之前多次强制 kill/restart，PID 文件变成旧值）。Nginx 的信号机制依赖 Windows 内核事件对象 `Global\ngx_reload_<PID>`，PID 不对就找不到事件。  
**解决**：**不要用 `nginx -s reload`！** 改用 Windows 服务级别重启：

```python
# 正确做法：通过服务管理重启
fire_forget(c, "powershell -Command \"Stop-Service nginx -Force; Start-Sleep 1; Start-Service nginx\"")
# 然后断开 SSH 连接并等待 8 秒后重连
```

---

### ❌ 坑 7：`net stop nginx` / `net start nginx` 会导致 SSH 连接超时
**现象**：执行 `net stop nginx` 后 paramiko 报 `PipeTimeout`，`net start nginx` 同样挂起。  
**原因**：`net stop/start` 命令阻塞等待服务完全停止/启动，在高流量服务器上可能需要数十秒，超过 paramiko 默认 timeout。  
**解决**：使用 **fire-and-forget** 模式——打开新 SSH channel 发送命令但不等待结果，然后立即断开连接，等待后重新连接：

```python
def fire_forget(c, cmd):
    transport = c.get_transport()
    ch = transport.open_session()
    ch.exec_command(cmd)  # 不调用 ch.recv()，不等待输出

fire_forget(c, "powershell -Command \"Stop-Service nginx -Force; Start-Sleep 2; Start-Service nginx\"")
c.close()
time.sleep(8)
c2 = make_client()  # 重新连接验证
```

---

### ❌ 坑 8：服务器 D: 盘实际为空盘（null size）
**现象**：`New-Item -Path D:\model-radar` 报 "路径不合法"，`Get-ChildItem D:\` 报错，`Test-Path D:\FOND` 返回 False。  
**原因**：服务器的 D: 盘显示为空盘（Size/FreeSpace 均为 null），可能是未格式化或虚拟空盘。  
**解决**：所有文件部署到 C: 盘。

---

### ❌ 坑 9：多个 nginx 进程同时监听同一端口（旧进程未退出）
**现象**：`netstat` 显示多个 PID 监听 443 端口，其中一些是旧进程（使用旧配置）。  
**原因**：nginx 的 master/worker 进程模型在 reload 时会保留旧 worker 处理存量请求，同时新 worker 用新配置处理新请求。但如果 reload 失败（PID 问题），旧 master 和新启动的额外进程会同时存在。  
**解决**：通过 Windows 服务 `Stop-Service nginx` 停止所有 nginx 进程，再 `Start-Service nginx` 用新配置重新启动。

---

## 六、维护操作手册

### 更新前端文件

```python
# 重新上传 index.html（SFTP）
sftp = client.open_sftp()
sftp.put(r"D:\OPENCLAW\APP\Manager\index.html", "/C:/model-radar/index.html")
sftp.close()
# 无需重启 nginx（静态文件直接生效）
```

### 重启 Python 后端

```python
# 关闭旧进程
run(client, "powershell -Command \"Get-Process python | Where-Object {$_.CommandLine -like '*model-radar*'} | Stop-Process -Force\"")
# 启动新进程
py = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe"
fire_forget(client, f"powershell -Command \"Start-Process -FilePath '{py}' -ArgumentList 'C:\\model-radar\\server.py 5001' -WorkingDirectory C:\\model-radar -WindowStyle Hidden\"")
```

### 重启 Nginx（配置变更后）

```python
def restart_nginx(client):
    fire_forget(client, "powershell -Command \"Stop-Service nginx -Force; Start-Sleep 2; Start-Service nginx\"")
    client.close()
    time.sleep(8)
    c2 = make_client()
    out, _ = run(c2, "sc query nginx | findstr STATE")
    print(f"Nginx state: {out.strip()}")
    return c2
```

### 检查服务状态

```powershell
# 检查 nginx 服务
sc query nginx

# 检查 Python 后端
netstat -ano | findstr :5001

# 测试 API
Invoke-WebRequest -Uri http://127.0.0.1:5001/api/config/list -UseBasicParsing

# 查看 nginx 日志
Get-Content C:\nginx\logs\access.log -Tail 20
Get-Content C:\nginx\logs\error.log -Tail 20
```

### 回滚 Nginx 配置

```powershell
# 备份在 nginx.conf.bak / nginx.conf.bak2
Copy-Item C:\nginx\conf\nginx.conf.bak C:\nginx\conf\nginx.conf -Force
# 然后执行服务重启
```

---

## 七、完整 Nginx 配置参考

```nginx
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    types {
        text/html    html htm shtml;
        text/css     css;
        image/gif    gif;
        image/jpeg   jpeg jpg;
        application/javascript  js;
        image/png    png;
        image/webp   webp;
        image/x-icon ico;
        font/woff    woff;
        font/woff2   woff2;
        application/json  json;
    }
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    # HTTP -> HTTPS
    server {
        listen       80;
        server_name  oaai.xyz www.oaai.xyz;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS
    server {
        listen       443 ssl;
        server_name  oaai.xyz www.oaai.xyz;
        ssl_certificate      cert/oaai.xyz_bundle.crt;
        ssl_certificate_key  cert/oaai.xyz.key;
        ssl_ciphers  HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers  on;

        # SEO 验证文件
        location = /BingSiteAuth.xml { root C:/nginx/html; }
        location = /robots.txt       { root C:/nginx/html/compliance_site; }
        location = /sitemap.xml      { root C:/nginx/html/compliance_site; }

        # OA Fund Manager API
        location /api/ {
            proxy_pass http://127.0.0.1:3001/api/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
        }

        # OA Fund Manager 前端
        location /fond/ {
            proxy_pass http://127.0.0.1:3001/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
        }

        # OAAI Model-Radar 后端 API
        location /model-radar/api/ {
            proxy_pass http://127.0.0.1:5001/api/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_read_timeout 60s;
        }

        # OAAI Model-Radar 前端静态文件
        # 注意：必须用 alias，不能用 root！
        location /model-radar/ {
            alias C:/model-radar/;
            index index.html;
        }

        # 主站（合规学习网站）
        location / {
            root   C:/nginx/html/compliance_site;
            index  index.html index.htm;
            try_files $uri $uri/ /index.html;
        }
    }
}
```

---

## 八、项目文件结构（服务器端）

```
C:\model-radar\
├── index.html           # 前端单文件应用（React + Babel CDN，约 80KB）
├── server.py            # Python 标准库后端（零依赖，监听 5001 端口）
└── configs\
    └── 默认配置.json    # 初始空配置文件
```

---

## 九、自动化部署脚本一览

| 脚本文件 | 用途 |
|----------|------|
| `deploy_model_radar.py` | 主部署脚本 v4（文件上传 + 服务注册） |
| `deploy_nginx_clean.py` | 写入干净 Nginx 配置（base64 无 BOM） |
| `smart_restart.py` | 智能重启 nginx 服务（fire-and-forget） |
| `final_deploy.py` | 最终完整部署流程 |
| `verify_final.py` | 验证部署状态 |

所有脚本位于：`D:\OPENCLAW\`

---

## 十、FAQ

**Q：为什么不用 NSSM 注册 Python 服务？**  
A：NSSM 安装流程复杂（依赖网络下载），在腾讯云 Windows Server 上命令识别有问题。Python 后端以 `Start-Process -WindowStyle Hidden` 方式后台运行更简单可靠。缺点是服务器重启后需要手动重启后端进程。

**Q：Python 后端进程会在服务器重启后自动恢复吗？**  
A：不会。需要手动执行 `Start-Process` 命令重启，或者将启动命令加入 Windows 任务计划程序（开机触发）。

**Q：如何添加新的示例项目？**  
A：
1. 将项目文件上传到服务器 `C:\new-project\`
2. 若有后端，以指定端口启动（如 5002）
3. 在 `C:\nginx\conf\nginx.conf` 中添加新的 `location /new-project/` 块
4. 用 Windows 服务重启 nginx

**Q：浏览器有时显示旧的主站内容怎么办？**  
A：浏览器缓存问题，Ctrl+Shift+R 强制刷新，或访问 `https://oaai.xyz/model-radar/?v=2` 绕过缓存。
