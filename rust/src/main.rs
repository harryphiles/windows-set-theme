use chrono::prelude::*;
use std::process::{Command, Output};

fn run_powershell_command(cmd: &str) -> Result<String, String> {
    let program_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe";
    let output: Output = Command::new(program_path)
        .arg("-Command")
        .arg(cmd)
        .output()
        .map_err(|e| e.to_string())?;
    
    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}

fn get_theme_values() -> Vec<i32> {
    let value_names = ["SystemUsesLightTheme", "AppsUseLightTheme"];
    let get_command = r"Get-ItemPropertyValue -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name ";
    let mut results = Vec::new();
    for name in value_names.iter() {
        let command = format!("{}{}", get_command, name);
        if let Ok(result) = run_powershell_command(&command) {
            if let Ok(value) = result.trim().parse::<i32>() {
                results.push(value);
            }
        }
    }
    results
}

fn get_commands(value: i32) -> Vec<String> {
    let value_names = ["SystemUsesLightTheme", "AppsUseLightTheme"];
    let prefix = r"New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name";
    let suffix = "-Type Dword -Force";
    value_names
        .iter()
        .map(|&name| format!("{} {} -Value {} {}", prefix, name, value, suffix))
        .collect()
}

fn set_theme(theme: i32) {
    for command in get_commands(theme) {
        let _ = run_powershell_command(&command);
    }
}

fn restart_explorer() {
    let restart_command = "Stop-Process -Name explorer -Force; Start-Sleep -s 2; Start-Process explorer";
    let _ = run_powershell_command(restart_command);
}

fn is_daytime() -> bool {
    let now = Local::now().time();
    let daytime_start = NaiveTime::from_hms_opt(8, 0, 0).expect("Invalid time");
    let daytime_end = NaiveTime::from_hms_opt(18, 0, 0).expect("Invalid time");
    now > daytime_start && now < daytime_end
}

fn main() {
    let theme_values = get_theme_values();
    let desired_theme = if is_daytime() { 1 } else { 0 };
    if !theme_values.is_empty() {
        let current_theme = theme_values.iter().sum::<i32>() / theme_values.len() as i32;
        if desired_theme != current_theme {
            set_theme(desired_theme);
            restart_explorer();
        }
    }
}
