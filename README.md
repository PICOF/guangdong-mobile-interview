# 广东移动系统开发面试准备

围绕广东移动省数智化部「系统开发」岗位整理的个人面试资料，包含120道问答，以及从中挑选的临场20题。参考公开招聘信息、公开面经和已确认的个人经历，不代表官方题库。

- [完整120题](https://picof.github.io/guangdong-mobile-interview/)
- [临场20题](https://picof.github.io/guangdong-mobile-interview/quick.html)

## 更新内容

编辑 `content/handbook.md` 并提交到 `main` 分支即可。临场20题从完整资料自动提取，不需要重复修改。

GitHub Actions 会安装构建依赖、生成页面、检查题号与链接，然后通过官方 Pages Actions 发布。也可以在 Actions 页面手动执行 `Deploy interview handbook to GitHub Pages`。

## 本地预览

需要 Python 3.12 或兼容版本。

```sh
python -m pip install -r requirements.txt
python scripts/build.py
python -m http.server 8000 --bind 127.0.0.1 --directory _site
```

浏览器打开 `http://127.0.0.1:8000/`。生成结果位于 `_site/`，不提交到源码仓库。

## 部署设置

GitHub 仓库 `Settings → Pages → Build and deployment → Source` 选择 **GitHub Actions**。工作流使用 `github-pages` 环境和默认 `GITHUB_TOKEN`，不需要另存个人访问令牌。

公开仓库使用 GitHub Pages 与标准 GitHub-hosted Actions 构建，当前方案无需付费服务器或自定义域名。

## 内容范围

仓库只包含面试问答、页面样式、构建脚本与部署配置。简历原件、个人信息文件、证件、原始实验资料、凭据与本地绝对路径均不上传。

页面保留现有问答中的姓名、教育与项目经历。站点可公开访问；`noindex` 和 `robots.txt` 仅请求搜索引擎不收录，并不构成访问控制。

资料核验日期为2026-10-20。引用保留在正文末尾，原本指向本地个人资料的链接已改为文字说明。个人学习资料，与中国移动及其下属单位无官方关联。
