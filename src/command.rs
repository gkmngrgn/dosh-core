pub struct Command {
    name: String,
}

impl Command {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.to_string(),
        }
    }

    pub fn run(self) {
        // FIXME
        dbg!("not ready yet.");
    }
}
