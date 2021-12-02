use std::fs::{create_dir_all, File};
use std::io::Write;
use std::path::PathBuf;

use crate::command::Command;
use crate::constants::{DOSH_BUILD_DIR, DOSH_CONF_DIR, DOSH_CONF_NAME};

#[derive(Clone)]
pub struct Config {
    config_dir: PathBuf,
}

impl Config {
    pub fn new() -> Self {
        let config_dir = PathBuf::from(DOSH_CONF_DIR);
        Self { config_dir }
    }

    pub fn get_commands(self) -> Vec<Command> {
        let mut commands = vec![];
        for path in self.config_dir.read_dir().unwrap() {
            let command = Command::new(
                path.unwrap()
                    .file_name()
                    .to_str()
                    .unwrap()
                    .strip_suffix(".bzl")
                    .unwrap(),
                "description", // FIXME: get description of command.
            );
            commands.push(command);
        }
        commands
    }

    pub fn initialize(self) -> Result<&'static str, &'static str> {
        if !self.config_dir.exists() {
            match create_dir_all(DOSH_CONF_DIR) {
                Err(e) => {
                    dbg!(e);
                    return Err("error 1.");
                }
                _ => {
                    dbg!("folder is available.");
                }
            }
        }

        let dosh_path = self.config_dir.clone().join(DOSH_CONF_NAME);

        if !dosh_path.exists() {
            let mut dosh_file = File::create(dosh_path).unwrap();
            if let Err(e) = dosh_file.write(b"DOSH_VERSION = \"0.1.0\"") {
                dbg!("error 2.");
                eprintln!("{}", e);
            }
        }

        Ok("initialized.")
    }
}
