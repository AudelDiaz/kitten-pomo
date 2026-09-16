# Ventana por entorno

El `always-on-top` lo pone la app (Qt `WindowStaysOnTopHint`). Las reglas de
abajo solo afinan tamaño, posición y opacidad.

| Entorno  | Estado      | Archivo                          |
|----------|-------------|----------------------------------|
| Niri     | ✅ probado  | `packaging/niri/kitten-pomo.kdl` |
| Hyprland | 🧪 contrib  | `packaging/hyprland/kitten-pomo.conf` |
| GNOME    | 🧪 contrib  | `packaging/gnome/README.md` (sin reglas) |

## Niri

Pega `packaging/niri/kitten-pomo.kdl` en tu archivo de reglas y recarga Niri.
Ventana 200x200 abajo-derecha, sin foco inicial, opacidad 0.8.

## Hyprland

Añade `source = ~/ruta/a/kitten-pomo/packaging/hyprland/kitten-pomo.conf`
a tu `hyprland.conf`. Ejemplo no probado por el autor; PRs con screenshot
bienvenidos.

## GNOME

Sin reglas: ejecuta el launcher, arrastra la ventana donde quieras.
Ver `packaging/gnome/README.md` para autostart.
