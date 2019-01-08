import pkgutil

from lml.plugin import PluginManager


class NoPluginException(Exception):
    pass


class CustomPluginManager(PluginManager):
    def __init__(self):
        PluginManager.__init__(self, 'custom')

    def get_a_plugin(self, plugin_match_title=None,
                     plugin_name=None, **keywords):
        """
        根据插件名称获取对应插件实例
        如果有egg包插件则加载egg插件(定制优先原则)
        :param plugin_match_title: 插件匹配头
        :param plugin_name: 具体插件名(定制插件为egg包目录名)
        :param keywords: 参数
        :return:
        """
        egg_plugin = self.get_egg_plugin(plugin_match_title)
        key_plugin = egg_plugin if egg_plugin else plugin_name
        return PluginManager.get_a_plugin(self, key=key_plugin, **keywords)

    @staticmethod
    def get_egg_plugin(plugin_match_title):
        """
        根据插件前缀获取egg包插件
        :param plugin_match_title: 插件匹配头
        :return: egg包插件(xxx_custom)/没有包插件返回None
        """
        module_names = (module_info[1]
                        for module_info in pkgutil.iter_modules()
                        if module_info[2] and
                        module_info[1].startswith(plugin_match_title))
        for module_tmp in module_names:
            if module_tmp.endswith("custom"):
                return module_tmp
        return None

    def raise_exception(self, key):
        raise NoPluginException("cannot find a plugin")
