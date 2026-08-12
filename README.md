# FastAPI Scaffold

一个开箱即用的 FastAPI 后端起步模板（分层结构 + 异步 SQLAlchemy + JWT 认证 + 统一响应 + Docker 一键起）。

## 特性

- **分层架构**：`core`（配置/数据库/安全/异常）· `models` · `schemas` · `api`（路由 + 依赖）· `services`（待扩展）
- **异步 ORM**：SQLAlchemy 2.0 async，默认 SQLite（零配置直接跑），一行切换 MySQL
- **JWT 认证**：`python-jose` + `passlib[bcrypt]`，OAuth2 密码流登录
- **统一响应 / 异常处理**：`AppError` → 统一错误信封 `{code, msg}`，422/500 自动拦截
- **CORS**：基于环境变量，前端联调友好
- **Docker / Compose**：`docker-compose up` 直接拉起 MySQL + 应用
- **CI**：GitHub Actions 跑 pytest

## 目录结构

```
fastapi-scaffold/
├── app/
│   ├── main.py              # 应用入口、路由注册、CORS、异常处理
│   ├── core/
│   │   ├── config.py        # pydantic-settings 配置
│   │   ├── database.py      # async engine / session / Base / init_db
│   │   ├── security.py      # JWT + 密码哈希
│   │   └── exceptions.py    # 统一异常处理器
│   ├── models/user.py       # SQLAlchemy 模型
│   ├── schemas/user.py      # Pydantic 出入参模型
│   └── api/
│       ├── deps.py          # 当前用户 / 超级用户依赖
│       └── routes/
│           ├── auth.py      # /api/auth/login、/me
│           └── users.py     # /api/users CRUD + 个人资料
├── tests/test_main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

## 快速开始（本地，零依赖）

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                 # 默认用 SQLite，开箱即跑
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

## 生产化建议

- 用 **Alembic** 管理数据库迁移，替换 `init_db()` 的 `create_all`
- 通过环境变量注入强随机 `SECRET_KEY`
- 关闭 `DEBUG`，配置正式 `CORS_ORIGINS`
- 添加限流、日志、健康检查探针（已有 `/health`）

## License

MIT
