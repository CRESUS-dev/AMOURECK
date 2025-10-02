cat > /home/cresus/projects/AMOURECK/audit_amoureck.sh <<'EOF'
#!/usr/bin/env bash
set -e

BASE="/home/cresus/projects/AMOURECK"
VENV="$BASE/venv"
PY="$VENV/bin/python"
GUNICORN="$VENV/bin/gunicorn"

echo "=== AUDIT AMOURECK ==="
echo "Project dir: $BASE"
echo "Python in venv: $PY"
echo

# 1. existence files
echo "1) FICHIERS PRINCIPAUX"
for f in "$BASE/manage.py" "$BASE/AMOURECK/settings.py" "$BASE/AMOURECK/wsgi.py" "$BASE/requirements.txt"; do
  if [ -f "$f" ]; then echo " OK: $f"; else echo " MISSING: $f"; fi
done
echo

# 2. venv / pip packages
echo "2) VIRTUALENV & DEPENDANCES"
if [ -x "$PY" ]; then
  echo " venv python: $($PY --version 2>&1)"
  echo " pip freeze (top 40):"
  $VENV/bin/pip freeze | sed -n '1,40p'
else
  echo " venv python absent ou non-exécutable: $PY"
fi
echo

# 3) settings checks
echo "3) CHECK settings.py"
if [ -f "$BASE/AMOURECK/settings.py" ]; then
  GREP_HOSTS=$(sed -n '1,400p' "$BASE/AMOURECK/settings.py" | grep -n "ALLOWED_HOSTS" -n || true)
  echo " ALLOWED_HOSTS lines:"
  sed -n '1,400p' "$BASE/AMOURECK/settings.py" | nl -ba | sed -n '1,200p' | sed -n '1,200p' | sed -n '/ALLOWED_HOSTS/,+3p' || true
  echo
  echo " DEBUG value:"
  sed -n '1,200p' "$BASE/AMOURECK/settings.py" | nl -ba | sed -n '/DEBUG/,+1p' || true
else
  echo " settings.py missing"
fi
echo

# 4) wsgi sanity
echo "4) WSIG / IMPORT TEST"
if [ -f "$BASE/AMOURECK/wsgi.py" ]; then
  sed -n '1,200p' "$BASE/AMOURECK/AMOURECK/wsgi.py" 2>/dev/null || sed -n '1,200p' "$BASE/AMOURECK/wsgi.py"
fi
echo

# 5) manage.py check and migrate dry-run
echo "5) DJANGO CHECK & MIGRATE (using venv python)"
if [ -x "$PY" ]; then
  echo "-> python manage.py check (no DB write)"
  (cd "$BASE" && $PY manage.py check) || echo " manage.py check failed"
  echo
  echo "-> python manage.py showmigrations --plan | tail -n 20"
  (cd "$BASE" && $PY manage.py showmigrations --plan | tail -n 20) || echo " showmigrations failed"
else
  echo " skip checks because venv not present"
fi
echo

# 6) Gunicorn test launch (no bind, import test)
echo "6) GUNICORN IMPORT TEST (no socket bind) — will try to import wsgi"
if [ -x "$GUNICORN" ]; then
  (cd "$BASE" && $GUNICORN --check-config AMOURECK.wsgi:application 2>&1) || true
  echo
  echo " Trying: $GUNICORN AMOURECK.wsgi:application --workers 1 --log-level debug --timeout 10 --bind 127.0.0.1:8001 (10s timeout)"
  (cd "$BASE" && timeout 12 $GUNICORN AMOURECK.wsgi:application --workers 1 --log-level error --timeout 10 --bind 127.0.0.1:8001 &) || true
  sleep 2
  ss -ltnp | grep 8001 || true
else
  echo " gunicorn not found in venv: $GUNICORN"
fi
echo

# 7) Check systemd gunicorn unit file existence
echo "7) systemd unit gunicorn"
if [ -f /etc/systemd/system/gunicorn.service ]; then
  echo " /etc/systemd/system/gunicorn.service EXISTS"
  sudo sed -n '1,200p' /etc/systemd/system/gunicorn.service
else
  echo " /etc/systemd/system/gunicorn.service not found"
fi
echo

# 8) Nginx test config
echo "8) NGINX config test"
if [ -f /etc/nginx/sites-available/amoureck ]; then
  echo " /etc/nginx/sites-available/amoureck:"
  sudo sed -n '1,200p' /etc/nginx/sites-available/amoureck
else
  echo " /etc/nginx/sites-available/amoureck missing"
fi
echo " nginx -t result:"
sudo nginx -t || true
echo

# 9) logs summary
echo "9) LOGS SUMMARY (last 80 lines each)"
echo " journalctl -u gunicorn --no-pager -n 80"
sudo journalctl -u gunicorn --no-pager -n 80 || true
echo
echo " tail /var/log/nginx/error.log -n 60"
sudo tail -n 60 /var/log/nginx/error.log || true
echo

echo "=== FIN AUDIT ==="
EOF

chmod +x /home/cresus/projects/AMOURECK/audit_amoureck.sh
echo "Script created: /home/cresus/projects/AMOURECK/audit_amoureck.sh"
echo "Lancer maintenant: cd /home/cresus/projects/AMOURECK && ./audit_amoureck.sh"
