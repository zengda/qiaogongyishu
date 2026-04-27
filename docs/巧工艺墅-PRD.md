# 巧工艺墅 - 微信小程序 PRD 产品需求文档

> **文档版本**: v2.0
> **创建日期**: 2026-04-26
> **最后更新**: 2026-04-27
> **项目类型**: 微信小程序 + 管理后台
> **开发方式**: Trae IDE Vibe Coding
> **面向读者**: Trae IDE AI 编程助手（作为项目上下文输入）
> **数据库版本**: MySQL 8.0

---

## 一、项目概述

### 1.1 项目背景

"巧工艺墅"是一个面向农村自建房（乡村别墅）客户的图纸展示与获客小程序。售前客服人员通过微信聊天将小程序转发给潜在客户，客户通过浏览首页展示的设计图纸产品，了解我方设计实力，并表达建房意向。

### 1.2 核心目标

1. **展示设计实力**：通过精美的图纸产品展示，让客户直观感受设计水平
2. **客户获客转化**：通过"领取图纸"表单收集意向客户信息，建立销售线索
3. **客服引导成交**：通过在线客服入口引导客户添加微信，完成深度沟通

### 1.3 目标用户

- **C端用户**：有农村自建房/乡村别墅需求的潜在客户
- **B端用户**：售前客服人员（通过管理后台管理内容和查看客户信息）

---

## 二、技术架构

### 2.1 技术栈

| 层级 | 技术选型 | 版本要求 |
|------|---------|---------|
| 小程序前端 | 微信小程序原生开发（WXML + WXSS + JS） | 基础库 >= 2.25.0 |
| 后端框架 | Python + Flask | Python 3.12+, Flask 3.x |
| 数据库 | MySQL | 8.0 |
| 缓存 | Redis | 7.0+ |
| 图片/文件存储 | 本地存储 + 阿里云 OSS（管理后台可切换） | - |
| 管理后台前端 | Vue 3 + Element Plus | Vue 3.4+, Element Plus 2.x |

### 2.2 数据库选型说明

选择 **MySQL 8.0** 的理由：
- 图纸产品数据结构明确，关系型数据，适合关系型数据库
- 支持事务，保证数据一致性（如表单提交、产品增删改）
- 查询性能优秀，支持全文索引（搜索功能）
- 支持 JSON 字段类型，便于存储灵活的配置数据
- 运维成熟，社区资源丰富

选择 **Redis** 的理由：
- 缓存首页 Banner、分类列表等高频访问数据
- 缓存热门图纸产品列表，提升小程序加载速度
- 存储表单提交频率限制，防止恶意提交

### 2.3 项目目录结构

```
qiaogongyishu/
├── miniprogram/                  # 微信小程序前端
│   ├── pages/
│   │   ├── index/               # 首页
│   │   ├── detail/              # 图纸产品详情页
│   │   ├── customer-service/    # 在线客服页（微信二维码）
│   │   └── form/                # 领取图纸表单页
│   ├── components/              # 公共组件
│   │   ├── banner/              # 轮播图组件
│   │   ├── category-nav/        # 分类导航组件
│   │   ├── style-filter/        # 风格筛选组件
│   │   ├── product-card/        # 图纸产品卡片组件
│   │   └── search-bar/          # 搜索框组件
│   ├── utils/
│   │   ├── request.js           # 网络请求封装
│   │   ├── auth.js              # 登录授权工具
│   │   └── config.js            # 配置文件（API地址等）
│   ├── images/                  # 本地静态图片资源
│   ├── app.js
│   ├── app.json
│   ├── app.wxss
│   └── project.config.json
│
├── backend/                      # Flask 后端
│   ├── app/
│   │   ├── __init__.py          # Flask 应用工厂
│   │   ├── config.py            # 配置文件
│   │   ├── extensions.py        # Flask 扩展初始化
│   │   ├── models/              # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── product.py       # 图纸产品模型
│   │   │   ├── category.py      # 分类模型
│   │   │   ├── banner.py        # Banner模型
│   │   │   ├── customer.py      # 咨询客户模型
│   │   │   └── tag.py           # 风格标签模型
│   │   ├── api/                 # API 蓝图
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # 登录授权API
│   │   │   ├── product.py       # 图纸产品API
│   │   │   ├── category.py      # 分类API
│   │   │   ├── banner.py        # Banner API
│   │   │   ├── customer.py      # 咨询客户API
│   │   │   ├── upload.py        # 文件上传API
│   │   │   └── admin.py         # 管理后台API
│   │   ├── services/            # 业务逻辑层
│   │   │   ├── product_service.py
│   │   │   ├── customer_service.py
│   │   │   ├── upload_service.py
│   │   │   ├── cache_service.py
│   │   │   └── storage/         # 存储服务层（策略模式）
│   │   │       ├── __init__.py
│   │   │       ├── base.py      # 存储服务抽象基类（StorageBackend）
│   │   │       ├── local.py     # 本地存储实现
│   │   │       ├── oss.py       # 阿里云OSS存储实现
│   │   │       └── factory.py   # 存储服务工厂（根据配置创建实例）
│   │   └── utils/               # 工具函数
│   │       ├── response.py      # 统一响应格式
│   │       ├── decorators.py    # 装饰器（登录验证等）
│   │       └── pagination.py    # 分页工具
│   ├── migrations/              # 数据库迁移
│   ├── requirements.txt
│   ├── .env                     # 环境变量
│   └── run.py                   # 启动入口
│
├── admin/                        # 管理后台前端（Vue 3）
│   ├── src/
│   │   ├── views/
│   │   │   ├── login/           # 登录页
│   │   │   ├── dashboard/       # 仪表盘
│   │   │   ├── product/         # 图纸产品管理
│   │   │   ├── category/        # 分类管理
│   │   │   ├── banner/          # Banner管理
│   │   │   ├── customer/        # 咨询客户管理
│   │   │   └── tag/             # 风格标签管理
│   │   ├── components/          # 公共组件
│   │   ├── api/                 # API 请求
│   │   ├── router/              # 路由
│   │   ├── store/               # 状态管理
│   │   └── utils/               # 工具函数
│   ├── package.json
│   └── vite.config.js
│
└── docs/                         # 项目文档
    ├── prd.md                   # 本文档
    └── api-spec.yaml            # OpenAPI 3.0 接口规范（前后端开发唯一依据）
```

---

## 三、数据库设计

### 3.1 ER 关系

```
Category (分类)  1──N  Product (图纸产品)  N──M  Tag (风格标签)
                                          1──N  ProductImage (产品图片)
Banner (轮播图)                    1──N  Customer (咨询客户)
StorageConfig (存储配置)           1──1  系统全局配置（单例）
```

### 3.2 数据表结构

#### 3.2.1 categories - 分类表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| name | VARCHAR(50), NOT NULL, UNIQUE | 分类名称（一层/二层/三层/多层/双拼） |
| sort_order | INT, DEFAULT 0 | 排序权重，值越大越靠前 |
| is_active | TINYINT(1), DEFAULT 1 | 是否启用 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 3.2.2 tags - 风格标签表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| name | VARCHAR(50), NOT NULL, UNIQUE | 标签名称（新中式/欧式/现代/中式） |
| sort_order | INT, DEFAULT 0 | 排序权重 |
| is_active | TINYINT(1), DEFAULT 1 | 是否启用 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 3.2.3 products - 图纸产品表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| title | VARCHAR(200), NOT NULL | 图纸标题 |
| model_number | VARCHAR(100), NOT NULL | 图纸型号 |
| category_id | INT, FK -> categories.id | 所属分类 |
| description | TEXT | 图纸简介 |
| floor_area | VARCHAR(50) | 建筑面积（如"180㎡"） |
| building_area | VARCHAR(50) | 占地面积（如"120㎡"） |
| rooms | VARCHAR(50) | 户型（如"4室2厅3卫"） |
| sort_order | INT, DEFAULT 0 | 排序权重 |
| view_count | INT, DEFAULT 0 | 浏览次数 |
| is_active | TINYINT(1), DEFAULT 1 | 是否上架 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 3.2.4 product_images - 产品图片表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| product_id | INT, FK -> products.id | 所属产品 |
| image_url | VARCHAR(500), NOT NULL | 图片URL（OSS地址） |
| image_type | ENUM('banner','detail') | 图片类型：banner=轮播主图, detail=详情图 |
| sort_order | INT, DEFAULT 0 | 排序权重 |
| created_at | DATETIME | 创建时间 |

#### 3.2.5 product_tags - 产品标签关联表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| product_id | INT, FK -> products.id | 产品ID |
| tag_id | INT, FK -> tags.id | 标签ID |
| UNIQUE KEY (product_id, tag_id) | | 联合唯一索引 |

#### 3.2.6 banners - 轮播图表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| title | VARCHAR(200) | Banner标题 |
| image_url | VARCHAR(500), NOT NULL | 图片URL（OSS地址） |
| link_type | ENUM('none','product','category','url') | 跳转类型 |
| link_value | VARCHAR(500) | 跳转值（产品ID/分类ID/URL） |
| sort_order | INT, DEFAULT 0 | 排序权重 |
| is_active | TINYINT(1), DEFAULT 1 | 是否启用 |
| start_time | DATETIME | 展示开始时间 |
| end_time | DATETIME | 展示结束时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 3.2.7 customers - 咨询客户表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| name | VARCHAR(50), NOT NULL | 客户姓名 |
| phone | VARCHAR(20), NOT NULL | 手机号码 |
| wechat | VARCHAR(100) | 微信号 |
| province | VARCHAR(50) | 省份 |
| city | VARCHAR(50) | 城市 |
| building_area_budget | VARCHAR(100) | 建房面积预算 |
| product_id | INT, FK -> products.id, NULLABLE | 意向产品ID（从哪个产品页进入的表单） |
| product_title | VARCHAR(200) | 意向产品标题（冗余存储） |
| source | VARCHAR(50) | 来源渠道（小程序） |
| status | ENUM('new','contacted','followed','closed'), DEFAULT 'new' | 跟进状态 |
| remark | TEXT | 备注 |
| created_at | DATETIME | 创建时间（提交时间） |
| updated_at | DATETIME | 更新时间 |

#### 3.2.8 admins - 管理员表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| username | VARCHAR(50), NOT NULL, UNIQUE | 用户名 |
| password_hash | VARCHAR(255), NOT NULL | 密码哈希 |
| real_name | VARCHAR(50) | 真实姓名 |
| role | ENUM('super','admin'), DEFAULT 'admin' | 角色 |
| is_active | TINYINT(1), DEFAULT 1 | 是否启用 |
| last_login_at | DATETIME | 最后登录时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 3.2.9 system_settings - 系统设置表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| setting_key | VARCHAR(100), NOT NULL, UNIQUE | 设置键名 |
| setting_value | TEXT | 设置值 |
| description | VARCHAR(255) | 说明 |
| updated_at | DATETIME | 更新时间 |

> 预置数据：`customer_service_qrcode`（客服微信二维码图片URL）

#### 3.2.10 storage_configs - 存储配置表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT, PK, AUTO_INCREMENT | 主键 |
| storage_type | ENUM('local','oss'), NOT NULL, DEFAULT 'local' | 存储类型：local=本地存储, oss=阿里云OSS |
| local_base_url | VARCHAR(500) | 本地存储的基础访问URL（如 http://localhost:5000/uploads） |
| local_upload_path | VARCHAR(500) | 本地存储的上传目录路径（如 /app/uploads） |
| oss_access_key_id | VARCHAR(200) | 阿里云 OSS AccessKey ID |
| oss_access_key_secret | VARCHAR(500) | 阿里云 OSS AccessKey Secret（加密存储） |
| oss_bucket_name | VARCHAR(200) | OSS Bucket 名称 |
| oss_endpoint | VARCHAR(500) | OSS Endpoint（如 oss-cn-hangzhou.aliyuncs.com） |
| oss_cdn_domain | VARCHAR(500) | OSS CDN 加速域名（如 https://cdn.example.com） |
| oss_custom_domain | VARCHAR(500) | OSS 自定义域名（可选，绑定了CNAME的域名） |
| oss_region | VARCHAR(100) | OSS 地域（如 cn-hangzhou） |
| max_file_size | INT, DEFAULT 5242880 | 最大文件大小（字节），默认5MB |
| allowed_extensions | VARCHAR(500), DEFAULT 'jpg,jpeg,png,webp,gif' | 允许的文件扩展名（逗号分隔） |
| is_active | TINYINT(1), DEFAULT 1 | 是否为当前生效配置 |
| updated_at | DATETIME | 最后更新时间 |
| created_at | DATETIME | 创建时间 |

> **设计说明**：
> - 此表采用**单例模式**，系统中只保留一条 `is_active=1` 的记录作为当前生效配置
> - 切换存储方式时，将原记录 `is_active` 设为 0，新记录设为 1
> - `oss_access_key_secret` 在数据库中加密存储，管理后台展示时脱敏显示（如 `LTAI5t**********3xKp`）
> - 本地存储模式下，`local_base_url` 用于生成可访问的图片 URL
> - OSS 模式下，优先使用 `oss_cdn_domain`，其次使用 `oss_custom_domain`，最后使用 `oss_endpoint + bucket`

---

## 四、微信小程序端 - 页面详细设计

### 4.0 全局设计规范

- **无底部 TabBar**：小程序不设置底部菜单栏
- **导航栏**：使用微信默认导航栏，标题为"巧工艺墅"
- **主题色**：`#1A6D5C`（深青绿色，体现建筑/工匠质感）
- **辅助色**：`#F5A623`（暖金色，用于按钮和强调）
- **背景色**：`#F7F8FA`（浅灰白色）
- **字体**：使用系统默认字体
- **图片懒加载**：所有图片使用懒加载，提升首屏加载速度
- **下拉刷新**：首页支持下拉刷新
- **分享功能**：所有页面支持转发分享给微信好友

### 4.1 首页（pages/index/index）

**页面路径**: `/pages/index/index`

**页面布局**（从上往下）：

```
┌─────────────────────────────────┐
│         Banner 轮播图            │  ← 自动轮播，3-5秒切换，支持手势滑动
│     （高度：360rpx）             │
├─────────────────────────────────┤
│  🔍 搜索框                       │  ← 点击跳转搜索页/弹出搜索面板
├─────────────────────────────────┤
│  分类标签导航频道                  │  ← 横向滚动
│  [一层] [二层] [三层] [多层] [双拼] [🏷风格] │
├─────────────────────────────────┤
│  风格筛选栏（点击"风格"后展开）      │  ← 条件展开，默认收起
│  [全部] [新中式] [欧式] [现代] [中式]  │
├─────────────────────────────────┤
│  图纸产品瀑布流/双列列表           │  ← 每行2个卡片
│  ┌──────┐  ┌──────┐            │
│  │ 图片  │  │ 图片  │            │
│  │ 标题  │  │ 标题  │            │
│  └──────┘  └──────┘            │
│  ┌──────┐  ┌──────┐            │
│  │ ...  │  │ ...  │            │
│  └──────┘  └──────┘            │
│                                 │
│        上拉加载更多               │
└─────────────────────────────────┘
```

**交互说明**：

1. **Banner 轮播图**
   - 自动轮播，间隔 3 秒
   - 支持手势左右滑动
   - 点击可跳转（跳转类型由后台配置：产品详情/分类页/外部链接）
   - 圆角指示器（小圆点）

2. **搜索框**
   - 点击搜索框 → 弹出搜索面板（非新页面），支持按标题/型号搜索图纸
   - 搜索历史记录（本地存储，最多10条）
   - placeholder 文案："搜索图纸型号、名称"

3. **分类标签导航频道**
   - 横向排列，超出屏幕可横向滚动
   - 当前选中分类高亮显示（主题色背景 + 白色文字）
   - 默认选中"一层"
   - 最右侧为"风格"标签按钮（带图标 icon），点击展开/收起风格筛选栏
   - 点击分类标签 → 切换分类，刷新产品列表
   - 点击"风格"按钮 → 展开/收起风格筛选栏（带动画过渡）

4. **风格筛选栏**
   - 默认收起状态
   - 点击"风格"按钮后展开（高度动画过渡）
   - 包含标签：全部、新中式、欧式、现代、中式
   - "全部"为默认选中状态
   - 选中风格标签后，与当前分类进行联合筛选
   - 再次点击"风格"按钮可收起

5. **图纸产品列表**
   - 双列瀑布流布局
   - 每个产品卡片包含：封面图、标题、面积信息
   - 图片比例 4:3，圆角 12rpx
   - 标题最多显示2行，超出省略号
   - 面积信息显示在标题下方，灰色小字
   - 点击卡片 → 跳转产品详情页
   - 上拉触底加载更多（分页加载，每页10条）
   - 加载中显示 loading 骨架屏

**数据接口**：

```
GET /api/v1/banners              # 获取Banner列表
GET /api/v1/categories           # 获取分类列表
GET /api/v1/tags                 # 获取风格标签列表
GET /api/v1/products?category_id=1&tag_id=2&page=1&per_page=10&keyword=xxx  # 获取产品列表（支持分类、标签、搜索联合筛选）
```

---

### 4.2 图纸产品详情页（pages/detail/detail）

**页面路径**: `/pages/detail/detail?id={product_id}`

**页面布局**：

```
┌─────────────────────────────────┐
│      主图轮播图（Swiper）         │  ← 全宽，高度 600rpx
│     ← [图1] [图2] [图3] →       │     支持手势滑动，点击可预览大图
├─────────────────────────────────┤
│  图纸标题                        │  ← 大号加粗
│  型号：QGY-2026-001              │  ← 灰色小字
├─────────────────────────────────┤
│  ┌─────┬─────┬─────┐           │
│  │建筑面积│占地面积│ 户型  │           │  ← 基本参数信息栏
│  │ 180㎡ │ 120㎡ │4室2厅 │           │
│  └─────┴─────┴─────┘           │
├─────────────────────────────────┤
│                                 │
│         图纸详情图                │  ← 纵向排列展示所有详情图
│         （多张图片）              │     图片宽度100%，点击可预览大图
│         ...                     │
│                                 │
├─────────────────────────────────┤
│  ┌─────────────────────────┐   │  ← 固定在页面底部
│  │ 建房详情咨询设计顾问       │   │
│  │ 添加下方微信客服          │   │
│  │ [在线客服]  [领取图纸]    │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

**交互说明**：

1. **主图轮播图**
   - 展示该产品的 banner 类型图片（product_images 表中 image_type='banner'）
   - 支持手势左右滑动切换
   - 点击图片 → 调用 wx.previewImage 预览大图，支持左右滑动查看所有主图
   - 底部显示当前图片序号指示器（1/5）

2. **产品基本信息**
   - 标题：大号字体加粗显示
   - 型号：灰色小字，"型号："前缀
   - 基本参数栏：三列布局，展示建筑面积、占地面积、户型
   - 如果某些字段为空则隐藏对应列

3. **图纸详情图**
   - 纵向排列展示所有详情图片（product_images 表中 image_type='detail'）
   - 图片宽度 100%，自适应高度
   - 点击图片 → 调用 wx.previewImage 预览大图
   - 图片懒加载

4. **底部固定栏**
   - 固定在页面底部，不随页面滚动
   - 上方文字："建房详情咨询设计顾问" + "添加下方微信客服"
   - 两个按钮并排：
     - **在线客服**：主题色按钮，点击跳转客服页面
     - **领取图纸**：辅助色（暖金色）按钮，点击跳转表单页面
   - 底部安全区域适配（iPhone 底部横条）

5. **页面分享**
   - 支持转发给好友，分享卡片显示产品封面图 + 标题

**数据接口**：

```
GET /api/v1/products/{id}        # 获取产品详情（含主图和详情图）
POST /api/v1/products/{id}/view  # 记录浏览次数（PV统计）
```

---

### 4.3 在线客服页（pages/customer-service/customer-service）

**页面路径**: `/pages/customer-service/customer-service`

**页面布局**：

```
┌─────────────────────────────────┐
│  ← 在线客服                      │  ← 导航栏
├─────────────────────────────────┤
│                                 │
│                                 │
│      ┌───────────────┐         │
│      │               │         │
│      │  客服微信二维码  │         │  ← 居中展示，带白色边框和阴影
│      │               │         │
│      └───────────────┘         │
│                                 │
│     微信扫一扫，添加客服          │
│     为您一对一解答建房疑问        │
│                                 │
│     ┌─────────────────┐        │
│     │  长按保存二维码   │        │  ← 提示文字
│     └─────────────────┘        │
│                                 │
└─────────────────────────────────┘
```

**交互说明**：

1. 页面居中展示客服微信二维码图片
2. 二维码图片支持长按保存到手机相册
3. 二维码下方有引导文案
4. 二维码图片 URL 来自系统设置（system_settings 表的 `customer_service_qrcode`）

**数据接口**：

```
GET /api/v1/settings/customer_service_qrcode  # 获取客服二维码URL
```

---

### 4.4 领取图纸表单页（pages/form/form）

**页面路径**: `/pages/form/form?product_id={product_id}&product_title={title}`

> 如果从非产品页进入，product_id 和 product_title 为空

**页面布局**：

```
┌─────────────────────────────────┐
│  ← 领取图纸                      │  ← 导航栏
├─────────────────────────────────┤
│                                 │
│  ┌─────────────────────────┐   │
│  │  您好！请填写以下信息      │   │
│  │  我们将为您发送详细图纸    │   │
│  └─────────────────────────┘   │
│                                 │
│  姓名 *                         │
│  ┌─────────────────────────┐   │
│  │  请输入您的姓名           │   │
│  └─────────────────────────┘   │
│                                 │
│  手机号 *                       │
│  ┌─────────────────────────┐   │
│  │  请输入您的手机号         │   │
│  └─────────────────────────┘   │
│                                 │
│  微信号                         │
│  ┌─────────────────────────┐   │
│  │  请输入您的微信号（选填）  │   │
│  └─────────────────────────┘   │
│                                 │
│  所在省市                       │
│  ┌─────────────────────────┐   │
│  │  请选择您所在的省市       │   │  ← 使用微信地区选择器
│  └─────────────────────────┘   │
│                                 │
│  建房面积预算                    │
│  ┌─────────────────────────┐   │
│  │  请输入您的建房面积预算    │   │
│  └─────────────────────────┘   │
│                                 │
│  ┌─────────────────────────┐   │
│  │     点击获取房屋图纸       │   │  ← 主题色按钮，固定底部
│  └─────────────────────────┘   │
│                                 │
└─────────────────────────────────┘
```

**表单字段说明**：

| 字段 | 必填 | 类型 | 校验规则 | placeholder |
|------|------|------|---------|-------------|
| 姓名 | 是 | 文本 | 2-20个字符 | 请输入您的姓名 |
| 手机号 | 是 | 数字 | 11位手机号正则校验 | 请输入您的手机号 |
| 微信号 | 否 | 文本 | 最多50个字符 | 请输入您的微信号（选填） |
| 所在省市 | 否 | 地区选择 | 使用微信原生地区选择器 | 请选择您所在的省市 |
| 建房面积预算 | 否 | 文本 | 最多100个字符 | 请输入您的建房面积预算 |

**交互说明**：

1. 表单顶部显示引导文案
2. 如果从产品详情页进入，页面顶部显示意向产品信息卡片（产品封面缩略图 + 标题）
3. 必填字段标有红色 `*` 号
4. 手机号输入框使用 `type="number"` 键盘，限制输入11位数字
5. 所在省市使用微信原生地区选择器（`wx.chooseRegion`）
6. 提交按钮固定在页面底部
7. 点击"点击获取房屋图纸"按钮：
   - 前端校验必填字段
   - 校验通过 → 提交表单
   - 提交成功 → 弹出成功弹窗："提交成功！我们的设计顾问将尽快与您联系"
   - 弹窗有"确定"按钮，点击后返回首页
8. 防重复提交：按钮点击后禁用，显示 loading 状态
9. 同一手机号限制每分钟提交1次（后端校验）

**数据接口**：

```
POST /api/v1/customers           # 提交客户表单
```

请求体：
```json
{
  "name": "张三",
  "phone": "13800138000",
  "wechat": "zhangsan_wx",
  "province": "广东省",
  "city": "广州市",
  "building_area_budget": "200-300㎡",
  "product_id": 1,
  "product_title": "新中式三层别墅"
}
```

---

### 4.5 搜索页（pages/search/search）

**页面路径**: `/pages/search/search`

**页面布局**：

```
┌─────────────────────────────────┐
│  ← 🔍 [搜索框] [取消]           │  ← 自动聚焦
├─────────────────────────────────┤
│  搜索历史                        │
│  [历史1] [历史2] [历史3]         │  ← 点击直接搜索
│                    [清空]       │
├─────────────────────────────────┤
│  热门搜索                        │
│  [热门1] [热门2] [热门3]         │
├─────────────────────────────────┤
│  搜索结果列表（输入关键词后展示）   │  ← 与首页产品列表样式一致
│  ...                            │
└─────────────────────────────────┘
```

**交互说明**：

1. 进入页面自动聚焦搜索框
2. 搜索历史存储在本地（wx.setStorageSync），最多保留10条
3. 支持清空搜索历史
4. 输入关键词后实时搜索（防抖 500ms）
5. 搜索结果为空时展示空状态提示

---

## 五、管理后台 - 页面详细设计

### 5.0 管理后台概述

- **技术栈**：Vue 3 + Element Plus + Vite
- **布局**：经典左侧栏 + 顶部栏 + 内容区布局
- **登录认证**：账号密码登录，JWT Token 认证（详见 5.1.1）
- **响应式**：适配 PC 端浏览器

### 5.0.1 管理后台 UI 样式规范

**左侧边栏（深色主题）**：

| 样式项 | 值 | 说明 |
|--------|-----|------|
| 背景色 | `#1D1E2C` | 深蓝黑色，沉稳专业 |
| 菜单文字颜色 | `#FFFFFF` | 白色，确保深色背景下的可读性 |
| 菜单文字大小 | `14px` | 统一字体大小，所有菜单项一致 |
| 菜单文字字重 | `400` (normal) | 常规字重 |
| 菜单项高度 | `56px` | 每个菜单项高度一致 |
| 菜单项内边距 | `0 20px` | 左右内边距 |
| 菜单悬停背景色 | `#2D2E3E` | 鼠标悬停时略微变亮 |
| 菜单选中背景色 | `#1A6D5C`（主题色） | 当前选中菜单项高亮 |
| 菜单选中文字颜色 | `#FFFFFF` | 选中状态文字仍为白色 |
| 子菜单缩进 | `20px` | 二级菜单相对一级菜单缩进 |
| Logo 区域高度 | `64px` | 顶部 Logo/系统名称区域 |
| Logo 区域背景色 | `#16172A` | 比 sidebar 略深，形成层次 |
| 左侧栏宽度 | `220px` | 固定宽度，不可折叠 |

**顶部栏**：

| 样式项 | 值 | 说明 |
|--------|-----|------|
| 背景色 | `#FFFFFF` | 白色背景 |
| 高度 | `56px` | 固定高度 |
| 右侧用户区域 | 头像 + 用户名 + 退出按钮 | |

**内容区**：

| 样式项 | 值 | 说明 |
|--------|-----|------|
| 背景色 | `#F0F2F5` | 浅灰色背景 |
| 内边距 | `20px` | 内容区域四周留白 |
| 卡片背景色 | `#FFFFFF` | 白色卡片 |
| 卡片圆角 | `8px` | 统一圆角 |
| 卡片阴影 | `0 2px 12px rgba(0,0,0,0.06)` | 轻微阴影 |

### 5.1 登录页

- 用户名 + 密码登录
- 默认管理员账号：admin / admin123（首次登录后强制修改密码）

#### 5.1.1 JWT 用户认证设计

**认证流程**：

```
┌──────────┐     POST /admin/auth/login      ┌──────────┐
│  管理后台  │ ──── {username, password} ────→ │  后端API  │
│  前端     │                                  │          │
│          │ ←── {token, user_info} ──────── │          │
└──────────┘                                  └──────────┘
     │
     │  后续请求 Header: Authorization: Bearer <token>
     ▼
┌──────────┐     GET /admin/xxx               ┌──────────┐
│  管理后台  │ ──── Authorization: Bearer ────→ │  后端API  │
│  前端     │                                  │  (验证JWT)│
│          │ ←── 200 OK / 401 Unauthorized ── │          │
└──────────┘                                  └──────────┘
```

**JWT Token 规范**：

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 签名算法 | HS256 | HMAC SHA-256 |
| Token 有效期 | 24 小时 | 过期后需重新登录 |
| Token 存储位置 | localStorage | 前端存储在浏览器 localStorage |
| Token 请求头 | `Authorization: Bearer <token>` | 每次请求携带 |
| Payload 字段 | `user_id`, `username`, `role`, `exp`, `iat` | Token 载荷内容 |

**登录接口详情**：

- **请求**: `POST /api/v1/admin/auth/login`
- **请求体**: `{"username": "admin", "password": "admin123"}`
- **成功响应**: `{"code": 200, "message": "success", "data": {"token": "eyJhbG...", "user": {"id": 1, "username": "admin", "real_name": "管理员", "role": "super"}}}`
- **失败响应**: `{"code": 401, "message": "用户名或密码错误", "data": null}`

**前端认证拦截器**：

```javascript
// axios 请求拦截器 - 自动附加 Token
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// axios 响应拦截器 - 401 自动跳转登录
axios.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token')
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    }
    return Promise.reject(error)
  }
)
```

**后端 JWT 装饰器**：

```python
# backend/app/utils/decorators.py
from functools import wraps
import jwt
from flask import request, current_app, g

def admin_required(f):
    """管理员登录验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return {"code": 401, "message": "未提供认证Token", "data": None}, 401
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            g.current_admin_id = payload['user_id']
            g.current_admin_role = payload['role']
        except jwt.ExpiredSignatureError:
            return {"code": 401, "message": "Token已过期，请重新登录", "data": None}, 401
        except jwt.InvalidTokenError:
            return {"code": 401, "message": "无效的Token", "data": None}, 401
        return f(*args, **kwargs)
    return decorated
```

**安全措施**：
- 密码使用 `werkzeug.security.generate_password_hash` 加密存储（pbkdf2:sha256）
- 登录失败连续 5 次后锁定账号 30 分钟
- Token 过期后前端自动清除并跳转登录页
- 同一账号不允许多设备同时登录（可选，通过 Redis 记录活跃 Token）

### 5.2 左侧导航栏菜单结构

```
仪表盘（Dashboard）
图纸产品管理
    ├── 产品列表（增删改查）
    └── 添加产品
分类管理（增删改）
风格标签管理（增删改）
Banner管理（增删改）
咨询客户
    ├── 客户列表（查看、标记状态、添加备注）
    └── 客户导出（导出Excel）
系统设置
    ├── 存储配置（本地存储/阿里云OSS切换）
    ├── 客服二维码设置
    └── 修改密码
```

### 5.3 仪表盘（Dashboard）

**内容**：
- 今日新增客户数 / 本周新增客户数 / 本月新增客户数
- 图纸产品总数 / 上架产品数
- 最近7天客户咨询趋势图（折线图）
- 最新咨询客户列表（最近10条）

### 5.4 图纸产品管理

#### 5.4.1 产品列表页

**表格列**：

| 列名 | 说明 |
|------|------|
| ID | 产品ID |
| 封面图 | 缩略图展示 |
| 标题 | 产品标题 |
| 型号 | 产品型号 |
| 分类 | 所属分类名称 |
| 风格标签 | 标签名称，多个用标签展示 |
| 浏览量 | PV统计 |
| 状态 | 上架/下架，可切换 |
| 排序 | 排序权重 |
| 创建时间 | 格式：YYYY-MM-DD HH:mm:ss |
| 操作 | 编辑、删除、上下架 |

**功能**：
- 搜索：按标题/型号搜索
- 筛选：按分类筛选、按状态筛选
- 批量操作：批量上架/下架/删除
- 分页：每页20条

#### 5.4.2 添加/编辑产品页

**表单字段**：

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| 图纸标题 | 是 | 文本输入 | 最多200字符 |
| 图纸型号 | 是 | 文本输入 | 最多100字符，如"QGY-2026-001" |
| 所属分类 | 是 | 下拉选择 | 从分类表中选择 |
| 风格标签 | 否 | 多选标签 | 从标签表中选择，可多选 |
| 建筑面积 | 否 | 文本输入 | 如"180㎡" |
| 占地面积 | 否 | 文本输入 | 如"120㎡" |
| 户型 | 否 | 文本输入 | 如"4室2厅3卫" |
| 图纸简介 | 否 | 多行文本 | 最多500字符 |
| 主图轮播图 | 是 | 多图上传 | 至少上传1张，最多9张，支持拖拽排序 |
| 图纸详情图 | 是 | 多图上传 | 至少上传1张，最多20张，支持拖拽排序 |
| 排序权重 | 否 | 数字输入 | 值越大越靠前，默认0 |
| 是否上架 | 是 | 开关 | 默认上架 |

**图片上传说明**：
- 图片存储方式由管理后台"系统设置-存储配置"决定（本地存储 或 阿里云 OSS）
- 本地存储模式：图片上传到服务器本地目录，通过 Flask 静态文件服务访问
- OSS 存储模式：后端生成签名 URL，前端直传 OSS（或后端中转上传）
- 支持格式：JPG、PNG、WEBP、GIF
- 单张图片限制：不超过 5MB（可在存储配置中调整）
- 上传后自动生成缩略图
- 支持拖拽排序

### 5.5 分类管理

**表格列**：ID、分类名称、排序权重、状态、创建时间、操作（编辑/删除）

**功能**：
- 新增分类：输入分类名称 + 排序权重
- 编辑分类：修改分类名称 + 排序权重
- 删除分类：有关联产品时禁止删除，提示"该分类下有图纸产品，无法删除"
- 预置分类：一层、二层、三层、多层、双拼

### 5.6 风格标签管理

**表格列**：ID、标签名称、排序权重、状态、创建时间、操作（编辑/删除）

**功能**：
- 新增标签：输入标签名称 + 排序权重
- 编辑标签：修改标签名称 + 排序权重
- 删除标签：有关联产品时禁止删除
- 预置标签：新中式、欧式、现代、中式

### 5.7 Banner管理

**表格列**：ID、Banner图片（缩略图）、标题、跳转类型、排序权重、状态、操作（编辑/删除）

**功能**：
- 新增 Banner：上传图片 + 设置标题 + 配置跳转（无跳转/产品详情/分类/自定义URL）
- 编辑 Banner
- 删除 Banner
- 启用/禁用 Banner
- 支持设置展示时间段

### 5.8 咨询客户管理

**表格列**：

| 列名 | 说明 |
|------|------|
| ID | 客户ID |
| 姓名 | 客户姓名 |
| 手机号 | 客户手机号 |
| 微信号 | 客户微信号 |
| 所在省市 | 省份 + 城市 |
| 面积预算 | 建房面积预算 |
| 意向产品 | 关联的产品标题（可点击跳转） |
| 来源 | 来源渠道 |
| 跟进状态 | 新客户/已联系/跟进中/已成交，可切换 |
| 提交时间 | 格式：YYYY-MM-DD HH:mm:ss |
| 操作 | 查看详情、修改状态、添加备注 |

**功能**：
- 搜索：按姓名/手机号搜索
- 筛选：按跟进状态筛选、按日期范围筛选
- 客户详情弹窗：展示客户完整信息 + 跟进记录
- 修改跟进状态
- 添加备注
- 导出 Excel：导出筛选后的客户列表

### 5.9 系统设置

- **客服二维码设置**：上传客服微信二维码图片
- **存储配置管理**：切换本地存储/阿里云 OSS，配置存储参数（详见第十二章"存储系统设计"）
- **修改密码**：输入旧密码 + 新密码 + 确认新密码

#### 5.9.1 存储配置管理页

**页面布局**：

```
┌─────────────────────────────────────────┐
│  存储配置管理                              │
├─────────────────────────────────────────┤
│                                         │
│  当前存储方式：● 本地存储  ○ 阿里云 OSS    │  ← 单选切换
│                                         │
│  ┌─ 本地存储配置（选择本地时展示） ──────┐  │
│  │  基础访问URL：[http://...       ]    │  │
│  │  上传目录路径：[/app/uploads     ]    │  │
│  │  当前已用空间：125 MB / 10 GB        │  │
│  └─────────────────────────────────────┘  │
│                                         │
│  ┌─ 阿里云 OSS 配置（选择OSS时展示） ──┐  │
│  │  AccessKey ID：[LTAI5t...       ]   │  │
│  │  AccessKey Secret：[***********  ]   │  │  ← 密码框，脱敏显示
│  │  Bucket 名称：[qiaogongyishu   ]    │  │
│  │  Endpoint：[oss-cn-hangzhou... ]    │  │
│  │  CDN 加速域名：[https://cdn...  ]    │  │
│  │  自定义域名：[https://img...    ]    │  │  ← 可选
│  │  地域：[cn-hangzhou ▼]              │  │
│  │                                     │  │
│  │  [测试连接]                          │  │  ← 点击测试 OSS 连接
│  │  连接状态：✅ 连接成功                 │  │
│  └─────────────────────────────────────┘  │
│                                         │
│  ┌─ 通用配置 ─────────────────────────┐  │
│  │  最大文件大小：[5] MB               │  │
│  │  允许的文件类型：jpg,png,webp,gif   │  │
│  └─────────────────────────────────────┘  │
│                                         │
│           [保存配置]  [重置]              │
│                                         │
└─────────────────────────────────────────┘
```

**交互说明**：

1. **存储方式切换**
   - 单选按钮切换"本地存储"和"阿里云 OSS"
   - 切换后对应配置区域显示/隐藏（带动画过渡）
   - 切换存储方式时弹出确认弹窗："切换存储方式后，已上传的文件仍保留在原存储中。新上传的文件将使用新的存储方式。是否确认切换？"

2. **OSS 配置**
   - AccessKey Secret 使用密码输入框，默认脱敏显示
   - 点击密码框右侧"眼睛"图标可临时查看明文
   - "测试连接"按钮：点击后调用后端接口测试 OSS 连接，显示连接结果
   - 测试成功显示绿色 ✅，失败显示红色 ❌ + 错误信息

3. **保存配置**
   - 点击"保存配置"按钮 → 前端校验必填字段 → 调用后端接口
   - 保存成功后弹出提示："存储配置已更新"
   - 保存后自动刷新存储服务（后端重新加载配置，无需重启服务）

4. **安全提示**
   - 页面顶部显示提示信息："存储配置涉及敏感信息，请确保仅在可信网络环境下修改"

---

## 六、API 接口设计

### 6.1 接口规范

**基础URL**: `https://api.example.com/api/v1`

**统一响应格式**：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

**分页响应格式**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "per_page": 10,
    "pages": 10
  }
}
```

**HTTP 状态码规范**：

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（Token过期或无效） |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

### 6.2 小程序端 API

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /auth/wx-login | 微信登录（wx.login code换token） | 否 |
| GET | /banners | 获取Banner列表 | 否 |
| GET | /categories | 获取分类列表 | 否 |
| GET | /tags | 获取风格标签列表 | 否 |
| GET | /products | 获取产品列表（分页+筛选） | 否 |
| GET | /products/{id} | 获取产品详情 | 否 |
| POST | /products/{id}/view | 记录产品浏览 | 否 |
| GET | /search?keyword=xxx | 搜索产品 | 否 |
| POST | /customers | 提交客户表单 | 否 |
| GET | /settings/{key} | 获取系统设置 | 否 |

### 6.3 管理后台 API

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /admin/auth/login | 管理员登录 | 否 |
| POST | /admin/auth/logout | 管理员登出 | 是 |
| GET | /admin/dashboard | 仪表盘统计数据 | 是 |
| GET | /admin/products | 产品列表 | 是 |
| POST | /admin/products | 创建产品 | 是 |
| PUT | /admin/products/{id} | 更新产品 | 是 |
| DELETE | /admin/products/{id} | 删除产品 | 是 |
| PATCH | /admin/products/{id}/status | 切换产品上下架 | 是 |
| GET | /admin/categories | 分类列表 | 是 |
| POST | /admin/categories | 创建分类 | 是 |
| PUT | /admin/categories/{id} | 更新分类 | 是 |
| DELETE | /admin/categories/{id} | 删除分类 | 是 |
| GET | /admin/tags | 标签列表 | 是 |
| POST | /admin/tags | 创建标签 | 是 |
| PUT | /admin/tags/{id} | 更新标签 | 是 |
| DELETE | /admin/tags/{id} | 删除标签 | 是 |
| GET | /admin/banners | Banner列表 | 是 |
| POST | /admin/banners | 创建Banner | 是 |
| PUT | /admin/banners/{id} | 更新Banner | 是 |
| DELETE | /admin/banners/{id} | 删除Banner | 是 |
| GET | /admin/customers | 客户列表 | 是 |
| GET | /admin/customers/{id} | 客户详情 | 是 |
| PATCH | /admin/customers/{id}/status | 修改客户状态 | 是 |
| PATCH | /admin/customers/{id}/remark | 添加客户备注 | 是 |
| GET | /admin/customers/export | 导出客户Excel | 是 |
| POST | /admin/upload/image | 上传图片（获取OSS签名） | 是 |
| GET | /admin/settings | 获取系统设置 | 是 |
| PUT | /admin/settings | 更新系统设置 | 是 |
| PUT | /admin/auth/password | 修改密码 | 是 |
| GET | /admin/storage/config | 获取当前存储配置 | 是 |
| PUT | /admin/storage/config | 更新存储配置 | 是 |
| POST | /admin/storage/test | 测试存储连接（OSS） | 是 |

> **完整接口规范**：所有接口的详细定义（请求参数、响应格式、Schema）请参见 `docs/api-spec.yaml`（OpenAPI 3.0 格式），该文件是前后端开发的唯一依据。

---

## 七、非功能性需求

### 7.1 性能要求

- 小程序首屏加载时间 < 2秒
- API 接口响应时间 < 500ms（P99）
- 图片使用 WebP 格式，配合 OSS 图片处理自动生成缩略图
- 列表接口使用 Redis 缓存，缓存时间 5 分钟

### 7.2 安全要求

- 所有 API 接口使用 HTTPS
- 管理后台接口使用 JWT Token 认证，Token 有效期 24 小时
- 文件上传限制文件类型和大小
- 表单提交防重复（同一手机号 1 分钟内只能提交 1 次）
- SQL 注入防护（使用 ORM 参数化查询）
- XSS 防护（输入过滤 + 输出转义）
- 接口限流：小程序端单 IP 100次/分钟，管理后台单账号 200次/分钟

### 7.3 兼容性要求

- 微信基础库版本 >= 2.25.0
- 适配 iPhone SE ~ iPhone 15 Pro Max
- 适配主流 Android 机型

### 7.4 可维护性要求

- 后端代码遵循 PEP 8 编码规范
- API 接口有完整的 Swagger/OpenAPI 文档
- 关键业务逻辑有注释说明
- 数据库变更使用 Flask-Migrate 管理

---

## 八、开发阶段规划

### Phase 1：API 契约与基础框架（第1周）

- [ ] 编写 OpenAPI 3.0 接口规范文件 `docs/api-spec.yaml`（作为前后端开发唯一依据）
- [ ] 根据 API 契约生成 Flask 后端路由框架，所有接口先返回硬编码假数据
- [ ] 初始化项目结构（小程序 + Flask + 管理后台）
- [ ] 数据库设计与建表（MySQL 8.0）
- [ ] Flask 基础架构搭建（应用工厂、配置、扩展）
- [ ] 实现存储服务层（策略模式：抽象基类 + 本地存储实现 + OSS 存储实现 + 工厂）
- [ ] 统一响应格式、错误处理、JWT 认证
- [ ] 确保前端（小程序 + 管理后台）能调用所有假数据接口正常渲染

### Phase 2：管理后台开发（第2-3周）

- [ ] 管理后台登录页
- [ ] 分类管理 CRUD
- [ ] 风格标签管理 CRUD
- [ ] Banner 管理 CRUD
- [ ] 图纸产品管理 CRUD（含图片上传，对接存储服务层）
- [ ] 咨询客户列表与状态管理
- [ ] 仪表盘统计
- [ ] 系统设置（存储配置管理 + 客服二维码 + 修改密码）
- [ ] 存储配置功能：本地存储/OSS 切换、OSS 连接测试

### Phase 3：小程序端开发（第3-4周）

- [ ] 小程序项目初始化与全局配置
- [ ] 网络请求封装
- [ ] 首页（Banner + 分类导航 + 风格筛选 + 产品列表）
- [ ] 搜索功能
- [ ] 产品详情页
- [ ] 在线客服页
- [ ] 领取图纸表单页

### Phase 4：联调测试与上线（第5周）

- [ ] 后端接口从假数据切换到真实数据库查询
- [ ] 小程序与管理后台联调
- [ ] 功能测试与 Bug 修复
- [ ] 性能优化（Redis 缓存、图片压缩）
- [ ] 微信小程序审核提交
- [ ] 服务器部署上线

---

## 九、补充完善说明

相比原始需求，本文档做了以下补充和完善：

1. **搜索功能**：首页增加搜索框，支持按标题/型号搜索图纸产品，含搜索历史
2. **产品信息扩展**：产品增加建筑面积、占地面积、户型等参数字段，让客户快速了解图纸概况
3. **浏览量统计**：记录产品浏览次数，为后续运营分析提供数据
4. **Banner管理**：独立管理轮播图，支持配置跳转链接和展示时间段
5. **风格标签独立管理**：后台可自由增删改风格标签，不硬编码
6. **客户状态管理**：咨询客户支持跟进状态标记（新客户/已联系/跟进中/已成交），方便销售跟进
7. **客户导出**：支持导出客户列表为 Excel，方便线下使用
8. **仪表盘**：管理后台首页展示关键运营数据
9. **系统设置**：客服二维码可在后台配置更换，无需改代码
10. **安全防护**：防重复提交、接口限流、XSS/SQL注入防护
11. **缓存策略**：使用 Redis 缓存高频数据，提升性能
12. **图片优化**：OSS 图片处理自动生成缩略图，支持 WebP 格式
13. **分享功能**：小程序页面支持微信转发分享，利于客服传播
14. **意向产品关联**：客户表单记录来源产品，便于了解客户意向
15. **API 契约驱动开发**：使用 OpenAPI 3.0 规范文件（api-spec.yaml）作为前后端开发唯一依据，后端先返回假数据确保前端可调用
16. **存储系统策略模式**：抽象存储服务层，支持本地存储/阿里云 OSS 自主切换，管理后台可视化配置
17. **OSS 连接测试**：管理后台支持在线测试 OSS 连接，配置保存后自动刷新无需重启
18. **管理后台深色侧边栏**：左侧边栏深色主题（#1D1E2C），白色文字统一 14px，完整的 UI 样式规范
19. **JWT 认证完整设计**：包含认证流程图、Token 规范、前端拦截器代码、后端装饰器代码、安全措施
20. **Trae IDE 配置**：完整的插件清单、settings.json/tasks.json 配置、Vibe Coding 分阶段提示词模板和最佳实践

---

## 十、环境变量配置（.env）

```env
# Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production

# MySQL
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=menghuan123
MYSQL_DATABASE=qiaogongyishu

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# 阿里云 OSS（可选，管理后台配置优先级更高；首次部署或本地开发时可在此配置）
OSS_ACCESS_KEY_ID=your-access-key-id
OSS_ACCESS_KEY_SECRET=your-access-key-secret
OSS_BUCKET_NAME=your-bucket-name
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_CDN_DOMAIN=https://cdn.example.com

# 本地存储（默认存储方式，OSS未配置时使用）
LOCAL_UPLOAD_PATH=./uploads
LOCAL_BASE_URL=http://localhost:5000/uploads

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_EXPIRATION_HOURS=24

# 微信小程序
WX_APPID=your-wx-appid
WX_APP_SECRET=your-wx-app-secret

# 管理后台
ADMIN_DEFAULT_USERNAME=admin
ADMIN_DEFAULT_PASSWORD=admin123
```

---

## 十一、requirements.txt

```
Flask==3.1.*
Flask-SQLAlchemy==3.1.*
Flask-Migrate==4.1.*
Flask-CORS==5.0.*
Flask-Limiter==3.12.*
PyMySQL==1.1.*
redis==5.2.*
oss2==2.19.*
PyJWT==2.10.*
python-dotenv==1.1.*
openpyxl==3.1.*
marshmallow==3.23.*
gunicorn==23.0.*
connexion[swagger-ui]==3.*
```

---

## 十二、API 契约驱动开发规范

### 12.1 契约文件位置

```
项目根目录/
└── docs/
    └── api-spec.yaml    # OpenAPI 3.0 接口规范（前后端开发的唯一依据）
```

### 12.2 契约优先开发流程

本项目采用 **API 契约优先（Contract-First）** 开发模式，核心流程如下：

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  编写 api-    │ ──→ │  后端根据契约生成  │ ──→ │  前端根据契约     │
│  spec.yaml    │     │  路由框架+假数据  │     │  开发页面+Mock    │
└──────────────┘     └──────────────────┘     └──────────────────┘
                                                      │
                                                      ▼
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  联调测试     │ ←── │  后端替换为       │ ←── │  前端对接真实接口  │
│  & 部署上线    │     │  真实数据库逻辑   │     │                   │
└──────────────┘     └──────────────────┘     └──────────────────┘
```

### 12.3 后端基于契约生成路由框架

**实现方式**：使用 `connexion` 库，自动根据 `api-spec.yaml` 生成 Flask 路由。

**步骤**：

1. **安装依赖**：`pip install connexion[swagger-ui]`

2. **Flask 应用集成 connexion**：

```python
# backend/app/__init__.py
from connexion import FlaskApp
from connexion.options import SwaggerUIOptions

def create_app():
    connexion_app = FlaskApp(
        __name__,
        specification_dir='../docs/',   # api-spec.yaml 所在目录
        options={"swagger_ui": True}
    )
    
    # 根据 OpenAPI 规范自动注册路由
    connexion_app.add_api(
        'api-spec.yaml',
        base_path='/api/v1',
        strict_validation=True,
        validate_responses=True
    )
    
    flask_app = connexion_app.app
    return flask_app
```

3. **实现路由处理函数**：在 `backend/app/api/` 目录下，按照 `api-spec.yaml` 中定义的 `operationId` 创建对应的处理函数，先返回硬编码假数据：

```python
# backend/app/api/product.py
# operationId: getProducts → 函数名 get_products

def get_products(category_id=None, tag_id=None, page=1, per_page=10, keyword=None):
    """获取产品列表 - 假数据版本"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "items": [
                {
                    "id": 1,
                    "title": "新中式三层别墅",
                    "model_number": "QGY-2026-001",
                    "category_name": "三层",
                    "floor_area": "360㎡",
                    "cover_image": "https://via.placeholder.com/400x300",
                    "tags": [{"id": 1, "name": "新中式"}],
                    "view_count": 128
                }
            ],
            "total": 25,
            "page": 1,
            "per_page": 10,
            "pages": 3
        }
    }
```

4. **假数据覆盖所有接口**：确保每个接口都有对应的处理函数返回合理的假数据，前端可以正常调用和渲染。

5. **后续替换为真实逻辑**：Phase 4 阶段逐步将假数据替换为数据库查询。

### 12.4 契约变更规则

- `api-spec.yaml` 是前后端开发的**唯一依据**，任何接口变更必须先修改此文件
- 修改契约后需同步通知前端开发人员
- 使用 Git 版本控制追踪契约变更历史
- 破坏性变更（删除字段、修改类型）需在变更记录中标注

### 12.5 Swagger UI 在线文档

开发环境下，启动 Flask 后端后访问以下地址查看交互式 API 文档：

```
http://localhost:5000/api/v1/ui/
```

Swagger UI 支持在线测试所有接口，方便前端开发调试。

---

## 十三、存储系统设计（策略模式）

### 13.1 设计目标

- 图片和小文件存储支持**本地存储**和**阿里云 OSS**两种方式
- 通过管理后台界面**自主切换**，无需修改代码或重启服务
- 使用**策略模式（Strategy Pattern）** 实现存储服务的可插拔切换

### 13.2 架构设计

```
┌─────────────────────────────────────────────┐
│              UploadService                   │  ← 业务层调用
│         (上传/删除/获取URL)                   │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│           StorageFactory                     │  ← 工厂类
│     get_storage() → StorageBackend           │
│     (读取 storage_configs 表，创建实例)        │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌─────────────────┐ ┌─────────────────┐
│  LocalStorage   │ │   OSSStorage    │
│  (本地存储实现)  │ │ (阿里云OSS实现)  │
└─────────────────┘ └─────────────────┘
         ▲                   ▲
         │                   │
┌─────────────────────────────────────────────┐
│        StorageBackend (抽象基类)              │
│  + upload(file) → file_info                  │
│  + delete(file_key) → bool                   │
│  + get_url(file_key) → str                   │
│  + get_signed_url(file_key, expires) → str   │
│  + list_files(prefix) → list                 │
│  + test_connection() → bool                  │
└─────────────────────────────────────────────┘
```

### 13.3 存储抽象基类

```python
# backend/app/services/storage/base.py
from abc import ABC, abstractmethod
from typing import Optional
import io

class StorageBackend(ABC):
    """存储服务抽象基类"""
    
    @abstractmethod
    def upload(self, file_data: io.BytesIO, file_path: str, 
               content_type: str = None) -> dict:
        """
        上传文件
        :param file_data: 文件二进制数据
        :param file_path: 存储路径（如 products/2026/04/abc.jpg）
        :param content_type: 文件MIME类型
        :return: {"key": "xxx", "url": "https://...", "size": 1024}
        """
        pass
    
    @abstractmethod
    def delete(self, file_key: str) -> bool:
        """删除文件"""
        pass
    
    @abstractmethod
    def get_url(self, file_key: str) -> str:
        """获取文件访问URL"""
        pass
    
    @abstractmethod
    def get_signed_url(self, file_key: str, expires: int = 3600) -> str:
        """获取临时签名URL（用于私有文件）"""
        pass
    
    @abstractmethod
    def test_connection(self) -> tuple[bool, str]:
        """
        测试存储连接是否正常
        :return: (是否成功, 描述信息)
        """
        pass
```

### 13.4 本地存储实现

```python
# backend/app/services/storage/local.py
import os
import uuid
from datetime import datetime
from .base import StorageBackend

class LocalStorage(StorageBackend):
    """本地文件存储实现"""
    
    def __init__(self, config: dict):
        self.base_url = config.get('local_base_url', 'http://localhost:5000/uploads')
        self.upload_path = config.get('local_upload_path', '/app/uploads')
        os.makedirs(self.upload_path, exist_ok=True)
    
    def upload(self, file_data, file_path, content_type=None):
        full_path = os.path.join(self.upload_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(file_data.read())
        file_data.seek(0)
        return {
            "key": file_path,
            "url": f"{self.base_url}/{file_path}",
            "size": file_data.getbuffer().nbytes
        }
    
    def delete(self, file_key):
        full_path = os.path.join(self.upload_path, file_key)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    
    def get_url(self, file_key):
        return f"{self.base_url}/{file_key}"
    
    def get_signed_url(self, file_key, expires=3600):
        # 本地存储不需要签名，直接返回URL
        return self.get_url(file_key)
    
    def test_connection(self):
        test_path = f"_test/{uuid.uuid4().hex}.txt"
        try:
            full_path = os.path.join(self.upload_path, test_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write("connection test")
            os.remove(full_path)
            return True, "本地存储连接正常"
        except Exception as e:
            return False, f"本地存储异常: {str(e)}"
```

### 13.5 阿里云 OSS 存储实现

```python
# backend/app/services/storage/oss.py
import oss2
from .base import StorageBackend

class OSSStorage(StorageBackend):
    """阿里云 OSS 存储实现"""
    
    def __init__(self, config: dict):
        auth = oss2.Auth(
            config['oss_access_key_id'],
            config['oss_access_key_secret']
        )
        self.bucket = oss2.Bucket(
            auth,
            config['oss_endpoint'],
            config['oss_bucket_name']
        )
        self.cdn_domain = config.get('oss_cdn_domain', '')
        self.custom_domain = config.get('oss_custom_domain', '')
        self.endpoint = config['oss_endpoint']
        self.bucket_name = config['oss_bucket_name']
    
    def _get_base_url(self):
        """获取基础URL，优先CDN > 自定义域名 > 默认域名"""
        if self.cdn_domain:
            return self.cdn_domain.rstrip('/')
        if self.custom_domain:
            return self.custom_domain.rstrip('/')
        return f"https://{self.bucket_name}.{self.endpoint}"
    
    def upload(self, file_data, file_path, content_type=None):
        headers = {}
        if content_type:
            headers['Content-Type'] = content_type
        self.bucket.put_object(file_path, file_data, headers=headers)
        return {
            "key": file_path,
            "url": f"{self._get_base_url()}/{file_path}",
            "size": file_data.getbuffer().nbytes
        }
    
    def delete(self, file_key):
        self.bucket.delete_object(file_key)
        return True
    
    def get_url(self, file_key):
        return f"{self._get_base_url()}/{file_key}"
    
    def get_signed_url(self, file_key, expires=3600):
        return self.bucket.sign_url('GET', file_key, expires)
    
    def test_connection(self):
        try:
            self.bucket.get_bucket_info()
            return True, f"OSS连接正常 (Bucket: {self.bucket_name})"
        except oss2.exceptions.OssError as e:
            return False, f"OSS连接失败: {e.message}"
```

### 13.6 存储服务工厂

```python
# backend/app/services/storage/factory.py
from .base import StorageBackend
from .local import LocalStorage
from .oss import OSSStorage

# 模块级缓存，避免每次请求都重新创建
_storage_instance: StorageBackend = None
_storage_type: str = None

def get_storage(force_refresh=False) -> StorageBackend:
    """
    获取当前存储服务实例（单例模式）
    :param force_refresh: 是否强制刷新（存储配置变更后调用）
    """
    global _storage_instance, _storage_type
    
    from .. import cache_service
    
    if not force_refresh and _storage_instance is not None:
        return _storage_instance
    
    # 从数据库读取当前生效的存储配置
    config = cache_service.get_active_storage_config()
    
    if config['storage_type'] == 'oss':
        _storage_instance = OSSStorage(config)
    else:
        _storage_instance = LocalStorage(config)
    
    _storage_type = config['storage_type']
    return _storage_instance

def refresh_storage():
    """刷新存储服务（管理后台修改存储配置后调用）"""
    global _storage_instance, _storage_type
    _storage_instance = None
    _storage_type = None
    get_storage(force_refresh=True)
```

### 13.7 上传服务集成

```python
# backend/app/services/upload_service.py
import uuid
from datetime import datetime
from .storage.factory import get_storage

class UploadService:
    
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
    
    @staticmethod
    def upload_image(file) -> dict:
        """上传图片"""
        # 校验文件类型
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext not in UploadService.ALLOWED_EXTENSIONS:
            raise ValueError(f"不支持的文件类型: {ext}")
        
        # 生成存储路径: {module}/{date}/{uuid}.{ext}
        date_path = datetime.now().strftime("%Y/%m")
        file_key = f"images/{date_path}/{uuid.uuid4().hex}.{ext}"
        
        # 通过存储服务层上传（自动选择本地或OSS）
        storage = get_storage()
        result = storage.upload(file.stream, file_key, content_type=file.content_type)
        
        return result
    
    @staticmethod
    def delete_file(file_key: str) -> bool:
        """删除文件"""
        storage = get_storage()
        return storage.delete(file_key)
    
    @staticmethod
    def get_file_url(file_key: str) -> str:
        """获取文件访问URL"""
        storage = get_storage()
        return storage.get_url(file_key)
```

### 13.8 OSS 配置功能开发最佳路径

按照以下顺序逐步实现 OSS 配置功能：

```
步骤1: 数据库配置表设计
  └── 创建 storage_configs 表（已在第三章 3.2.10 定义）
  └── 编写 SQLAlchemy Model
  └── 编写数据库迁移脚本

步骤2: 抽象存储服务层（策略模式）
  └── 实现 StorageBackend 抽象基类
  └── 实现 LocalStorage 本地存储
  └── 实现 OSSStorage 阿里云OSS存储
  └── 实现 StorageFactory 工厂类

步骤3: OSS 存储实现
  └── 集成 oss2 SDK
  └── 实现上传/删除/获取URL/签名URL
  └── 实现连接测试功能

步骤4: 上传路由改造集成
  └── 改造 upload API，使用 UploadService 替代直接调用 OSS
  └── UploadService 内部通过 StorageFactory 获取存储实例
  └── 确保上传接口对存储方式透明

步骤5: 管理后台配置界面
  └── 存储配置页面（Vue组件）
  └── 获取/更新存储配置 API
  └── 测试连接 API
  └── 切换存储方式确认弹窗

步骤6: OSS 相关存储配置
  └── .env 中保留 OSS 配置作为默认值（首次部署用）
  └── 管理后台配置优先级高于 .env
  └── 配置变更后自动刷新存储服务实例
```

---

## 十四、Trae IDE 插件及 Vibe Coding 配置要求

### 14.1 Trae IDE 环境要求

| 项目 | 要求 |
|------|------|
| Trae IDE 版本 | 最新稳定版（建议 >= 2.0） |
| Python 插件 | Trae 内置 Python 扩展（语法高亮、IntelliSense、调试） |
| Vue 插件 | Vue - Official（Vue 3 语法支持 + Volar） |
| 微信小程序插件 | WXML / WXSS 语法高亮插件（Trae 扩展市场搜索 "miniprogram"） |
| 数据库工具 | Trae 内置数据库连接或安装 "Database Client" 扩展 |
| API 调试 | Thunder Client 或 REST Client 扩展（替代 Postman） |
| YAML 支持 | Trae 内置 YAML 扩展（用于编辑 api-spec.yaml） |
| Git | Trae 内置 Git 支持 |

### 14.2 Trae IDE 项目初始化配置

**步骤 1：创建项目工作区**

在 Trae IDE 中创建项目根目录 `qiaogongyishu/`，按第二章 2.3 节的目录结构创建所有子目录。

**步骤 2：配置 Python 解释器**

```
Trae IDE → 左下角 Python 版本 → 选择/创建虚拟环境
推荐：Python 3.12 虚拟环境（venv）
```

创建虚拟环境命令：
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

**步骤 3：配置 Trae settings.json**

在项目根目录创建 `.vscode/settings.json`：

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.analysis.extraPaths": ["${workspaceFolder}/backend"],
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.rulers": [88]
  },
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.associations": {
    "*.wxml": "wxml",
    "*.wxss": "css",
    "*.wxs": "javascript"
  },
  "emmet.includeLanguages": {
    "wxml": "html"
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/node_modules": true,
    "**/.venv": true,
    "**/venv": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/venv": true
  }
}
```

**步骤 4：配置 Trae 启动任务**

在项目根目录创建 `.vscode/tasks.json`：

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "启动 Flask 后端",
      "type": "shell",
      "command": "${workspaceFolder}/backend/venv/bin/python",
      "args": ["${workspaceFolder}/backend/run.py"],
      "cwd": "${workspaceFolder}/backend",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "启动管理后台前端",
      "type": "shell",
      "command": "npm",
      "args": ["run", "dev"],
      "cwd": "${workspaceFolder}/admin",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "dependsOn": []
    },
    {
      "label": "同时启动后端+管理后台",
      "dependsOn": ["启动 Flask 后端", "启动管理后台前端"],
      "group": "build",
      "problemMatcher": []
    },
    {
      "label": "数据库迁移",
      "type": "shell",
      "command": "${workspaceFolder}/backend/venv/bin/flask",
      "args": ["db", "upgrade"],
      "cwd": "${workspaceFolder}/backend",
      "problemMatcher": []
    }
  ]
}
```

### 14.3 Vibe Coding 开发规范

#### 14.3.1 对话上下文管理

在 Trae IDE 中使用 Vibe Coding 时，建议按以下方式管理对话上下文：

| 阶段 | 上下文输入 | 说明 |
|------|-----------|------|
| 项目初始化 | `docs/prd.md` + `docs/api-spec.yaml` | 将两个文档内容作为初始上下文粘贴到 Trae Chat |
| 后端开发 | `docs/api-spec.yaml` + 当前开发模块的 PRD 章节 | 聚焦当前模块，避免上下文过长 |
| 前端开发 | PRD 中对应页面设计 + `docs/api-spec.yaml` 中的接口定义 | 确保前端与接口契约一致 |
| Bug 修复 | 错误信息 + 相关代码文件 | 精准定位问题 |

#### 14.3.2 Vibe Coding 分阶段提示词模板

**Phase 1 - 后端路由框架（假数据）**：

```
请根据 docs/api-spec.yaml 中的 OpenAPI 规范，使用 connexion 库生成 Flask 后端路由框架。
要求：
1. 使用 connexion[swagger-ui] 自动注册路由
2. 所有接口先返回硬编码假数据，确保 Swagger UI 可测试
3. 统一响应格式：{"code": 200, "message": "success", "data": {}}
4. JWT 认证装饰器 @admin_required 应用到所有 /admin/ 路由
5. 项目结构参考 docs/prd.md 第二章 2.3 节
```

**Phase 2 - 管理后台前端**：

```
请根据 docs/prd.md 第五章管理后台设计，使用 Vue 3 + Element Plus 创建管理后台。
要求：
1. 左侧边栏深色主题（背景色 #1D1E2C，白色文字 14px）
2. JWT 登录认证（Token 存 localStorage，axios 拦截器自动附加）
3. 所有页面参考 PRD 中的 ASCII 线框图布局
4. API 请求地址对接后端 http://localhost:5000/api/v1
```

**Phase 3 - 小程序端**：

```
请根据 docs/prd.md 第四章小程序页面设计，创建微信小程序原生项目。
要求：
1. 无底部 TabBar
2. 首页：Banner 轮播 + 分类导航 + 风格筛选 + 双列产品列表
3. 产品详情页：主图轮播 + 参数栏 + 详情图 + 底部固定栏
4. 网络请求封装，API 地址 http://localhost:5000/api/v1
```

#### 14.3.3 Vibe Coding 最佳实践

1. **分模块开发**：每次对话只聚焦一个模块（如"产品管理CRUD"），避免上下文过长导致质量下降
2. **先骨架后细节**：先生成基础框架和假数据，确认可运行后再填充业务逻辑
3. **增量迭代**：每个模块完成后先测试验证，再进入下一个模块
4. **引用契约**：每次涉及接口变更时，提醒 AI 同步更新 `docs/api-spec.yaml`
5. **代码审查**：AI 生成代码后，人工检查关键逻辑（认证、权限、数据校验）
6. **错误处理**：遇到 AI 生成的错误代码时，将完整错误信息粘贴回对话，让 AI 自行修复

### 14.4 Trae IDE 数据库连接配置

在 Trae IDE 中配置 MySQL 数据库连接，方便直接查看和管理数据：

```json
// .vscode/settings.json 中添加（或使用 Database Client 扩展配置）
"databaseClient.connections": [
  {
    "name": "巧工艺墅开发库",
    "type": "mysql",
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "menghuan123",
    "database": "qiaogongyishu",
    "color": "#1A6D5C"
  }
]
```

### 14.5 Trae IDE 推荐扩展清单

| 扩展名称 | 用途 | 必装 |
|---------|------|------|
| Python | Python 语言支持 + 调试 | ✅ |
| Vue - Official | Vue 3 语法 + Volar | ✅ |
| Prettier | 代码格式化（JS/Vue/CSS/JSON/YAML） | ✅ |
| Black Formatter | Python 代码格式化 | ✅ |
| ESLint | JavaScript/Vue 代码检查 | ✅ |
| Thunder Client | API 接口调试（内置） | ✅ |
| WXML / WXSS | 微信小程序语法高亮 | ✅ |
| YAML | YAML 语法支持（编辑 api-spec.yaml） | ✅ |
| Database Client | 数据库可视化管理 | 推荐 |
| GitLens | Git 增强功能 | 推荐 |
| Error Lens | 行内显示错误信息 | 推荐 |
| Auto Rename Tag | HTML/Vue 标签自动重命名 | 推荐 |
