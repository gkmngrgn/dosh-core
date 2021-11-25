use console::style;

use crate::config::Config;

pub struct Help {
    config: Config,
}

impl Help {
    pub fn new(config: Config) -> Self {
        Self { config }
    }

    pub fn print(self) {
        println!("{}", style("Available commands:").cyan());
        for command in &self.config.get_commands() {
            println!("  > {}: {}", command.name, command.description);
        }
    }
}
