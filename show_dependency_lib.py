"""Показать список зависимых пакетов по имени пакета"""
import pkg_resources
import re

_package_name = 'aiohttp'


def get_dependencies(_package_name):
    try:
        package = pkg_resources.working_set.by_key[_package_name]
        _requires = [str(r) for r in package.requires()]
        requires = []
        for r in _requires:
            substring = re.sub(r'^\w*-?\w*', '', r)
            if substring:
                index = r.find(substring[0])
                # print(f'String {r}, substring {substring}, index {index}')
                requires.append(r[:index])
            else:
                requires.append(_package_name)
        return requires
    except KeyError:
        print(f"Не смог найти зависимые пакеты для {_package_name}, используй pip show {_package_name}")


dependencies_lst = []


def get_dependencies_recursive(_package_name):
    dependencies = get_dependencies(_package_name)
    if dependencies and len(dependencies) > 0:
        for i in dependencies:
            get_dependencies_recursive(i)
    else:
        dependencies_lst.append(_package_name)
    return dependencies_lst


print(get_dependencies_recursive('aiogram'))

