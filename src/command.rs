pub struct Command {
    pub name: String,
    pub description: String,
}

impl Command {
    pub fn new(name: &str, description: &str) -> Self {
        Self {
            name: name.to_string(),
            description: description.to_string(),
        }
    }

    pub fn run(self) {
        // FIXME
        dbg!("not ready yet.");
    }
}
