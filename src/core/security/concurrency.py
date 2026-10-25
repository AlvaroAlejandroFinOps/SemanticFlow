"""
Concurrency control and per-company filelock primitives for SemanticFlow.
"""
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from filelock import FileLock, Timeout

from src.core.security.sanitize import resolve_within, sanitize_company_id


class ConcurrencyLockError(RuntimeError, TimeoutError):
    """Raised when an exclusive company compilation lock cannot be acquired within timeout."""


@contextmanager
def acquire_company_lock(
    company_id: str,
    lock_root: Optional[Path] = None,
    timeout_sec: float = 30.0,
    timeout_seconds: Optional[float] = None,
) -> Iterator[Path]:
    """
    Bloqueo exclusivo por compañía bajo lock_root/.locks/<company_id>.lock para prevenir
    condiciones de carrera entre ejecuciones concurrentes del Agente IDE y la CLI.
    """
    effective_timeout = timeout_seconds if timeout_seconds is not None else timeout_sec
    safe_id = sanitize_company_id(company_id)

    if lock_root is None:
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        base_resolved = (project_root / "artifacts" / "SemanticFlow" / "outputs").resolve()
    else:
        base_resolved = Path(lock_root).resolve()

    base_resolved.mkdir(parents=True, exist_ok=True)
    locks_dir = resolve_within(base_resolved, base_resolved / ".locks")
    locks_dir.mkdir(parents=True, exist_ok=True)
    lock_file = resolve_within(locks_dir, locks_dir / f"{safe_id}.lock")

    lock = FileLock(str(lock_file), timeout=effective_timeout)
    try:
        lock.acquire(timeout=effective_timeout)
        yield lock_file
    except Timeout as exc:
        raise ConcurrencyLockError(
            f"No se pudo adquirir el bloqueo exclusivo para la empresa '{safe_id}' "
            f"tras esperar {effective_timeout}s. Otra instancia del Agente IDE o CLI está compilando."
        ) from exc
    finally:
        if lock.is_locked:
            lock.release()
