# Pixel Kitten Pomodoro en GNOME

GNOME (Mutter) no tiene motor de reglas de ventana, así que no hay nada que configurar:

1. Corre `./install.sh` (instala bin + `.desktop`).
2. Busca "Pixel Kitten Pomodoro" en Actividades y ejecútalo.
3. El `always-on-top` lo pone la propia app (Qt `WindowStaysOnTopHint`
   → `_NET_WM_STATE_ABOVE`), sin extensiones.
4. Arrástrala donde quieras; la posición es manual.
5. Opcional: añádela a *Startup Applications* copiando el `.desktop` a
   `~/.config/autostart/`.

Estado: ejemplo **no probado** en GNOME puro. Si algo no cuadra (foco,
posición), abre un issue con tu versión de GNOME.
