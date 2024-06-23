import dnf

base = dnf.Base()
base.fill_sack(load_system_info=True)
query = base.sack.query()
installed = query.installed()
