use crate::config;
use crate::utils;
use clap::{App, Arg, ArgMatches};
use config::Config;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

pub struct CLI<'a> {
    arg_matches: ArgMatches<'a>,
}

impl<'a> CLI<'a> {
    pub fn new() -> CLI<'a> {
        let arg_matches = App::new("Just do it, shh!")
            .version(crate_version!())
            .author(crate_authors!())
            .arg(
                Arg::with_name("init")
                    .short("i")
                    .long("init")
                    .help("Initializes a default config file")
                    .required(false)
                    .takes_value(false),
            )
            .arg(
                Arg::with_name("command")
                    .help("Runs a command that specified in config file")
                    .multiple(true)
                    .required(false)
                    .takes_value(true),
            )
            .get_matches();
        Self {
            arg_matches: arg_matches,
        }
    }

    pub fn run(&self) {
        if self.arg_matches.is_present("init") {
            match self.init_file() {
                Err(e) => println!("{:?}", e),
                _ => println!("Done."),
            }
        } else {
            match utils::get_config() {
                Ok(config) => config.print_usage(),
                Err(msg) => eprintln!("{}", msg),
            }
        }
        // if let Some(command) = self.arg_matches.values_of("command") {
        //     println!("Command: {:?}", command);
        // }
    }

    fn init_file(&self) -> std::io::Result<()> {
        if Path::new(config::FILE_NAME).exists() {
            let error_msg = format!("The file {} already exists.", config::FILE_NAME);
            return Err(std::io::Error::new(std::io::ErrorKind::Other, error_msg));
        }
        let config_default = serde_yaml::to_string(&Config::new()).unwrap();
        let mut config_file = File::create(config::FILE_NAME)?;
        config_file.write_all(config_default.as_bytes())?;
        Ok(())
    }
}
