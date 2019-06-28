package main

import (
	"flag"
	"fmt"
	"os"

	"dosh"
)

var (
	flagConf *string
)

func init() {
	flagConf = flag.String("c", dosh.DefaultConf, "config file")
}

func printAvailableCommands() {
	fmt.Printf("TODO: print available commands here.")
}

func printVersion() {
	fmt.Printf("%s %s", dosh.AppName, dosh.AppVersion)
}

func main() {
	if len(os.Args) == 1 {
		printAvailableCommands()
		os.Exit(0)
	}

	cmd := os.Args[1]

	if cmd == "version" {
		printVersion()
		os.Exit(0)
	}

	flag.Parse()
	dosh.RunCommand(*flagConf, os.Args[2:])
}
