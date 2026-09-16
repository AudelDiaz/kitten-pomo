# Rutas de instalación

`install.sh` respeta `XDG_DATA_HOME` (por defecto `~/.local`):

| Qué            | Ruta                                             |
|----------------|--------------------------------------------------|
| Código         | `~/.local/share/kitten-pomo/{kitten-pomo.py,brain.py}` |
| Assets         | `~/.local/share/kitten-pomo/{svg,sprites,sounds}/` |
| Historial      | `~/.local/share/kitten-pomo/pomodoro.jsonl` (el instalador **nunca** lo toca) |
| Binario        | `~/.local/bin/kitten-pomo` (symlink)             |
| Launcher       | `~/.local/share/applications/kitten-pomo.desktop` |

El `.desktop` se genera desde `packaging/kitten-pomo.desktop.in`
sustituyendo `@HOME@` por tu `$HOME`, así el repo no tiene rutas absolutas.
