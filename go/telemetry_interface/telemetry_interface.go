package main

import(
	"fmt"
	"context"
	"time"

	"github.com/airmap/telemetry_client"
	"github.com/airmap/interfaces/src/go/telemetry"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)

	token := "..."

	md := metadata.New(map[string]string{
	    "authorization": fmt.Sprintf("Bearer %s", token),
	})

	mdCtx := metadata.NewOutgoingContext(ctx, md)
	stream, err := client.ConnectProvider(mdCtx)


}
