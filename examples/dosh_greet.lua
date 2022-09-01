-- task: say hello to anyone. it takes an argument.
cmd.add_task{
   name="say_hello",
   description="say hello to anyone",
   command=function(there)
      there = there or "world"
      cmd.info("hello " .. there .. "!")
   end
}

-- task: install my favourite apps.
cmd.add_task{
   name="check_my_apps",
   command=function()
      if not env.IS_ZSH then
         cmd.error("did you forget to install or activate zsh?")
      else
         cmd.info("you have zsh.")
      end
   end
}
