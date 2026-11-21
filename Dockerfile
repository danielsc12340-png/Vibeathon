# Base general EIRA (modo central). Ver DESPLIEGUE_CENTRAL.md
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 EIRA_MODO=central EIRA_PROXY=1 EIRA_HTTPS=1 \
    EIRA_RESPALDOS=/datos/respaldos
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY eira ./eira
COPY run.py ./
RUN useradd --create-home --uid 10001 eira && mkdir -p /app/instance /datos/respaldos \
    && chown -R eira /app/instance /datos
USER eira
EXPOSE 8000
CMD ["python", "run.py", "--central", "--red", "--sin-navegador", "--puerto", "8000"]
