# FastAPI Scaffold

一个开箱即用的 FastAPI 后端起步模板（分层结构 + 异步 SQLAlchemy + JWT 认证 + 统一响应 + Docker 一键起）。

## 特性

- **分层架构**：`core`（配置/数据库/安全/异常）· `models` · `schemas` · `api`（路由 + 依赖）· `services`（待扩展）
- **异步 ORM**：SQLAlchemy 2.0 async，默认 SQLite（零配置直接跑），一行切换 MySQL
- **JWT 认证**：`python-jose` + `bcrypt`，OAuth2 密码流登录
- **统一响应 / 异常处理**：`AppError` → 统一错误信封 `{code, msg}`，422/500 自动拦截
- **CORS**：基于环境变量，前端联调友好
- **结构化日志**：`core/logging.py`，生产环境输出单行 JSON，DEBUG 下输出可读文本
- **数据库迁移**：Alembic（`migrations/`），生产环境用 `alembic upgrade head` 管理 schema
- **代码门禁**：ruff + pre-commit，CI 同步跑 lint
- **测试**：auth / users / health 的 pytest 用例
- **Docker / Compose**：`docker-compose up` 直接拉起 MySQL + 应用
- **CI**：GitHub Actions 跑 ruff + pytest
- **Makefile**：`make install/test/lint/migrate/run` 一键开发

## 目录结构

```
fastapi-scaffold/
├── app/
│   ├── main.py              # 应用入口、路由注册、CORS、异常处理、日志
│   ├── core/
│   │   ├── config.py        # pydantic-settings 配置
│   │   ├── database.py      # async engine / session / Base / init_db
│   │   ├── security.py      # JWT + 密码哈希
│   │   ├── exceptions.py    # 统一异常处理器
│   │   └── logging.py       # 结构化日志配置
│   ├── models/user.py       # SQLAlchemy 模型
│   ├── schemas/user.py      # Pydantic 出入参模型
│   └── api/
│       ├── deps.py          # 当前用户 / 超级用户依赖
│       └── routes/
│           ├── auth.py      # /api/auth/login、/me
│           └── users.py     # /api/users CRUD + 个人资料
├── migrations/              # Alembic 迁移
├── tests/                   # pytest 用例（auth / users / health）
├── Dockerfile
├── docker-compose.yml
├── requirements.txt         # 运行时依赖
├── requirements-dev.txt     # 开发 / lint 依赖（ruff, pre-commit）
├── ruff.toml                # ruff 配置
├── .pre-commit-config.yaml  # pre-commit 钩子
├── Makefile
├── pytest.ini
├── .env.example
└── README.md
```

## 快速开始（本地，零依赖）

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
make install                                        # 装运行时 + 开发依赖，并装 pre-commit
cp .env.example .env                                 # 默认用 SQLite，开箱即跑
make run                                            # uvicorn app.main:app --reload
```

或手动：

```bash
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

打开交互式文档：http://localhost:8000/docs

## 切换到 MySQL

1. 安装驱动：`pip install aiomysql`
2. 在 `.env` 中设置：
   ```
   DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/fastapi_scaffold
   ```

## Docker 一键起（含 MySQL）

```bash
docker-compose up --build
```

## 认证用法

```bash
# 1. 先建一个超级用户（手动插入或用 /api/users，需 superuser token）
# 2. 登录拿 token
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=admin@example.com&password=changeme" \
  -H "Content-Type: application/x-www-form-urlencoded"

# 3. 带 token 访问受保护接口
curl http://localhost:8000/api/auth/me -H "Authorization: Bearer <TOKEN>"
```

## 数据库迁移（Alembic）

开发期默认 `CREATE_TABLES_ON_STARTUP=true`，启动时用 `create_all` 建表，零配置即可跑。
生产环境请关闭自动建表并改用迁移：

```bash
# .env
CREATE_TABLES_ON_STARTUP=false

# 首次初始化（若已有表则 stamp 即可，无需重跑）
alembic upgrade head
# 或：python -m alembic upgrade head
```

新增模型字段后生成迁移：

```bash
alembic revision --autogenerate -m "add column xxx"
alembic upgrade head
```

## 代码门禁

```bash
make lint     # ruff check + format --check
make format   # ruff format + check --fix
```

CI 中已集成 `ruff check .` 与 `pytest -q`。

## 生产化建议

- 通过环境变量注入强随机 `SECRET_KEY`
- 关闭 `DEBUG`，配置正式 `CORS_ORIGINS`
- 用 Alembic 管理 schema（已内置）
- 添加限流、健康检查探针（已有 `/health`）

## License

MIT
