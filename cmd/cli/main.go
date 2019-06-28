package main

import (
	"flag"
	"fmt"
	"os"

	"dosh"
)

var (
	cmdInit, cmdGen, cmdRun                              *flag.FlagSet
	flagInitConf, flagGenConf, flagRunConf, flagGenShell *string
	flagGenForce                                         *bool
)

func init() {
	// Param: Initialize
	cmdInit = flag.NewFlagSet("initialize", flag.ExitOnError)
	flagInitConf = cmdInit.String("config", dosh.DefaultConf, getText("flag-conf-desc"))

	// Param: Generate
	cmdGen = flag.NewFlagSet("generate", flag.ExitOnError)
	flagGenConf = cmdGen.String("config", dosh.DefaultConf, getText("flag-conf-desc"))
	flagGenShell = cmdGen.String("shell", "", getText("flag-gen-shell-desc"))
	flagGenForce = cmdGen.Bool("force", false, getText("flag-gen-force-desc"))

	// Param: Run
	cmdRun = flag.NewFlagSet("run", flag.ExitOnError)
	flagRunConf = cmdRun.String("config", dosh.DefaultConf, getText("flag-conf-desc"))
}

func printVersion() {
	fmt.Printf("%s %s", dosh.AppCliName, dosh.AppVersion)
}

func printUsage() {
	fmt.Printf(
		"%s: %s <%s> [<%s>]\n",
		getText("usage"), dosh.AppCliName, getText("commands"), getText("options"))
	fmt.Println()
	fmt.Println(getText("commands"))
	fmt.Printf("    generate        %s\n", getText("cmd-gen-desc"))
	fmt.Printf("    initialize      %s\n", getText("cmd-init-desc"))
	fmt.Printf("    run             %s\n", getText("cmd-run-desc"))
	fmt.Println()
	fmt.Printf("    help            %s\n", getText("cmd-help-desc"))
	fmt.Printf("    version         %s\n", getText("cmd-vers-desc"))
}

func main() {
	if len(os.Args) == 1 || os.Args[1] == "help" {
		printUsage()
		os.Exit(0)
	}

	cmd := os.Args[1]

	if cmd == "version" {
		printVersion()
		os.Exit(0)
	}

	commands := [3]string{
		cmdGen.Name(),
		cmdInit.Name(),
		cmdRun.Name(),
	}

	isValidCmd := false
	for _, command := range commands {
		if cmd == command {
			isValidCmd = true
			break
		}
	}

	if !isValidCmd {
		printUsage()
		os.Exit(1)
	}

	flag.Parse()

	args := os.Args[2:]

	switch cmd {
	case cmdGen.Name():
		cmdGen.Parse(args)
		genScript(*flagGenConf, *flagGenShell, *flagGenForce)
	case cmdInit.Name():
		cmdInit.Parse(args)
		initConf(*flagInitConf)
	case cmdRun.Name():
		cmdRun.Parse(args)
		dosh.RunCommand(*flagRunConf, args)
	default:
		fmt.Printf("%q is not valid cmd.\n", cmd)
		os.Exit(2)
	}
}
