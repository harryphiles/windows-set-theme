import subprocess
from datetime import datetime, time


def run_powershell_command(command: str) -> str:
    """run power shell command"""
    try:
        program_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        proc = subprocess.run([program_path, "-Command", command], capture_output=True, text=True)
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
    if daytime_start < current_time and current_time < daytime_end:
        return 1
    return 0

def get_light_theme_values() -> list:
    """get values for Windows light theme settings 1(light) or 0(dark)"""
    value_names = ["SystemUsesLightTheme", "AppsUseLightTheme"]
    get_command = f"Get-ItemPropertyValue -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name "
    commands = [get_command + name for name in value_names]
    result = [int(run_powershell_command(command)) for command in commands]
    return result

def get_commands(value: int) -> list:
    value_names = ["SystemUsesLightTheme", "AppsUseLightTheme"]
    prefix = "New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name"
    suffix = "-Type Dword -Force"
    commands = [" ".join([prefix, name, f"-Value {value}",suffix]) for name in value_names]
    return commands


if __name__ == "__main__":
    daytime = is_daytime()
    current_state = get_light_theme_values()
    if daytime != sum(current_state) / len(current_state):
        for command in get_commands(daytime):
            run_powershell_command(command)
