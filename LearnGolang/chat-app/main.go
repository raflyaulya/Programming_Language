package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
	"sync"
)

var clients = make(map[string]net.Conn)
var lock sync.Mutex

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <server|client> [IP] [Port]")
		return
	}

	mode := os.Args[1]

	if mode == "server" {
		runServer()
	} else if mode == "client" {
		runClient()
	} else {
		fmt.Println("Invalid mode. Use 'server' or 'client'.")
	}
}

func runServer() {
	port := ":8080" // Default port
	if len(os.Args) > 2 {
		port = ":" + os.Args[2]
	}

	listener, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Println("Error starting server:", err)
		return
	}
	defer listener.Close()
	fmt.Println("Server started on", port)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}

		go handleClient(conn)
	}
}

func handleClient(conn net.Conn) {
	defer conn.Close()
	reader := bufio.NewReader(conn)

	// First message is the nickname
	nickname, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("Error reading nickname:", err)
		return
	}
	nickname = strings.TrimSpace(nickname)

	lock.Lock()
	clients[nickname] = conn
	lock.Unlock()

	fmt.Println("Connected:", nickname)

	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Connection lost for", nickname)
			lock.Lock()
			delete(clients, nickname)
			lock.Unlock()
			return
		}

		handleMessage(nickname, message)
	}
}

func handleMessage(sender string, message string) {
	message = strings.TrimSpace(message)
	if strings.HasPrefix(message, "@") {
		parts := strings.SplitN(message, " ", 2)
		if len(parts) < 2 {
			return
		}

		recipient := strings.TrimPrefix(parts[0], "@")
		text := parts[1]

		lock.Lock()
		conn, exists := clients[recipient]
		lock.Unlock()

		if exists {
			conn.Write([]byte(fmt.Sprintf("[%s]: %s\n", sender, text)))
		}
	} else {
		lock.Lock()
		for nickname, conn := range clients {
			if nickname != sender {
				conn.Write([]byte(fmt.Sprintf("[%s]: %s\n", sender, message)))
			}
		}
		lock.Unlock()
	}
}

func runClient() {
	if len(os.Args) < 4 {
		fmt.Println("Usage: go run main.go client <IP> <Port>")
		return
	}

	address := os.Args[2] + ":" + os.Args[3]
	conn, err := net.Dial("tcp", address)
	if err != nil {
		fmt.Println("Error connecting to server:", err)
		return
	}
	defer conn.Close()

	fmt.Print("Enter your nickname: ")
	reader := bufio.NewReader(os.Stdin)
	nickname, _ := reader.ReadString('\n')
	nickname = strings.TrimSpace(nickname)

	conn.Write([]byte(nickname + "\n"))

	go func() {
		serverReader := bufio.NewReader(conn)
		for {
			message, err := serverReader.ReadString('\n')
			if err != nil {
				fmt.Println("Disconnected from server.")
				return
			}
			fmt.Print(message)
		}
	}()

	for {
		text, _ := reader.ReadString('\n')
		text = strings.TrimSpace(text)
		conn.Write([]byte(text + "\n"))
	}
}
