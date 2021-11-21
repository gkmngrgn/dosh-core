use dosh::command::Command;
use structopt::StructOpt;

#[derive(StructOpt, Debug)]
#[structopt(name = "dosh")]
struct Opt {
    #[structopt()]
    command: Option<String>,

    #[structopt(short, long, parse(from_occurrences))]
    verbose: u8,
}

fn main() {
    let opt = Opt::from_args();
    match &opt.command {
        Some(name) => {
            let cmd = Command::new(&name);
            cmd.run()
        }
        None => print_help(),
    }
    dbg!(opt);
}

fn print_help() {
    dbg!("Not ready yet.");
}
