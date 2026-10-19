-- 1. 创建数据库（统一命名为 fastapi_two_day）
CREATE DATABASE IF NOT EXISTS admin_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 切换到该数据库
USE admin_db;

-- 3. 创建 memo 表（字段严格对应你代码里的定义）
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    sort VARCHAR(50) NOT NULL,
    star VARCHAR(100) NOT NULL,
    start_time VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;