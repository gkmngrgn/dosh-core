use console::style;

pub struct Help {}

impl Help {
    pub fn new() -> Self {
        Self {}
    }

    pub fn print(self) {
        println!("{}", style("Available commands:").cyan());
    }
}
