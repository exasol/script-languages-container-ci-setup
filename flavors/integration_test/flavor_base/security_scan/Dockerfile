FROM {{release}}

RUN echo "Building security scan..."

COPY security_scan/test.sh /test.sh
ENTRYPOINT ["/test.sh"]