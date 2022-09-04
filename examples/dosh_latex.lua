-- all my cover letters, resumes, presentations are written in LaTeX.
-- I use this script for generating PDF files.

cmd.add_task{
   name="build",
   description="run formatter and generate pdf files",
   command=function ()
      local commands = {"latexindent", "ladexmk"}
      for i = 1, #commands do
         if not cmd.exists_command(commands[i]) then
            error("Command does not exist: " .. commands[i])
         end
      end

      cmd.eval("latexindent -w -s tex/*.tex")
      cmd.eval("latexmk -xelatex tex/*.tex")
      cmd.eval("mkdir -p pdf/ && mv *.pdf pdf/")
   end
}

cmd.add_task{
   name="clean",
   description="remove build files, except pdfs",
   command=function ()
      cmd.eval("rm *.{aux,fdb_latexmk,fls,log,out,xdv}")
      cmd.eval("rm tex/*.bak*")
   end
}
