use std::fs;

use starlark::environment::{Globals, Module};
use starlark::eval::Evaluator;
use starlark::syntax::{AstModule, Dialect};
use starlark::values::Value;

struct Context {
    pub module: Option<Module>,
}

impl Context {
    pub fn new() -> Self {
        Self {}
    }

    pub fn file(&self, file: &Path) -> impl Iterator<Item = Message> {
        let filename = &file.to_string_lossy();
        Self::err(
            filename,
            fs::read_to_string(file)
                .map(|content| self.file_with_contents(filename, content))
                .map_err(|e| e.into()),
        )
    }

    fn run(&self) {
        let content = r#"
        def hello():
           return "hello"
        hello() + " world!"
        "#;
        let ast: AstModule =
            AstModule::parse("hello_world.star", content.to_owned(), &Dialect::Standard)?;

        // We create a `Globals`, defining the standard library functions available.
        // The `standard` function uses those defined in the Starlark specification.
        let globals: Globals = Globals::standard();

        // We create a `Module`, which stores the global variables for our calculation.
        let module: Module = Module::new();

        // We create an evaluator, which controls how evaluation occurs.
        let mut eval: Evaluator = Evaluator::new(&module);

        // And finally we evaluate the code using the evaluator.
        let res: Value = eval.eval_module(ast, &globals)?;
        assert_eq!(res.unpack_str(), Some("hello world!"));

        let mut eval = Evaluator::new(module);
    }
}
