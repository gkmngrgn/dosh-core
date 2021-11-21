use crate::constants::DOSH_FOLDER_NAME;
use std::{fs, io};

pub struct Config {}

impl Config {
    pub fn new() -> Self {
        Self {}
    }

    pub fn initialize(self) -> io::Result<()> {
        fs::create_dir_all(DOSH_FOLDER_NAME)
    }
}
