use serde::{Deserialize, Serialize};
use serde_yaml::{Mapping, Number, Value};
use std::collections::HashMap;
extern crate term;
use std::io::prelude::*;

pub static FILE_NAME: &str = "dosh.yaml";

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct Config {
    settings: Mapping,
    environments: Vec<String>,
    aliases: HashMap<String, Alias>,
    commands: HashMap<String, Command>,
}

impl Config {
    pub fn new() -> Self {
        let mut config = Self {
            settings: Mapping::new(),
            environments: vec!["PROD".to_string(), "TEST".to_string()],
            aliases: HashMap::new(),
            commands: HashMap::new(),
        };

        // Settings
        config.settings.insert(
            Value::String("version".to_string()),
            Value::String(env!("CARGO_PKG_VERSION").to_string()),
        );
        config.settings.insert(
            Value::String("verbosity".to_string()),
            Value::Number(Number::from(0)),
        );

        // Aliases
        config.aliases.insert(
            "hugo".to_string(),
            Alias {
                default: "hugo".to_string(),
                linux: None,
                mac: None,
                win: Some("hugo.exe".to_string()),
            },
        );

        // Commands
        config.commands.insert(
            "start".to_string(),
            Command {
                environments: vec![],
                help_text: "run the development server".to_string(),
                run: CommandRun::OneLine(String::from("{hugo} server -D")),
            },
        );
        config.commands.insert(
            "build".to_string(),
            Command {
                environments: vec![],
                help_text: "generate static files to the public folder".to_string(),
                run: CommandRun::OneLine(String::from("{hugo}")),
            },
        );
        config.commands.insert(
            "deploy".to_string(),
            Command {
                environments: vec!["PROD".to_string()],
                help_text: "deploy to the production server".to_string(),
                run: CommandRun::Group(vec![
                    String::from("CMD build"),
                    String::from("CD public"),
                    String::from("RUN git add ."),
                    String::from("RUN git commit -m \"publish changes.\""),
                    String::from("RUN git push origin master"),
                    String::from("CD .."),
                    String::from("PRINT \"DONE.\""),
                ]),
            },
        );

        config
    }

    pub fn print_usage(self) {
        let mut t = term::stdout().unwrap();

        t.fg(term::color::CYAN).unwrap();
        writeln!(t, "Environments").unwrap();
        t.reset().unwrap();

        for environment in self.environments {
            writeln!(t, "  - {}", environment).unwrap();
        }
        writeln!(t, "").unwrap();

        t.fg(term::color::CYAN).unwrap();
        writeln!(t, "Commands").unwrap();
        t.reset().unwrap();

        for (name, command) in self.commands {
            writeln!(
                t,
                "  > {name:20} {help_text}",
                name = name,
                help_text = command.help_text
            )
            .unwrap();
        }
        t.reset().unwrap();
    }
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct Alias {
    default: String,
    linux: Option<String>,
    mac: Option<String>,
    win: Option<String>,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct Command {
    help_text: String,
    run: CommandRun,
    environments: Vec<String>,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum CommandRun {
    OneLine(String),
    Group(Vec<String>),
}
