import subprocess

# Uninstall all packages
installed_packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8').split('\n')
for package in installed_packages:
    if package and not package.startswith('-e'):
        subprocess.call(['pip', 'uninstall', '-y', package])

# Reinstall packages from requirements.txt
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
