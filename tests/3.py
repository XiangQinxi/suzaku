import os
import sys
import platform
import subprocess
import json
import re
from pathlib import Path
from PIL import Image
import tempfile


def get_desktop_wallpaper():
    """
    获取当前桌面壁纸路径
    返回: 壁纸文件路径字符串，如果无法获取则返回 None
    """
    system = platform.system().lower()

    if system == 'windows':
        return _get_windows_wallpaper()
    elif system == 'darwin':
        return _get_macos_wallpaper()
    elif system == 'linux':
        return _get_linux_wallpaper()
    else:
        return None


def _get_windows_wallpaper():
    """Windows 系统获取壁纸"""
    try:
        import win32api
        import win32con
        import win32gui
    except ImportError:
        # 回退到注册表方法
        return _get_windows_wallpaper_registry()

    # 方法1: 使用 SPI_GETDESKWALLPAPER
    try:
        wallpaper_path = win32api.GetProfileVal('Desktop', 'Wallpaper', '')
        if wallpaper_path and os.path.exists(wallpaper_path):
            return wallpaper_path
    except:
        pass

    # 方法2: 读取注册表
    return _get_windows_wallpaper_registry()


def _get_windows_wallpaper_registry():
    """通过注册表获取Windows壁纸路径"""
    try:
        import winreg
    except ImportError:
        return None

    try:
        # 尝试从当前用户的个性化设置获取
        key_path = r"Control Panel\Desktop"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            wallpaper_path, _ = winreg.QueryValueEx(key, "Wallpaper")
            if wallpaper_path and os.path.exists(wallpaper_path):
                return wallpaper_path

        # 尝试从系统主题获取
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            try:
                theme_path, _ = winreg.QueryValueEx(key, "CurrentTheme")
                if theme_path:
                    # 解析主题文件获取壁纸路径
                    theme_path = theme_path.replace('\\', '/')
                    if os.path.exists(theme_path):
                        with open(theme_path, 'r') as f:
                            content = f.read()
                            match = re.search(r'Wallpaper\s*=\s*(.+)', content)
                            if match:
                                wallpaper_path = match.group(1).strip()
                                if os.path.exists(wallpaper_path):
                                    return wallpaper_path
            except FileNotFoundError:
                pass
    except Exception:
        pass

    return None


def _get_macos_wallpaper():
    """macOS 系统获取壁纸"""
    try:
        # 方法1: 使用AppleScript获取当前空间壁纸
        script = """
        tell application "System Events"
            tell current desktop
                return picture
            end tell
        end tell
        """
        result = subprocess.run(['osascript', '-e', script],
                                capture_output=True, text=True)
        wallpaper_path = result.stdout.strip()
        if wallpaper_path and os.path.exists(wallpaper_path):
            return wallpaper_path

        # 方法2: 检查默认壁纸位置
        default_path = os.path.expanduser(
            "~/Library/Application Support/Dock/desktoppicture.db")
        if os.path.exists(default_path):
            # 尝试从数据库读取
            return _parse_macos_wallpaper_db(default_path)
    except Exception:
        pass

    return None


def _parse_macos_wallpaper_db(db_path):
    """解析macOS壁纸数据库"""
    try:
        # 使用sqlite3读取数据库
        import sqlite3

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 获取最新壁纸设置
        cursor.execute("SELECT value FROM data ORDER BY rowid DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            # 路径可能是二进制plist格式
            from Foundation import NSData, NSPropertyListSerialization
            data = NSData.dataWithBytes_length_(result[0], len(result[0]))
            plist, _, _ = NSPropertyListSerialization.propertyListWithData_options_format_error_(
                data, 0, None, None
            )

            if plist and '$objects' in plist:
                # 在plist对象中查找路径
                for obj in plist['$objects']:
                    if isinstance(obj, str) and obj.startswith('/'):
                        if os.path.exists(obj):
                            return obj
    except ImportError:
        # 没有PyObjC的情况
        pass
    except Exception:
        pass

    return None


def _get_linux_wallpaper():
    """Linux 系统获取壁纸（支持多种桌面环境）"""
    # 检测当前桌面环境
    desktop_env = _detect_linux_desktop_environment()

    if desktop_env == 'gnome':
        return _get_gnome_wallpaper()
    elif desktop_env == 'kde':
        return _get_kde_wallpaper()
    elif desktop_env == 'xfce':
        return _get_xfce_wallpaper()
    elif desktop_env == 'mate':
        return _get_mate_wallpaper()
    elif desktop_env == 'cinnamon':
        return _get_cinnamon_wallpaper()
    else:
        # 尝试通用方法
        return _try_common_linux_locations()


def _detect_linux_desktop_environment():
    """检测Linux桌面环境"""
    env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

    if "gnome" in env:
        return "gnome"
    elif "kde" in env:
        return "kde"
    elif "xfce" in env:
        return "xfce"
    elif "mate" in env:
        return "mate"
    elif "cinnamon" in env:
        return "cinnamon"

    # 回退检测方式
    if os.environ.get("GNOME_DESKTOP_SESSION_ID"):
        return "gnome"
    elif os.environ.get("KDE_FULL_SESSION"):
        return "kde"

    return "unknown"


def _get_gnome_wallpaper():
    """GNOME桌面环境获取壁纸"""
    try:
        # 方法1: 使用gsettings
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.background", "picture-uri"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            uri = result.stdout.strip().strip("'")
            if uri.startswith("file://"):
                path = uri[7:]
                return path
            return _convert_uri_to_path(uri)

        # 方法2: 检查配置文件
        config_path = os.path.expanduser(
            "~/.config/gnome-control-center/backgrounds/background.xml")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()
                match = re.search(r'<filename>(.*?)</filename>', content)
                if match:
                    path = match.group(1)
                    if os.path.exists(path):
                        return path
    except Exception:
        pass
    return None


def _get_kde_wallpaper():
    """KDE Plasma桌面环境获取壁纸"""
    try:
        # 方法1: 检查配置文件
        config_path = os.path.expanduser(
            "~/.config/plasma-org.kde.plasma.desktop-appletsrc")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()

                # 查找壁纸插件部分
                pattern = r'\[Containments\]\[(\d+)\]\[Wallpaper\]\[org\.kde\.image\]\[General\]\nImage=(.*)'
                matches = re.findall(pattern, content)

                if matches:
                    # 获取最新设置的壁纸
                    latest_wallpaper = matches[-1][1]
                    if latest_wallpaper and os.path.exists(latest_wallpaper):
                        return latest_wallpaper

        # 方法2: 使用DBus
        try:
            import dbus
            bus = dbus.SessionBus()
            plasma = bus.get_object('org.kde.plasmashell', '/PlasmaShell')
            script = plasma.get_dbus_method('evaluateScript', 'org.kde.PlasmaShell')
            result = script(
                "String(desktops()[0].currentConfigGroup).concat(desktops()[0].wallpaperPlugin)")
            if result:
                parts = result.split("\n")
                if len(parts) > 1 and parts[0] == "Wallpaper" and parts[
                    1] == "org.kde.image":
                    result = script(
                        "desktops()[0].currentConfigGroup = ['Wallpaper', 'org.kde.image', 'General']; String(desktops()[0].readConfig('Image'))")
                    if result:
                        path = result.split("\n")[0]
                        if os.path.exists(path):
                            return path
        except ImportError:
            pass
    except Exception:
        pass
    return None


def _get_xfce_wallpaper():
    """XFCE桌面环境获取壁纸"""
    try:
        # 方法1: 使用xfconf-query
        result = subprocess.run(
            ["xfconf-query", "-c", "xfce4-desktop", "-p",
             "/backdrop/screen0/monitor0/workspace0/last-image"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            path = result.stdout.strip()
            if os.path.exists(path):
                return path

        # 方法2: 检查配置文件
        config_path = os.path.expanduser(
            "~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()
                match = re.search(
                    r'<property name="last-image" type="string" value="(.*?)"/>', content)
                if match:
                    path = match.group(1)
                    if os.path.exists(path):
                        return path
    except Exception:
        pass
    return None


def _get_mate_wallpaper():
    """MATE桌面环境获取壁纸"""
    try:
        # 使用gsettings
        result = subprocess.run(
            ["gsettings", "get", "org.mate.background", "picture-filename"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            path = result.stdout.strip().strip("'")
            if os.path.exists(path):
                return path
    except Exception:
        pass
    return None


def _get_cinnamon_wallpaper():
    """Cinnamon桌面环境获取壁纸"""
    try:
        # 使用gsettings
        result = subprocess.run(
            ["gsettings", "get", "org.cinnamon.desktop.background", "picture-uri"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            uri = result.stdout.strip().strip("'")
            return _convert_uri_to_path(uri)
    except Exception:
        pass
    return None


def _convert_uri_to_path(uri):
    """转换URI为文件路径"""
    if uri.startswith("file://"):
        return uri[7:]
    return uri


def _try_common_linux_locations():
    """尝试常见的Linux壁纸位置"""
    common_paths = [
        os.path.expanduser("~/.background-image"),
        os.path.expanduser("~/.config/background-image"),
        "/usr/share/backgrounds/default.png",
        "/usr/share/backgrounds/default.jpg"
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    return None


def get_wallpaper_image():
    """
    获取壁纸作为PIL图像对象
    返回: PIL.Image对象 或 None
    """
    wallpaper_path = get_desktop_wallpaper()
    if wallpaper_path and os.path.exists(wallpaper_path):
        try:
            return Image.open(wallpaper_path)
        except Exception:
            pass
    return None


def save_wallpaper_copy(destination_path):
    """
    保存壁纸副本到指定路径
    返回: 成功返回True，失败返回False
    """
    wallpaper_path = get_desktop_wallpaper()
    if wallpaper_path and os.path.exists(wallpaper_path):
        try:
            # 直接复制文件
            import shutil
            shutil.copy2(wallpaper_path, destination_path)
            return True
        except Exception:
            # 尝试使用PIL重新保存
            try:
                img = Image.open(wallpaper_path)
                img.save(destination_path)
                return True
            except Exception:
                pass
    return False


# 使用示例
if __name__ == "__main__":
    wallpaper_path = get_desktop_wallpaper()

    if wallpaper_path:
        print(f"当前壁纸路径: {wallpaper_path}")

        # 获取壁纸图像
        wallpaper_img = get_wallpaper_image()
        if wallpaper_img:
            print(f"壁纸尺寸: {wallpaper_img.width}x{wallpaper_img.height}")

            # 保存副本
            temp_dir = tempfile.gettempdir()
            copy_path = os.path.join(temp_dir, "wallpaper_copy.jpg")
            if save_wallpaper_copy(copy_path):
                print(f"壁纸副本已保存到: {copy_path}")
            else:
                print("无法保存壁纸副本")
    else:
        print("无法获取桌面壁纸信息")

    # 各平台依赖提示
    print("\n依赖提示:")
    if platform.system() == 'Windows':
        print("Windows: 推荐安装 pywin32 (pip install pywin32)")
    elif platform.system() == 'Darwin':
        print("macOS: 推荐安装 PyObjC (pip install pyobjc)")
    elif platform.system() == 'Linux':
        print("Linux: 可能需要安装以下工具:")
        print("  - GNOME: gsettings (通常已安装)")
        print("  - KDE: dbus-python (pip install dbus-python)")
        print("  - XFCE: xfconf-query (通常已安装)")
