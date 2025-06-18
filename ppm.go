package main

import (
	"fmt"
	"os"
	"os/user"

	"github.com/fatih/color"
)

const Version string = "0.1"

var helpText = `
Usage: ppm [options] <command>

ppm is a command-line package manager currently under testing.
If you encounter any issues while using ppm, please report them at: https://github.com/the-OmegaLabs/ppm/issues

This software is licensed under the Apache License v2.0.

Common commands:
init         Initialize configuration files and software sources
reset        Forcefully remove the ppm process lock
refresh      Synchronize with the dpkg database
update       Update the package list
search       Search for packages by keyword
clean        Clean ppm cache files
download     Download a package by keyword (beta)`

var (
	warnColor = color.New(color.FgYellow)
	failColor = color.New(color.FgRed)
	infoColor = color.New(color.FgBlue)
	doneColor = color.New(color.FgGreen)
)

func isPipe() bool {
	fi, err := os.Stdin.Stat()
	if err != nil {
		return false
	}

	return fi.Mode()&os.ModeNamedPipe != 0
}

func mark(c *color.Color) {
	c.Print("<>")
}

func warn() { mark(warnColor) }
func fail() { mark(failColor) }
func info() { mark(infoColor) }
func done() { mark(doneColor) }

func checkEnv() bool {
	usr, _ := user.Current()

	var err bool = false

	if isPipe() {
		fail()
		fmt.Println(" This program cannot be run from a pipe.")
		err = true
	}

	if usr.Uid != "0" {
		fail()
		fmt.Println(" This operation requires administrative privileges.")
		err = true
	}

	os.MkdirAll("/var/ppm/", 0755)
	os.MkdirAll("/etc/ppm/", 0755)

	return err
}

func main() {
	fmt.Println("ppm", Version)

	if !checkEnv() {
		return
	}
}
