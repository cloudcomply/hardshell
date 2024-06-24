import distro
from src.hardshell.common.common import pkg_mgr_dnf

if distro.id().lower() in pkg_mgr_dnf:
    import dnf

    base = dnf.Base()
    base.fill_sack()
