extern crate clap;
use clap::{App, Arg, ArgMatches};
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

const CONFIG_FILE_NAME: &str = "dosh.yaml";
const CONFIG_DEFAULT_CONTENT: &str = "\
settings:
    version: {version}
    verbosity: 0  # {QUIET: -1, NORMAL: 0, DEBUG: 1}
environments:
    - PROD
    - TEST
aliases:
    hugo:
        win: hugo.exe
        others: hugo  # {available OSes: win, linux, mac, bsd}
commands:
    start:
        help_text: run the development server
        run: ${hugo} server -D
    build:
        help_text: generate static files to the public folder
        run: ${hugo}
    deploy:
        environments:
            - PROD
        help_text: deploy to the production server
        run:
            - CMD build
            - CD public
            - RUN git add .
            - RUN git commit -m \"publish changes.\"
            - RUN git push origin master
            - CD ..
            - PRINT \"DONE.\"
";

pub struct CLI<'a> {
    arg_matches: ArgMatches<'a>,
}

impl<'a> CLI<'a> {
    pub fn new() -> CLI<'a> {
        let arg_matches = App::new("Just do it, shh!")
            .version("0.1.0")
            .author("Gökmen Görgen")
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
        }
        if let Some(command) = self.arg_matches.values_of("command") {
            println!("Command: {:?}", command);
        }
    }

    fn init_file(&self) -> std::io::Result<()> {
        if Path::new(CONFIG_FILE_NAME).exists() {
            let error_msg = format!("The file {} already exists.", CONFIG_FILE_NAME);
            return Err(std::io::Error::new(std::io::ErrorKind::Other, error_msg));
        }
        let mut config_file = File::create(CONFIG_FILE_NAME)?;
        config_file.write_all(CONFIG_DEFAULT_CONTENT.as_bytes())?;
        Ok(())
    }
}
