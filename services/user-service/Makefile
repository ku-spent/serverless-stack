.PHONY: build clean deploy gomodgen

local:
	npm run dev

build:
	export GO111MODULE=on
	env GOOS=linux go build -ldflags="-s -w" -o bin/users user/deliveries/lambda/main.go

clean:
	rm -rf ./bin ./vendor go.sum

get:
	go mod download

deploy: clean get build
	sls deploy --verbose
