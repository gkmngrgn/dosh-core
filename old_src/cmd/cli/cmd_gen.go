package main

import "fmt"

const (
	paramBASH = "bash"
	paramPWSH = "pwsh"
)

func genScript(conf, shell string, force bool) {
	switch shell {
	case paramBASH:
		fmt.Println("BASH")
	case paramPWSH:
		fmt.Println("PWSH")
	default:
		fmt.Println("unknown shell type.")
	}
}
