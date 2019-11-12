extern crate clap;
use clap::{App, Arg, ArgMatches};

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
            println!("init parameter is used.");
        }
        if let Some(command) = self.arg_matches.values_of("command") {
            println!("Command: {:?}", command);
        }
    }
}
