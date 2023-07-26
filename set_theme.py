import subprocess
from datetime import datetime, time
from typing import List


def run_powershell_command(cmd: str) -> str:
    """run power shell command"""
    try:
        program_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        proc = subprocess.run([program_path, "-Command", cmd], capture_output=True, text=True, check=True)
        if proc.returncode != 0:
            return proc.stdout
        return proc.stdout
    except Exception as exc:
        return exc.__class__, exc

def is_daytime() -> bool:
    """check whether current time is in the daytime or not"""
    daytime_start = time(8,0)
    daytime_end = time(19,0)
    current_time = datetime.now().time()
    if daytime_start < current_time < daytime_end:
        return 1
    return 0

def get_theme_values() -> List[int]:
    """get values for Windows light theme settings 1(light) or 0(dark)"""
    value_names = ["SystemUsesLightTheme", "AppsUseLightTheme"]
    get_command = r"Get-ItemPropertyValue -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name "
    commands = [get_command + name for name in value_names]
    result = [int(run_powershell_command(command)) for command in commands]
    return result

def get_commands(value: int) -> List[str]:
    """generate commands with input value (dark or light)"""
    value_names = ["SystemUsesLightTheme", "AppsUseLightTheme"]
    prefix = r"New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name"
    suffix = "-Type Dword -Force"
    commands = [" ".join([prefix, name, f"-Value {value}",suffix]) for name in value_names]
    return commands


if __name__ == "__main__":
    desired_theme = is_daytime()
    theme_settings = get_theme_values()
    if desired_theme != sum(theme_settings) / len(theme_settings):
        for command in get_commands(desired_theme):
            run_powershell_command(command)
