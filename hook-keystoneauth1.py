from PyInstaller.utils.hooks import collect_data_files

# Collect data files from keystoneauth1 package
datas = collect_data_files('keystoneauth1')
