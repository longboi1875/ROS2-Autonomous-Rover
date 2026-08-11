from glob import glob
from setuptools import find_packages, setup

package_name = 'rover_mission'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools', 'PyYAML'],
    zip_safe=True,
    maintainer='Gurnek Sandhu',
    maintainer_email='gurnek@mercedesandsingh.com',
    description='Waypoint mission execution and progress reporting.',
    license='Apache-2.0',
    entry_points={'console_scripts': ['mission_manager = rover_mission.mission_manager:main']},
)

