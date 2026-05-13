FROM postgres:17

# Some clients (and older JVMs) use the legacy zone name "Asia/Calcutta".
# Newer tzdata may not ship that alias, so PostgreSQL rejects the startup GUC:
#   FATAL: invalid value for parameter "TimeZone": "Asia/Calcutta"
# Creating a symlink makes the alias resolvable again.
RUN ln -sf /usr/share/zoneinfo/Asia/Kolkata /usr/share/zoneinfo/Asia/Calcutta
