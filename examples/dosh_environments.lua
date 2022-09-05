-- limit command use by the environment.

local ENV_PROD = "prod"
local ENV_STAG = "stag"

cmd.add_task{
   name="train_data",
   description="train data in server",
   environments={ENV_PROD, ENV_STAG},
   command=function ()
      cmd.run_url("http://localhost:8000/train_data.sh")
   end
}
