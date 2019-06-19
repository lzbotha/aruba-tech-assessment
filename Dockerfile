FROM python:3.7-slim as development

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 5000

ENV PYTHONPATH=/aplocation

ENV FLASK_APP='aplocation.route:app'
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0"]

FROM development as production

CMD ["gunicorn", "--bind=0.0.0.0:5000", "aplocation.route:app"]
