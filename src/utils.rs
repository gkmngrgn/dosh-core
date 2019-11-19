use crate::config;
use serde_yaml;
use std::env;
use std::fs::File;
use std::io::prelude::*;

pub fn get_config() -> Result<config::Config, String> {
    let mut current_dir = env::current_dir().unwrap();
    loop {
        if current_dir.join(config::FILE_NAME).exists() {
            break;
        }
        match current_dir.parent() {
            Some(parent_dir) => current_dir = parent_dir.to_path_buf(),
            None => {
                let msg = format!("Config file {} could not be found.", config::FILE_NAME);
                return Err(msg);
            }
        }
    }

    let mut config_str = String::new();
    let mut config_file = File::open(current_dir.join(config::FILE_NAME)).unwrap();
    config_file.read_to_string(&mut config_str).unwrap();

    match serde_yaml::from_str(&config_str) {
        Ok(config) => Ok(config),
        Err(_) => {
            let msg = format!("Config file {} is not valid.", config::FILE_NAME);
            Err(msg)
        }
    }
}
