FROM python:3.10

# 设置容器内的工作目录
WORKDIR /root/backend

# 复制依赖清单
COPY requirements.txt .

# 安装 Python 依赖（建议加上清华源加速）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制后端代码和目录
COPY app/ ./app/

# 暴露后端端口
EXPOSE 8000

# 启动 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
