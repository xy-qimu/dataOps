FROM quay.io/astronomer/astro-runtime:11.6.0

USER root

# option: install odbc driver for sql server
COPY install_odbc.sh /tmp/install_odbc.sh
RUN chmod +x /tmp/install_odbc.sh
RUN apt-get update && apt-get install -y lsb-release
CMD ["/tmp/install_odbc.sh"]
