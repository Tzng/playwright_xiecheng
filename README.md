# 开始开发

## 配置清华源

注意：请在管理员环境下运行下面的操作

```
python3 -m pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple --user
```

官网的介绍：https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

## 安装依赖

安装依赖

```shell
pip3 install -r requirements.txt
```

安装需要的浏览器

```shell
playwright install
```

## 运行

prod模式启动项目

```shell
uvicorn theling_web_data.main:app --reload  --host 127.0.0.1 --port 9110 --workers 1 --reload --env-file env/prod.env
```