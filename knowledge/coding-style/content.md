# Coding Style Guide

---

name: coding-style
version: v1.0.0
type: convention
category: development
updated: 2026-07-19
---

# 1. 总则


## 1.1 核心原则


- **可读性优先** - 代码是写给人读的，其次才是给机器执行的

- **一致性** - 整个项目保持统一的风格
- **简洁性** - 避免不必要的复杂度
- **可维护性** - 考虑未来的维护成本

## 1.2 适用范围


本规范适用于所有项目代码，包括但不限于：


- JavaScript / TypeScript

- Python
- Java
- Go
- 其它语言

语言特定规范参见各语言扩展文档。


---


# 2. 命名规范


## 2.1 通用规则


### 规则


1. 使用描述性名称

2. 避免缩写（除非是公认的）
3. 避免单字母变量（除循环变量）
4. 名称应表达意图

### 示例


✅ 正确：


```javascript

const userCount = 10;
const isAuthenticated = true;
function calculateTotalPrice() { }
```

❌ 错误：


```javascript

const uc = 10;              // 过度缩写
const x = true;             // 无意义名称
function calc() { }         // 模糊不清
```

---


## 2.2 变量命名


### JavaScript / TypeScript


**规则：** 使用 camelCase


✅ 正确：


```javascript

const userName = 'John';
let itemCount = 0;
const isActive = true;
```

❌ 错误：


```javascript

const user_name = 'John';   // snake_case
const ItemCount = 0;        // PascalCase
```

---


### Python


**规则：** 使用 snake_case


✅ 正确：


```python

user_name = 'John'
item_count = 0
is_active = True
```

❌ 错误：


```python

userName = 'John'           # camelCase
ItemCount = 0               # PascalCase
```

---


## 2.3 函数命名


### 规则


1. 使用动词开头

2. 表达函数的行为
3. 布尔返回值使用 is/has/should 前缀

### 示例


✅ 正确：


```javascript

function getUserById(id) { }
function calculateTotal() { }
function isValid() { }
function hasPermission() { }
```

❌ 错误：


```javascript

function user(id) { }       // 不是动词
function total() { }        // 不清晰
function valid() { }        // 应该是 isValid
```

---


## 2.4 类命名


### 规则


使用 PascalCase（所有语言通用）


✅ 正确：


```javascript

class UserService { }
class OrderManager { }
class PaymentProcessor { }
```

❌ 错误：


```javascript

class userService { }       // camelCase
class order_manager { }     // snake_case
```

---


## 2.5 常量命名


### 规则


使用 UPPER_SNAKE_CASE


✅ 正确：


```javascript

const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';
const DEFAULT_TIMEOUT = 5000;
```

❌ 错误：


```javascript

const maxRetryCount = 3;    // camelCase
const ApiBaseUrl = '...';   // PascalCase
```

---


# 3. 格式规范


## 3.1 缩进


### 规则


- 使用 2 空格或 4 空格（项目统一）

- 禁止使用 Tab

### 示例


✅ 正确（2 空格）：


```javascript

function example() {
  if (condition) {
    doSomething();
  }
}
```

❌ 错误：


```javascript

function example() {
    if (condition) {        // 混用空格数
        doSomething();
    }
}
```

---


## 3.2 行长度


### 规则


- 每行不超过 100 字符

- 超长行应适当换行

### 示例


✅ 正确：


```javascript

const result = calculateSomething(
  param1,
  param2,
  param3
);
```

❌ 错误：


```javascript

const result = calculateSomething(param1, param2, param3, param4, param5, param6);
```

---


## 3.3 空行


### 规则


1. 函数之间空一行

2. 逻辑块之间空一行
3. 文件末尾保留一个空行
4. 不要连续多个空行

### 示例


✅ 正确：


```javascript

function functionA() {
  // code
}

function functionB() {

  // code
}
```

❌ 错误：


```javascript

function functionA() {
  // code
}
function functionB() {      // 缺少空行
  // code
}
```

---


## 3.4 大括号


### 规则


- 左大括号不换行（K&R 风格）

- 右大括号独占一行

✅ 正确：


```javascript

if (condition) {
  doSomething();
}
```

❌ 错误：


```javascript

if (condition)
{                           // 左大括号换行
  doSomething();
}
```

---


# 4. 注释规范


## 4.1 注释原则


1. 注释说明"为什么"，而非"是什么"

2. 代码应该自解释，减少注释
3. 注释应保持更新

---


## 4.2 单行注释


### JavaScript / TypeScript


```javascript

// 获取用户信息
const user = getUser();

// TODO: 优化性能

// FIXME: 修复边界情况
// NOTE: 这里有特殊处理
```

---


## 4.3 多行注释


### JavaScript / TypeScript


```javascript

/**
 * 计算订单总价
 * 
 * @param {Array} items - 订单项列表
 * @param {number} discount - 折扣率
 * @returns {number} 总价
 */
function calculateTotal(items, discount) {
  // implementation
}
```

---


## 4.4 文件注释


```javascript

/**
 * User Service
 * 
 * 处理用户相关业务逻辑
 * 
 * @author John Doe
 * @since 2026-07-19
 */
```

---


# 5. 最佳实践


## 5.1 函数


### 规则


1. 函数应该短小

2. 函数只做一件事
3. 函数参数不超过 3 个
4. 避免副作用

### 示例


✅ 正确：


```javascript

function calculateTax(amount) {
  return amount * 0.1;
}

function applyTax(amount) {

  const tax = calculateTax(amount);
  return amount + tax;
}
```

❌ 错误：


```javascript

function processOrder(order, user, payment, shipping, discount, coupon) {
  // 参数过多
  // 做了太多事情
}
```

---


## 5.2 变量


### 规则


1. 使用 const 优先于 let

2. 避免使用 var
3. 变量声明靠近使用处
4. 一次声明一个变量

### 示例


✅ 正确：


```javascript

const user = getUser();
const name = user.name;

let count = 0;

count += 1;
```

❌ 错误：


```javascript

var user = getUser();       // 使用 var
let name, age, email;       // 一次声明多个
```

---


## 5.3 条件语句


### 规则


1. 避免深层嵌套

2. 使用提前返回
3. 复杂条件提取为变量

### 示例


✅ 正确：


```javascript

function processUser(user) {
  if (!user) return;
  if (!user.isActive) return;
  
  // 处理逻辑
}
```

❌ 错误：


```javascript

function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.email) {
        // 深层嵌套
      }
    }
  }
}
```

---


# 6. 反模式


## 6.1 魔法数字


❌ 错误：


```javascript

if (status === 1) {         // 1 是什么？
  // code
}
```

✅ 正确：


```javascript

const STATUS_ACTIVE = 1;

if (status === STATUS_ACTIVE) {

  // code
}
```

---


## 6.2 过长函数


❌ 错误：


```javascript

function processOrder() {
  // 200 行代码
}
```

✅ 正确：


```javascript

function processOrder() {
  validateOrder();
  calculateTotal();
  applyDiscount();
  createInvoice();
}
```

---


## 6.3 过度注释


❌ 错误：


```javascript

// 声明变量 i
let i = 0;

// i 加 1

i = i + 1;
```

✅ 正确：


```javascript

let itemCount = 0;
itemCount += 1;
```

---


# 7. 工具


## 7.1 推荐工具


- **ESLint** - JavaScript/TypeScript 代码检查

- **Prettier** - 代码格式化
- **Black** - Python 代码格式化
- **gofmt** - Go 代码格式化

---


## 7.2 配置示例


### .eslintrc.json


```json

{
  "extends": "eslint:recommended",
  "rules": {
    "indent": ["error", 2],
    "max-len": ["error", 100],
    "no-var": "error"
  }
}
```

---


# 8. 语言特定扩展


本规范定义通用规则。各语言特定规则参见：


- `coding-style-javascript.md`

- `coding-style-python.md`
- `coding-style-java.md`
- `coding-style-go.md`

---


# 9. 检查清单


编写代码后检查：


- [ ] 命名符合规范

- [ ] 格式正确（缩进、空行、行长度）
- [ ] 注释适当
- [ ] 函数短小
- [ ] 无魔法数字
- [ ] 无过度嵌套
- [ ] 通过 Linter 检查

---


# 10. 例外情况


以下情况可例外：


1. 性能关键代码（需注释说明）

2. 与外部系统集成（遵循外部约定）
3. 临时调试代码（应在提交前移除）

例外需在 Code Review 中说明理由。


---
