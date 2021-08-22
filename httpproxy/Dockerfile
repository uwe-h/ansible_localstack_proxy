FROM mitmproxy/mitmproxy
COPY httpproxy/redirect.py redirect.py
#COPY httpproxy/mitmproxy/httpproxy.pem .
COPY httpproxy/mitmproxy/* /home/mitmproxy/.mitmproxy/
#COPY localstackcerts/server.test.pem .
CMD ["mitmdump", "-s", "redirect.py","-k"]
