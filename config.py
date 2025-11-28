"""配置管理模块"""
import os
import yaml


class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, base_path):
        self.base_path = base_path
        self.config_path = os.path.join(base_path, "config")
        
    def load_chara_meta(self):
        """加载角色元数据"""
        with open(os.path.join(self.config_path, "chara_meta.yml"), 'r', encoding="utf-8") as fp:
            config = yaml.safe_load(fp)
            return config["mahoshojo"]
    
    def load_text_configs(self):
        """加载文本配置"""
        with open(os.path.join(self.config_path, "text_configs.yml"), 'r', encoding="utf-8") as fp:
            config = yaml.safe_load(fp)
            return config["text_configs"]
    
    def load_keymap(self, platform):
        """加载快捷键映射 - 确保文件存在时不会重写"""
        keymap_file = os.path.join(self.config_path, "keymap.yml")
        
        # 如果文件不存在，创建默认配置
        if not os.path.exists(keymap_file):
            default_keymap = self._get_default_keymap()
            self._save_keymap(default_keymap)
            return default_keymap.get(platform, {})
        
        try:
            with open(keymap_file, 'r', encoding="utf-8") as fp:
                config = yaml.safe_load(fp)
                return config.get(platform, {})
        except Exception as e:
            print(f"加载keymap.yml失败: {e}")
            # 返回默认配置
            return self._get_default_keymap().get(platform, {})
    
    def _get_default_keymap(self):
        """获取默认快捷键配置"""
        return {
            "win": {
                "start_generate": "ctrl+e",
                "next_character": "ctrl+j",
                "prev_character": "ctrl+l",
                "next_emotion": "ctrl+u",
                "prev_emotion": "ctrl+o",
                "next_background": "ctrl+i",
                "prev_background": "ctrl+k",
                "toggle_listener": "alt+ctrl+p",
                "character_1": "ctrl+1",
                "character_2": "ctrl+2",
                "character_3": "ctrl+3",
                "character_4": "ctrl+4",
                "character_5": "ctrl+5",
                "character_6": "ctrl+6"
            },
            "darwin": {
                "start_generate": "cmd+e",
                "next_character": "cmd+j",
                "prev_character": "cmd+l",
                "next_emotion": "cmd+u",
                "prev_emotion": "cmd+o",
                "next_background": "cmd+i",
                "prev_background": "cmd+k",
                "toggle_listener": "alt+cmd+p",
                "character_1": "cmd+1",
                "character_2": "cmd+2",
                "character_3": "cmd+3",
                "character_4": "cmd+4",
                "character_5": "cmd+5",
                "character_6": "cmd+6"
            },
            "gui": {
                "font_family": "Arial",
                "font_size": 12,
                "quick_characters": {}
            }
        }
    
    def _save_keymap(self, keymap_data):
        """保存快捷键配置"""
        try:
            keymap_file = os.path.join(self.config_path, "keymap.yml")
            with open(keymap_file, 'w', encoding='utf-8') as f:
                yaml.dump(keymap_data, f, allow_unicode=True, default_flow_style=False)
            return True
        except Exception as e:
            print(f"保存keymap.yml失败: {e}")
            return False
    
    def load_process_whitelist(self, platform):
        """加载进程白名单"""
        with open(os.path.join(self.config_path, "process_whitelist.yml"), 'r', encoding="utf-8") as fp:
            config = yaml.safe_load(fp)
            return config.get(platform, [])
    
    def load_gui_settings(self):
        """加载GUI设置"""
        keymap_file = os.path.join(self.config_path, "keymap.yml")
        default_settings = {
            "font_family": "Arial",
            "font_size": 12,
            "quick_characters": {}
        }
        
        try:
            if os.path.exists(keymap_file):
                with open(keymap_file, 'r', encoding='utf-8') as f:
                    keymap_data = yaml.safe_load(f)
                    gui_settings = keymap_data.get("gui", {})
                    
                    # 合并设置
                    for key, value in default_settings.items():
                        if key not in gui_settings:
                            gui_settings[key] = value
                    return gui_settings
        except Exception as e:
            print(f"加载GUI设置失败: {e}")
            
        return default_settings
    
    def save_gui_settings(self, settings):
        """保存GUI设置到keymap.yml - 确保不会重写整个文件"""
        try:
            keymap_file = os.path.join(self.config_path, "keymap.yml")
            
            # 读取现有的keymap文件
            if os.path.exists(keymap_file):
                with open(keymap_file, 'r', encoding='utf-8') as f:
                    keymap_data = yaml.safe_load(f) or {}
            else:
                keymap_data = self._get_default_keymap()
            
            # 更新GUI设置，保留其他设置
            keymap_data["gui"] = settings
            
            # 写回文件
            with open(keymap_file, 'w', encoding='utf-8') as f:
                yaml.dump(keymap_data, f, allow_unicode=True, default_flow_style=False)
            
            return True
        except Exception as e:
            print(f"保存GUI设置失败: {e}")
            return False


class AppConfig:
    """应用配置类"""
    
    def __init__(self, base_path):
        self.BOX_RECT = ((728, 355), (2339, 800))  # 文本框区域坐标
        self.KEY_DELAY = 0.1  # 按键延迟
        self.AUTO_PASTE_IMAGE = True
        self.AUTO_SEND_IMAGE = True
        self.BASE_PATH = base_path
        self.ASSETS_PATH = os.path.join(base_path, "assets")