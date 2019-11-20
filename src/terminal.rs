extern crate term;
use std::io::prelude::*;

pub struct Terminal {
    stdout: Box<term::StdoutTerminal>,
    stderr: Box<term::StderrTerminal>,
}

impl Terminal {
    pub fn new() -> Self {
        Self {
            stdout: term::stdout().unwrap(),
            stderr: term::stderr().unwrap(),
        }
    }

    pub fn empty_line(&mut self) {
        writeln!(self.stdout, "").unwrap();
    }

    pub fn error(&mut self, text: &str) {
        self.stderr.fg(term::color::RED).unwrap();
        writeln!(self.stderr, "{}", text).unwrap();
        self.stderr.reset().unwrap();
    }

    pub fn line(&mut self, text: &str) {
        writeln!(self.stdout, "{}", text).unwrap();
    }

    pub fn title(&mut self, text: &str) {
        self.stdout.fg(term::color::CYAN).unwrap();
        writeln!(self.stdout, "{}", text).unwrap();
        self.stdout.reset().unwrap();
    }
}
