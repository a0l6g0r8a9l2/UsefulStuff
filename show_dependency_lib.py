"""Показать список зависимых пакетов по имени пакета"""
import pkg_resources

_package_name = 'aiogram'


def get_dependencies_with():
    package = pkg_resources.working_set.by_key[_package_name]
    return [str(r) for r in package.requires()]


print(get_dependencies_with())
