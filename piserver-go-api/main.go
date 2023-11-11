package main

import (
	"fmt"
	"net/http"
)

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	fmt.Fprint(w, "Hello From Go Server!\n")
}

func main() {
	http.HandleFunc("/ping", pingHandler)

	port := 8080
	fmt.Printf("Server is running on port %d\n", port)
	// err := http.ListenAndServe(fmt.Sprintf(":%d", port), nil)
	err := http.ListenAndServe("192.168.1.5:8080", nil)

	if err != nil {
		fmt.Printf("Error starting the server %s\n", err)
	}
}
