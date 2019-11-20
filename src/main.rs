#[macro_use]
extern crate clap;

mod cli;
mod config;
mod terminal;
mod utils;

fn main() {
    let app = cli::CLI::new();
    app.run();
}
