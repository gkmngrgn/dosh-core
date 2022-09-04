-- say hello to anyone. it takes an argument.

cmd.add_task{
   name="say_hello",
   description="say hello to anyone",
   command=function(there)
      there = there or "world"
      cmd.info("hello " .. there .. "!")
   end
}
