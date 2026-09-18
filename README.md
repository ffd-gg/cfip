# cfip

拉取麒麟域名监测 (api.uouin.com) 的 CloudFlare 优选 IP，定时更新到 GitHub Gist。

订阅地址（跑起来后替换成你的用户名）：
https://gist.githubusercontent.com/YOUR_USER/GIST_ID/raw/cfip.txt

## 设置步骤
1. 创建 secret gist：https://gist.github.com （文件名必须叫 cfip.txt），记下 gist ID
2. 生成 classic PAT：https://github.com/settings/tokens 勾选 gist 权限
3. 仓库 Settings -> Secrets and variables -> Actions 新增 GIST_ID 和 GH_TOKEN
4. Actions 页手动触发 workflow_dispatch 验证

## 本地运行
python3 cf_fetch.py [输出文件]
