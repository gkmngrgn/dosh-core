use serde::{Deserialize, Serialize};
use std::{collections::HashMap, fs::read_to_string, path::PathBuf};

use crate::constants::{DOSH_BUILD_DIR, DOSH_CONF_DIR};

#[derive(Serialize, Deserialize, Debug)]
struct CommandData {
    description: String,
    run: Vec<String>,
}

#[derive(Serialize, Deserialize, Debug)]
struct ConfigData {
    project_name: String,
    commands: HashMap<String, CommandData>,
}


struct ConfigParser {
}

impl ConfigParser {
    fn parse(self) {
        let config_path = PathBuf::from(DOSH_CONF_DIR).join(DOSH_BUILD_DIR);
        let config_str = read_to_string(config_path).unwrap();
        let config: ConfigData = serde_json::from_str(&config_str).unwrap();
    }
}
