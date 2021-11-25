use std::process::exit;

use structopt::StructOpt;

use dosh::command::Command;
use dosh::config::Config;
use dosh::help::Help;

#[derive(StructOpt, Debug)]
#[structopt(name = "dosh")]
struct Opt {
    #[structopt()]
    command: Option<String>,

    /// Create a new dosh config folder in an existing directory
    #[structopt(long)]
    init: bool,

    /// Verbose mode (-v, -vv, -vvv, etc.)
    #[structopt(short, long, parse(from_occurrences))]
    verbose: u8,
}

fn main() {
    let opt = Opt::from_args();
    let config = Config::new();

    if opt.init {
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

    let is_worked = match &opt.command {
        Some(name) => {
            if name == "help" {
                false
            } else {
                let cmd = Command::new(&name, "description: foo");
                cmd.run();
                true
            }
        }
        None => true,
    };

    if !is_worked {
        let help = Help::new(config);
        help.print();
    }
}
