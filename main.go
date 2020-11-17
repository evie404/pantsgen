package main

import (
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/go-python/gpython/parser"
)

func main() {
	flag.Parse()
	if len(flag.Args()) == 0 {
		log.Printf("Need files to parse")
		os.Exit(1)
	}

	parser.SetDebug(4)

	for _, path := range flag.Args() {
		in, err := os.Open(path)
		if err != nil {
			log.Fatal(err)
		}

		fmt.Printf("-----------------\n")

		mod, err := parser.Parse(in, path, "exec")
		if err != nil {
			log.Fatal(err)
		}

		fmt.Printf("%+v\n", mod)
	}

}
