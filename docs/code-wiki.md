# 🔧 巧工艺墅（QiaoGongYiShu）· 项目 Code Wiki

---

## 一、项目概述

**巧工艺墅** 是一套面向农村自建房/别墅设计行业的全栈解决方案，包含三大子系统：
| 子系统 | 技术栈 | 运行端口 | 用途 |
|--------|--------|----------|------|
| **后端 API** | Flask 2.3 + SQLAlchemy + Redis | `5001` | 业务逻辑、数据存储、文件管理 |
| **管理后台** | Vue 3 + Element Plus + Vite | `3000` | 管理员管理产品/客户/分类等 |
| **微信小程序** | 原生小程序框架 | 微信开发者工具 | C 端用户浏览产品、提交咨询 |

---

## 二、项目目录结构

```
qiaogongyishu/
├── backend/                    # 后端 Flask 应用
│   ├── app/
│   │   ├── __init__.py         # Flask 工厂函数、上传路由
│   │   ├── config.py           # 配置类（开发/生产）
│   │   ├── extensions.py       # SQLAlchemy / Migrate / Redis 初始化
│   │   ├── api/                # API 蓝图（路由层）
│   │   ├── models/             # 数据模型（ORM 层）
│   │   ├── services/           # 业务逻辑层 + 存储抽象层
│   │   └── utils/              # 工具函数（装饰器/分页/响应）
│   ├── uploads/                # 本地文件存储目录
│   ├── instance/               # SQLite 数据库文件
│   ├── migrations/             # Alembic 数据库迁移
│   ├── run.py                  # 应用入口
│   └── requirements.txt        # Python 依赖
├── admin/                      # 管理后台 Vue3 SPA
│   ├── src/
│   │   ├── api/index.js        # API 封装层
│   │   ├── components/         # 布局组件
│   │   ├── router/index.js     # 路由配置 + 登录守卫
│   │   ├── store/index.js      # Vuex 状态管理
│   │   ├── utils/request.js    # Axios 请求拦截器
│   │   └── views/              # 页面组件
│   ├── vite.config.js          # Vite 配置 + 代理
│   └── package.json
├── miniprogram/                # 微信小程序
│   ├── app.js / app.json       # 小程序入口
│   ├── components/             # 可复用组件
│   ├── pages/                  # 页面
│   └── utils/                  # 请求封装 + 配置
└── docs/                       # 项目文档
```

---

## 三、后端架构详解

### 3.1 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| Web 框架 | Flask 2.3.3 | HTTP 路由、请求处理 |
| ORM | Flask-SQLAlchemy 3.1.1 | 数据库操作 |
| 数据库 | SQLite（开发） | 数据持久化 |
| 缓存 | Redis 5.0 | 分类/标签/Banner 缓存 |
| 认证 | PyJWT 2.8 | JWT Token 签发与验证 |
| 密码 | Werkzeug / passlib | 密码哈希 |
| 迁移 | Flask-Migrate / Alembic | 数据库版本管理 |
| 导出 | openpyxl / xlsxwriter | Excel 导出 |
| 存储 | 本地/OBS（抽象层） | 文件上传 |

### 3.2 应用启动流程

```
run.py
  └→ create_app()                [app/__init__.py]
       ├→ Config 加载             [app/config.py]
       ├→ init_extensions()       [app/extensions.py]  db / migrate / redis
       ├→ register_blueprints()   [app/api/__init__.py]  9个蓝图注册
       └→ 静态文件路由 /uploads/   [app/__init__.py]
  └→ CORS(app)                   [run.py]
  └→ app.run(5001)               [run.py]
  └→ init_data()                 [app/models/__init__.py]  预置数据
```

### 3.3 三层架构

```
API 层 (app/api/)         ← 蓝图路由，参数校验，调用服务层
   ↓
Service 层 (app/services/) ← 核心业务逻辑，缓存管理
   ↓
Model 层 (app/models/)    ← SQLAlchemy ORM 模型
```

### 3.4 API 蓝图一览

| 蓝图 | 前缀 | 文件 | 认证 |
|------|------|------|------|
| `auth_bp` | `/api/v1` | `app/api/auth.py` | 无需 |
| `product_bp` | `/api/v1` | `app/api/product.py` | 无需 |
| `category_bp` | `/api/v1` | `app/api/category.py` | 无需 |
| `tag_bp` | `/api/v1` | `app/api/tag.py` | 无需 |
| `banner_bp` | `/api/v1` | `app/api/banner.py` | 无需 |
| `customer_bp` | `/api/v1` | `app/api/customer.py` | 无需 |
| `upload_bp` | `/api/v1` | `app/api/upload.py` | 需要 |
| `admin_bp` | `/api/v1/admin` | `app/api/admin.py` | 需要 |
| `settings_bp` | `/api/v1` | `app/api/settings.py` | 部分需要 |

### 3.5 认证机制

**装饰器**：`admin_required` (位于 `app/utils/decorators.py`)

```
请求 → 提取 Authorization: Bearer <token>
     → jwt.decode(token, JWT_SECRET_KEY)
     → 查询 Admin 表验证身份
     → g.current_admin = admin
```

- JWT 算法：HS256
- Token 有效期：24 小时
- 密钥：`your-jwt-secret-key-here`

### 3.6 统一响应格式

**文件**：`app/utils/response.py`

```python
success(data, message)  → { code: 200, data, message }
error(code, message)    → { code, message, data: null }
paginated(items, page, per_page, total) → { items, total, page, per_page, pages }
```

### 3.7 缓存服务

**文件**：`app/services/cache_service.py`

三个缓存 key，均使用 Redis 存储（带降级到数据库查询）：

| Key | 内容 | TTL |
|-----|------|-----|
| `categories` | 分类列表 | 3600s (1h) |
| `tags` | 标签列表 | 3600s (1h) |
| `banners` | Banner 列表 | 1800s (30min) |

### 3.8 存储抽象层

**设计模式**：策略模式 + 工厂模式

```
StorageBackend (ABC)              [base.py]
├── LocalStorage                  [local.py]   本地文件存储
└── OSSStorage                    [oss.py]    阿里云 OSS 存储

get_storage_backend()             [factory.py] 单例工厂
reset_storage_backend()           [factory.py] 配置变更后重置
```

---

## 四、数据库模型与关系

### 4.1 ER 关系图

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   categories    │     │     products     │     │      tags       │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │──┐  │ id (PK)         │  ┌──│ id (PK)         │
│ name            │  └─→│ category_id (FK)│  │  │ name            │
│ sort_order      │     │ title           │  │  │ sort_order      │
│ is_active       │     │ model_number    │  │  │ is_active       │
│ created_at      │     │ description     │  │  └─────────────────┘
│ updated_at      │     │ floor_area      │  │          ↑
└─────────────────┘     │ building_area   │  │  ┌───────┴───────┐
                        │ rooms           │  │  │  product_tags │
                        │ view_count      │  │  ├───────────────┤
                        │ is_active       │  │  │ id (PK)       │
                        └────────┬────────┘  │  │ product_id(FK)│
                                 │           │  │ tag_id (FK)   │
                ┌────────────────┼───────────┘  │ UNIQUE(p,t)   │
                │                │              └───────────────┘
        ┌───────┴───────┐  ┌────┴────────┐
        │ product_images │  │  customers  │     ┌─────────────┐
        ├───────────────┤  ├─────────────┤     │   banners    │
        │ id (PK)       │  │ id (PK)     │     ├─────────────┤
        │ product_id(FK)│  │ name        │     │ id (PK)     │
        │ image_url     │  │ phone       │     │ title       │
        │ image_type    │  │ status      │     │ image_url   │
        │ sort_order    │  │ product_id  │     │ link_type   │
        └───────────────┘  │ source      │     │ is_active   │
                           └─────────────┘     └─────────────┘

┌──────────────┐  ┌───────────────┐  ┌──────────────────┐
│    admins    │  │ system_settings│  │  storage_configs │
├──────────────┤  ├───────────────┤  ├──────────────────┤
│ id (PK)      │  │ id (PK)       │  │ id (PK)          │
│ username     │  │ setting_key   │  │ storage_type     │
│ password_hash│  │ setting_value │  │ local_base_url   │
│ role         │  │ description   │  │ oss_* 字段        │
│ is_active    │  └───────────────┘  │ max_file_size    │
└──────────────┘                     └──────────────────┘
```

### 4.2 模型清单

| 模型 | 表名 | 文件 | 说明 |
|------|------|------|------|
| `Category` | `categories` | `app/models/category.py` | 产品分类（一层/二层/三层等） |
| `Tag` | `tags` | `app/models/tag.py` | 风格标签（新中式/欧式等） |
| `Product` | `products` | `app/models/product.py` | 产品/图纸 |
| `ProductImage` | `product_images` | `app/models/product_image.py` | 产品图片（banner/detail） |
| `ProductTag` | `product_tags` | `app/models/product_tag.py` | 产品-标签多对多关联 |
| `Banner` | `banners` | `app/models/banner.py` | 首页轮播图 |
| `Customer` | `customers` | `app/models/customer.py` | 客户咨询记录 |
| `Admin` | `admins` | `app/models/admin.py` | 管理员账号 |
| `SystemSetting` | `system_settings` | `app/models/system_setting.py` | 系统设置 KV 存储 |
| `StorageConfig` | `storage_configs` | `app/models/storage_config.py` | 文件存储配置 |

### 4.3 预置数据

**文件**：`app/models/__init__.py → init_data()`

首次启动自动创建：
- **分类**：一层、二层、三层、多层、双拼（5 个）
- **标签**：新中式、欧式、现代、中式（4 个）
- **管理员**：admin / admin123（超级管理员）
- **存储配置**：本地存储（默认）

---

## 五、管理后台前端详解

### 5.1 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| 框架 | Vue 3.4 | 响应式 UI |
| UI 库 | Element Plus 2.6 | 表格/表单/弹窗组件 |
| 路由 | Vue Router 4 | SPA 页面导航 |
| 状态管理 | Vuex 4 | Token/用户/侧边栏状态 |
| HTTP | Axios 1.6 | API 请求 |
| 图表 | ECharts 5.5 | 仪表盘图表 |
| 构建 | Vite 5.1 | 开发服务器 + 打包 |

### 5.2 路由系统

**文件**：`admin/src/router/index.js`

```
/login                        → 登录页（公开）
/                             → Layout（需认证）
  ├── /dashboard              → 仪表盘
  ├── /products /products/add /products/:id/edit  → 产品管理
  ├── /categories /categories/add /categories/:id/edit → 分类管理
  ├── /tags /tags/add /tags/:id/edit → 标签管理
  ├── /banners /banners/add /banners/:id/edit → Banner管理
  ├── /customers /customers/add /customers/:id → 客户管理
  └── /settings/storage /settings/customer-service /settings/change-password → 系统设置
```

**路由守卫**（`beforeEach`）：非登录页检查 `store.getters.token || localStorage.getItem('admin_token')`，无 token 跳转 `/login`。

### 5.3 请求拦截器

**文件**：`admin/src/utils/request.js`

```
请求拦截器 → 自动从 store 取 token 注入 Authorization header
响应拦截器 → 成功：提取 res.data（去壳）
           → 401：自动登出并跳转登录页
```

- baseURL: `/api/v1`
- 超时: 10000ms
- Vite 代理：`/api` → `http://localhost:5001`

### 5.4 API 封装

**文件**：`admin/src/api/index.js`

```javascript
authApi:     login                  → POST /api/v1/admin/auth/login
productApi:  list/get/create/update/delete → CRUD
categoryApi: list/get/create/update/delete → CRUD
tagApi:      list/get/create/update/delete → CRUD
bannerApi:   list/get/create/update/delete → CRUD
customerApi: list/get/create/updateStatus/updateRemark/delete/export
uploadApi:   upload                 → POST /api/v1/admin/upload/image
dashboardApi: stats                 → GET /api/v1/admin/dashboard
settingsApi: get/getAll/update      → 系统设置
```

> ⚠️ **注意**：`authApi.login` 使用独立的 axios 实例，不经过 request 拦截器，避免旧 token 导致 401。

### 5.5 状态管理

**文件**：`admin/src/store/index.js`

```javascript
state: {
  token,            // localStorage('admin_token') 持久化
  user,             // 当前管理员信息
  sidebarCollapsed  // 侧边栏折叠状态
}
actions: {
  login({ token, user }),  // 保存 token 和用户信息
  logout(),                 // 清除 token 和用户信息
  toggleSidebar()           // 切换侧边栏
}
```

---

## 六、微信小程序前端详解

### 6.1 技术栈

原生微信小程序框架（WXML + WXSS + JS）

### 6.2 页面结构

| 页面 | 路径 | 功能 |
|------|------|------|
| 首页 | `pages/index/index` | Banner 轮播 + 分类导航 + 风格筛选 + 产品列表 |
| 详情页 | `pages/detail/detail` | 产品详情 + 图片预览 + 表单入口 |
| 表单页 | `pages/form/form` | 客户咨询提交 |
| 搜索页 | `pages/search/search` | 关键词搜索 + 搜索历史 |
| 客服页 | `pages/customer-service/customer-service` | 客服二维码展示 |

### 6.3 自定义组件

| 组件 | 路径 | 属性/事件 |
|------|------|-----------|
| `banner-component` | `components/banner/` | banners, bind:click |
| `category-nav` | `components/category-nav/` | categories, activeCategory, showStyleFilter, tags, activeTag, bind:change, bind:styleTap, bind:tagChange |

### 6.4 请求封装

**文件**：`miniprogram/utils/request.js`

```javascript
baseUrl = app.globalData.apiBaseUrl  // http://localhost:5001/api/v1
// 封装 get/post/put/del 方法
// 自动处理 code===200 ? resolve(res.data.data) : reject(msg)
```

### 6.5 配置

**文件**：`miniprogram/utils/config.js`

```javascript
apiBaseUrl: 'http://localhost:5001/api/v1'
categoryNames: ['一层', '二层', '三层', '多层', '双拼']
tagNames: ['全部', '新中式', '欧式', '现代', '中式']
statusMap: { new:'新客户', contacted:'已联系', followed:'跟进中', closed:'已成交' }
```

---

## 七、核心业务流程

### 7.1 用户浏览产品流程

```
小程序首页 → GET /banners (Banner轮播)
          → GET /categories (分类导航)
          → GET /tags (风格标签)
          → GET /products?category_id=&tag_id=&page=&per_page= (产品列表)
          → POST /products/:id/view (记录浏览)
          → 点击产品 → GET /products/:id (产品详情)
          → 点击咨询 → 跳转表单页 → POST /customers (提交客户信息)
```

### 7.2 管理后台 CRUD 流程

```
登录 → POST /admin/auth/login → JWT Token
     → 仪表盘 GET /admin/dashboard
     → 产品管理 GET/POST/PUT/DELETE /admin/products
     → 分类管理 GET/POST/PUT/DELETE /admin/categories  → 清除缓存
     → 标签管理 GET/POST/PUT/DELETE /admin/tags        → 清除缓存
     → Banner管理 GET/POST/PUT/DELETE /admin/banners   → 清除缓存
     → 客户管理 GET/POST/PATCH /admin/customers
     → 导出客户 GET /admin/customers/export (xlsx)
     → 上传图片 POST /admin/upload/image (multipart)
```

### 7.3 图片上传与存储流程

```
前端上传 → POST /admin/upload/image (multipart/form-data)
         → UploadService.upload_image()
         → get_storage_backend()            [工厂获取实例]
         → storage.upload(file, filename)    [本地或OSS]
         → 返回完整 URL
         → 前端保存 URL 到产品/ Banner 表单
         → 提交产品/ Banner → 后端保存到 product_images 表
```

---

## 八、关键配置项

### 8.1 后端配置

**文件**：`backend/.env`

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SECRET_KEY` | `dev-secret-key` | Flask 密钥 |
| `JWT_SECRET_KEY` | `dev-jwt-secret-key` | JWT 签名密钥 |
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///./qiaogongyishu.db` | 数据库连接 |
| `REDIS_HOST` | `localhost` | Redis 主机 |
| `REDIS_PORT` | `6379` | Redis 端口 |
| `STORAGE_TYPE` | `local` | 存储类型（local/oss） |
| `LOCAL_BASE_URL` | `http://localhost:5001/uploads` | 本地文件访问 URL |

### 8.2 管理后台配置

**文件**：`admin/vite.config.js`

| 代理路径 | 目标 |
|----------|------|
| `/api` | `http://localhost:5001` |
| `/uploads` | `http://localhost:5001` |

### 8.3 小程序配置

**文件**：`miniprogram/project.config.json`

- AppID: `wx45a9077e1509a589`
- 基础库: `2.25.0`
- `urlCheck`: `false`（开发阶段关闭 URL 校验）

---

## 九、已知问题与改进建议

### 9.1 已知问题

| 问题 | 严重程度 | 位置 |
|------|----------|------|
| JWT 密钥硬编码 `your-jwt-secret-key-here` | 高 | `app/api/auth.py:L86` |
| `admin_required` 装饰器使用 `current_app.config['JWT_SECRET_KEY']` 而非登录时使用的相同密钥 | 高 | `app/utils/decorators.py:L12` |
| 微信登录为模拟实现，未接入真实微信 OAuth | 中 | `app/api/auth.py:L11` |
| Redis 未启动时缓存服务降级到数据库，但无日志警告 | 低 | `app/services/cache_service.py` |
| 小程序 `apiBaseUrl` 硬编码为 localhost，生产环境需修改 | 中 | `miniprogram/utils/config.js:L2` |

### 9.2 建议改进

1. **安全性**：将 JWT 密钥移至 `.env` 文件，保持登录签发与验证使用同一密钥
2. **生产部署**：小程序 `apiBaseUrl` 应改为 HTTPS 域名；管理后台应添加 nginx 反向代理
3. **Redis 依赖**：添加 Redis 连接失败时的日志告警，生产环境必须配置 Redis
4. **数据库**：生产环境建议使用 MySQL/PostgreSQL 替代 SQLite
5. **测试**：目前缺少单元测试和集成测试，建议添加 pytest 测试用例

---

## 十、开发运维命令

### 后端

```bash
# 安装依赖
cd backend && pip install -r requirements.txt

# 启动开发服务器（端口 5001）
python run.py

# 初始化数据库（首次运行）
flask init-db

# 数据库迁移
flask db init
flask db migrate -m "描述"
flask db upgrade
```

### 管理后台

```bash
# 安装依赖
cd admin && npm install

# 启动开发服务器（端口 3000）
npm run dev

# 构建生产版本
npm run build
```

### 微信小程序

```bash
# 使用微信开发者工具打开 miniprogram 目录
# 配置 → 项目设置 → 不校验合法域名（开发阶段）
```
