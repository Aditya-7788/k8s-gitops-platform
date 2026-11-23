FROM scratch AS static
COPY nginx.conf /nginx.conf
COPY index.html /index.html

FROM nginxinc/nginx-unprivileged:1.27-alpine AS runtime
COPY --from=static /nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=static /index.html /usr/share/nginx/html/index.html
EXPOSE 8080
STOPSIGNAL SIGTERM
