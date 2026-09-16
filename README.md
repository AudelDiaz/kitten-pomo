# Pixel Kitten Pomodoro 🐈‍⬛

Una gatita negra pixel-art que vive flotando en tu escritorio y te acompaña en
tus pomodoros. Cozy, no estricta: te invita al break, no te bloquea.

## Controles

| Acción              | Efecto                          |
|---------------------|---------------------------------|
| Click izquierdo     | Iniciar pomodoro 25:00          |
| Doble click         | Pausar / reanudar               |
| Click derecho       | Reset (rompe la racha)          |
| Rueda (2x en 3s)    | Cerrar (con confirmación)       |
| `Shift+Click` o `T` | Simular fin (2s, para probar)   |
| Arrastrar           | Mover                            |

Al completar: sonido cozy + shake de 5s + break de 5:00 dentro de la burbuja.
**4 pomodoros seguidos en 150 min → break largo de 20:00.**

## Instalación

Requiere Python 3 + PySide6 (`pip install PySide6`).

```bash
./install.sh
# o: make install
```

Instala en `~/.local/share/kitten-pomo`, symlink en `~/.local/bin/kitten-pomo`
y launcher `.desktop`. Tu `pomodoro.jsonl` existente se conserva siempre.
Ver `docs/paths.md`.

```bash
./uninstall.sh            # conserva el historial
./uninstall.sh --purge-data  # borra todo incluido el historial
```

## Ventana por entorno

| Niri | Hyprland | GNOME |
|------|----------|-------|
| ✅ probado | 🧪 contrib | 🧪 contrib |

Ver `docs/compositors.md` y `packaging/`.

## Historial

Cada ciclo se guarda en `pomodoro.jsonl` (`ts/type/duration/completed`).
Ejemplo en `examples/pomodoro.sample.jsonl`.

```bash
python3 brain.py --stats   # racha actual y próximo break
```

Comparte el log con tu agente/Harness para analizar picos de foco y rachas.

## Licencia

MIT — ver `LICENSE`.
