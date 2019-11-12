mod cli;

fn main() {
    let app = cli::CLI::new();
    app.run();
}
