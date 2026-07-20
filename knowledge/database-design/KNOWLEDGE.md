# Database Design Guidelines

数据库设计的最佳实践和规范。


---


## 基本原则


### 1. 命名规范


#### 表名


✅ **正确：**

- 使用复数形式：`users`, `orders`, `products`
- 小写字母加下划线：`user_profiles`, `order_items`
- 清晰描述实体：`shopping_carts`, `product_categories`

❌ **错误：**

- 单数形式：`user`, `order`
- 驼峰命名：`userProfiles`, `orderItems`
- 缩写：`usr`, `ord`

---


#### 列名


✅ **正确：**

- 小写字母加下划线：`first_name`, `created_at`
- 清晰描述：`email_verified`, `last_login_at`
- Boolean 使用 is_ 前缀：`is_active`, `is_deleted`

❌ **错误：**

- 驼峰命名：`firstName`, `createdAt`
- 缩写：`fn`, `ln`
- 模糊命名：`flag`, `status`

---


#### 主键


✅ **推荐：**

- UUID：`id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- 自增整数：`id SERIAL PRIMARY KEY`

**命名：** 统一使用 `id`


---


#### 外键


✅ **正确：**

- 使用 `{表名单数}_id`：`user_id`, `order_id`, `product_id`

❌ **错误：**

- 不一致的命名：`userId`, `order`, `prod_id`

---


### 2. 数据类型选择


#### 文本类型


```sql

-- 固定长度（少用）
CHAR(10)

-- 可变长度

VARCHAR(255)      -- 短文本（邮箱、用户名）
TEXT              -- 长文本（描述、评论）

-- PostgreSQL 特有

JSONB             -- JSON 数据
```

---


#### 数值类型


```sql

-- 整数
SMALLINT          -- -32,768 to 32,767
INTEGER           -- -2,147,483,648 to 2,147,483,647
BIGINT            -- 大整数

-- 小数

DECIMAL(10, 2)    -- 精确小数（金额）
NUMERIC(10, 2)    -- 同上
FLOAT             -- 浮点数（少用，不精确）
```

**金额字段：** 必须使用 DECIMAL 或 NUMERIC


---


#### 日期时间


```sql

DATE              -- 日期：2026-07-19
TIME              -- 时间：10:30:00
TIMESTAMP         -- 日期时间：2026-07-19 10:30:00
TIMESTAMPTZ       -- 带时区（推荐）
```

**推荐：** 使用 TIMESTAMPTZ 存储所有时间


---


#### Boolean


```sql

BOOLEAN           -- true/false
```

**命名：** 使用 `is_`, `has_`, `can_` 前缀


---


### 3. 约束


#### 主键约束


```sql

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- 或
  id SERIAL PRIMARY KEY
);
```

---


#### 唯一约束


```sql

CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL
);
```

---


#### 外键约束


```sql

CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**ON DELETE 选项：**

- `CASCADE` - 级联删除
- `SET NULL` - 设置为 NULL
- `RESTRICT` - 阻止删除（默认）
- `NO ACTION` - 同 RESTRICT

---


#### 检查约束


```sql

CREATE TABLE products (
  id UUID PRIMARY KEY,
  price DECIMAL(10, 2) CHECK (price >= 0),
  stock INTEGER CHECK (stock >= 0),
  status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'deleted'))
);
```

---


#### NOT NULL 约束


```sql

CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  username VARCHAR(50) NOT NULL,
  bio TEXT  -- 可以为 NULL
);
```

---


### 4. 索引


#### 单列索引


```sql

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_created_at ON orders(created_at);
```

---


#### 复合索引


```sql

-- 查询条件：WHERE user_id = ? AND status = ?
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 顺序很重要！

-- 可以使用：user_id
-- 可以使用：user_id + status
-- 不能使用：status（单独）
```

---


#### 唯一索引


```sql

CREATE UNIQUE INDEX idx_users_email ON users(email);
```

---


#### 部分索引


```sql

-- 只索引活跃用户
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- 只索引未删除的订单

CREATE INDEX idx_valid_orders ON orders(user_id) WHERE deleted_at IS NULL;
```

---


#### 何时添加索引


✅ **应该添加：**

- 外键列
- 频繁 WHERE 条件的列
- 频繁 ORDER BY 的列
- 频繁 JOIN 的列

❌ **不应该添加：**

- 很少查询的列
- 大量写入的表（索引影响写入性能）
- 低基数列（如 Boolean）

---


## 表设计模式


### 用户表


```sql

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  avatar_url TEXT,
  bio TEXT,
  role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin')),
  is_active BOOLEAN DEFAULT true,
  email_verified BOOLEAN DEFAULT false,
  last_login_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_created_at ON users(created_at);
```

---


### 时间戳字段


每个表都应该有：


```sql

created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
```

**自动更新 updated_at：**


```sql

-- PostgreSQL 触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 

  BEFORE UPDATE ON users 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();
```

---


### 软删除


```sql

CREATE TABLE products (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  -- ... 其他字段
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 查询时过滤已删除

SELECT * FROM products WHERE deleted_at IS NULL;

-- 创建索引优化

CREATE INDEX idx_products_not_deleted ON products(id) WHERE deleted_at IS NULL;
```

---


### 审计字段


```sql

CREATE TABLE orders (
  id UUID PRIMARY KEY,
  -- ... 业务字段
  created_by UUID REFERENCES users(id),
  updated_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

---


## 关系设计


### 一对多


```sql

-- 用户和订单：一个用户有多个订单
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(50) NOT NULL
);

CREATE TABLE orders (

  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  total DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_orders_user_id ON orders(user_id);

```

---


### 多对多


```sql

-- 用户和角色：用户可以有多个角色，角色可以分配给多个用户
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(50) NOT NULL
);

CREATE TABLE roles (

  id UUID PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

-- 关联表

CREATE TABLE user_roles (
  user_id UUID NOT NULL,
  role_id UUID NOT NULL,
  assigned_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);

CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
```

---


### 自引用关系


```sql

-- 评论的回复
CREATE TABLE comments (
  id UUID PRIMARY KEY,
  content TEXT NOT NULL,
  parent_id UUID,  -- NULL 表示顶级评论
  user_id UUID NOT NULL,
  FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_comments_parent_id ON comments(parent_id);

```

---


## 性能优化


### 1. 避免 N+1 查询


❌ **错误（N+1）：**

```javascript
// 获取所有订单
const orders = await db.query('SELECT * FROM orders');

// 对每个订单查询用户（N 次查询）

for (const order of orders) {
  const user = await db.query('SELECT * FROM users WHERE id = $1', [order.user_id]);
  order.user = user;
}
```

✅ **正确（JOIN）：**

```sql
SELECT 
  orders.*,
  users.username,
  users.email
FROM orders
JOIN users ON orders.user_id = users.id;
```

---


### 2. 使用 EXPLAIN 分析查询


```sql

EXPLAIN ANALYZE
SELECT * FROM orders 
WHERE user_id = 'xxx' 
  AND status = 'pending'
ORDER BY created_at DESC
LIMIT 20;
```

---


### 3. 分页优化


❌ **错误（OFFSET 性能差）：**

```sql
SELECT * FROM orders 
ORDER BY created_at DESC
LIMIT 20 OFFSET 10000;  -- 慢！
```

✅ **正确（基于游标）：**

```sql
SELECT * FROM orders 
WHERE created_at < '2026-07-19 10:00:00'
ORDER BY created_at DESC
LIMIT 20;
```

---


### 4. 批量操作


❌ **错误（逐条插入）：**

```sql
INSERT INTO users (email) VALUES ('user1@example.com');
INSERT INTO users (email) VALUES ('user2@example.com');
-- ...
```

✅ **正确（批量插入）：**

```sql
INSERT INTO users (email) VALUES 
  ('user1@example.com'),
  ('user2@example.com'),
  ('user3@example.com');
```

---


## 数据完整性


### 1. 使用事务


```sql

BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 'user1';

UPDATE accounts SET balance = balance + 100 WHERE id = 'user2';

COMMIT;

```

---


### 2. 并发控制


**乐观锁（版本号）：**

```sql
CREATE TABLE products (
  id UUID PRIMARY KEY,
  name VARCHAR(255),
  stock INTEGER,
  version INTEGER DEFAULT 0
);

-- 更新时检查版本

UPDATE products 
SET stock = stock - 1, version = version + 1
WHERE id = 'xxx' AND version = 5;
```

**悲观锁（行锁）：**

```sql
BEGIN;
SELECT * FROM products WHERE id = 'xxx' FOR UPDATE;
UPDATE products SET stock = stock - 1 WHERE id = 'xxx';
COMMIT;
```

---


## 反模式


### ❌ 使用 VARCHAR 存储日期


```sql

-- 错误
CREATE TABLE events (
  event_date VARCHAR(10)  -- '2026-07-19'
);

-- 正确

CREATE TABLE events (
  event_date DATE
);
```

---


### ❌ 使用 FLOAT 存储金额


```sql

-- 错误（精度问题）
CREATE TABLE orders (
  total FLOAT
);

-- 正确

CREATE TABLE orders (
  total DECIMAL(10, 2)
);
```

---


### ❌ 过度范式化


有时候适当的冗余可以提高性能：


```sql

-- 冗余 total_amount，避免每次都计算
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  total_amount DECIMAL(10, 2)  -- 订单项总和
);

CREATE TABLE order_items (

  id UUID PRIMARY KEY,
  order_id UUID,
  amount DECIMAL(10, 2)
);
```

---


## 安全


### 1. 最小权限原则


```sql

-- 应用账号只有必要的权限
GRANT SELECT, INSERT, UPDATE ON users TO app_user;
-- 不要 GRANT ALL
```

---


### 2. 防止 SQL 注入


✅ **使用参数化查询：**

```javascript
// 正确
db.query('SELECT * FROM users WHERE email = $1', [email]);

// 错误

db.query(`SELECT * FROM users WHERE email = '${email}'`);
```

---


### 3. 加密敏感数据


```sql

-- 存储加密后的密码
CREATE TABLE users (
  password_hash VARCHAR(255) NOT NULL  -- bcrypt hash
);

-- 敏感信息加密存储

CREATE TABLE user_secrets (
  encrypted_data TEXT  -- 加密后的数据
);
```

---


## 迁移管理


### 使用迁移工具


- Flyway

- Liquibase
- Knex.js migrations
- Sequelize migrations

**迁移文件命名：**

```
001_create_users_table.sql
002_add_email_to_users.sql
003_create_orders_table.sql
```

---


### 向后兼容


```sql

-- 添加列（设置默认值）
ALTER TABLE users ADD COLUMN phone VARCHAR(20) DEFAULT '';

-- 删除列（先废弃，再删除）

-- Step 1: 停止使用
-- Step 2: 下个版本删除
ALTER TABLE users DROP COLUMN old_field;
```

---


## 工具推荐


- **设计工具：** dbdiagram.io, draw.io

- **管理工具：** pgAdmin, DBeaver, TablePlus
- **性能分析：** pg_stat_statements
- **迁移工具：** Flyway, Knex.js

---


## 参考资源


- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

- [Database Design Best Practices](https://www.guru99.com/database-design.html)
- [SQL Style Guide](https://www.sqlstyle.guide/)

---


## 版本历史


- **v1.0.0** - 2026-07-19 - 初始版本


---
