FROM python:3.12.2
# EXPOSE 5000
ENV DOCKED Yes
RUN pip install flask
RUN pip install requests
RUN pip install flask_mysqldb
RUN mkdir app
WORKDIR /app/
RUN mkdir templates
RUN mkdir static
COPY server.py /app
COPY functions.py /app
COPY db_operations.py /app
COPY db_config.py /app
COPY db_classes.py /app
COPY templates/  /app/templates/
COPY static/  /app/static/
RUN chmod -R 755 /app/static
RUN chmod -R 755 /app/templates
CMD python server.py