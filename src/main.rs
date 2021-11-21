use std::process::exit;

use dosh::command::Command;
use dosh::config::Config;
use dosh::help::Help;
use structopt::StructOpt;

#[derive(StructOpt, Debug)]
#[structopt(name = "dosh")]
struct Opt {
    #[structopt()]
    command: Option<String>,

    #[structopt(long)]
    init: bool,

    #[structopt(short, long, parse(from_occurrences))]
    verbose: u8,
}

fn main() {
    let opt = Opt::from_args();
    if opt.init {
        let config = Config::new();
        match config.initialize() {
            Ok(msg) => {
                println!("{}", msg);
                exit(0);
            }
            Err(msg) => {
                eprintln!("{}", msg);
                exit(1);
            }
        }
    }

    match &opt.command {
        Some(name) => {
            let cmd = Command::new(&name);
            cmd.run();
        }
        None => {
            let help = Help::new();
            help.print();
        }
    }
    dbg!(opt);
}
